# 🗾 日本の祝日一覧API / 🇯🇵 Holidays API

日本の「国民の祝日」の一覧をJSON形式で返すAPI(実際はAPI風の静的ページ)です。

データは[内閣府が公開](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)しているCSVから自動で生成しています。詳しい生成元データや更新周期は下記 [#データ更新について](#データ更新について) を参照してください。

内閣府から公開されている1955年以降のデータすべてを変換・公開しています。

## データ更新について

| | |
| - | - |
| オリジナルデータ | https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv |
| オリジナル公開ページ | [内閣府 / 「国民の祝日」について](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) |
| 更新周期 | 世界標準時 毎月15日 16時15日 |

## 全取得URL(JSON形式)

```
https://hrkn.github.io/jp-holidays/api/v1/list.json
```

### レスポンス例

```json
{
  "created": "2026-01-09T23:17:01.528647+09:00",
  "data": [
    {
      "date": "1955-01-01",
      "title": "元日",
      "day_of_week": 6,
      "day_of_week_text": "Saturday",
      "timestamp": -473418000
    },
      :
  ]
}
```

データ先頭のcreatedキーに生成を行った日付が入ります。
またdataキー内に祝日データが日付順で返されます。

| キー | 説明 |
| - | - |
|date|ISO8601形式の日付|
|title|祝日名(単に「祝日」となっているのは前後を祝日に挟まれた平日でいわゆる「国民の休日」)|
|day_of_week|ISO 8601で定める曜日の数値(0:日曜日～6:土曜日)|
|day_of_week_text|英語表記の曜日|
|timestamp|日付のUnixタイムスタンプ|

### CSV形式
URL末尾の拡張子をcsvに変更するとCSV形式で返却します。(他の年指定や年・月指定のAPIも同様です)

```
https://hrkn.github.io/jp-holidays/api/v1/list.csv
```

### レスポンス例

```csv
date,title,day_of_week,day_of_week_text,timestamp
1955-01-01,元日,6,Saturday,-473418000
1955-01-15,成人の日,6,Saturday,-472208400
1955-03-21,春分の日,1,Monday,-466592400
1955-04-29,天皇誕生日,5,Friday,-463222800
1955-05-03,憲法記念日,2,Tuesday,-462877200
  :
```

CSV形式にはデータ生成日時は含まれません。
各列の内容はJSON形式のdataキー以下の同名キーと同じ内容です。

## 年指定取得URL

```
https://hrkn.github.io/jp-holidays/api/v1/{year}/list.json
```

`year` は 1955～今年+1 の範囲で指定してください。

## 年・月指定取得URL

```
https://hrkn.github.io/jp-holidays/api/v1/{year}/{month}/list.json
```

数値が一桁になる月では `month` に0埋め2桁の数を指定してください。(例: 4月 → `04`)

## ライセンス

MIT
