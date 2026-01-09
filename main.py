import collections
import csv
import datetime
import io
import json
import pathlib
import sys

import dateutil
import requests

JPTZ = dateutil.tz.gettz("Asia/Tokyo")


def emit_json(path: pathlib.Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False)


def emit_csv(path: pathlib.Path, data: list):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["date", "title", "day_of_week", "day_of_week_text", "timestamp"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def bind_dict(created: str, data: list):
    return {"created": created, "data": data}


def main(dir: str):
    output_dir = pathlib.Path(dir)
    output_dir.mkdir(exist_ok=True)

    response = requests.get("https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv")
    response.encoding = response.apparent_encoding
    content = io.StringIO(response.text)
    csv_data = csv.reader(content)
    next(csv_data)  # ヘッダスキップ

    monthly = collections.defaultdict(lambda: collections.defaultdict(list))
    for row in csv_data:
        date_str, title = row
        date = datetime.datetime.strptime(date_str, "%Y/%m/%d").replace(tzinfo=JPTZ)
        year = date.year
        month = date.month
        monthly[year][month].append(
            dict(
                date=date.date().isoformat(),
                title=title,
                day_of_week=date.date().isoweekday(),
                day_of_week_text=date.strftime("%A"),
                timestamp=int(date.timestamp()),
            )
        )

    created = datetime.datetime.now().astimezone(JPTZ).isoformat()
    whole = []
    for year, monthly_holiday_dict in monthly.items():
        holidays_in_year = []

        for month in range(1, 13):
            holidays_in_month = monthly_holiday_dict[month]
            whole.extend(holidays_in_month)
            holidays_in_year.extend(holidays_in_month)

            monthly_json = output_dir / f"{year}/{month:02}/list.json"
            emit_json(monthly_json, bind_dict(created, holidays_in_month))
            monthly_csv = output_dir / f"{year}/{month:02}/list.csv"
            emit_csv(monthly_csv, holidays_in_month)

        emit_json(
            output_dir / f"{year}/list.json", bind_dict(created, holidays_in_year)
        )
        emit_csv(output_dir / f"{year}/list.csv", holidays_in_year)

    emit_json(output_dir / "list.json", bind_dict(created, whole))
    emit_csv(output_dir / "list.csv", whole)


if __name__ == "__main__":
    main(sys.argv[1])
