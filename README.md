
# 商品監視および投稿システム

このプロジェクトは、Amazon Japanの商品の在庫状況や価格を監視し、在庫がある場合にソーシャルメディアに更新を投稿することを目的としています。このアプリケーションは、ウェブスクレイピングを使用して在庫情報を収集し、ユーザーインターフェースにはPyQt5を利用しています。

## Version

2.0

## 機能

- **商品監視**: 指定された商品の在庫状況と価格変動を監視します。
- **ウェブスクレイピング**: BeautifulSoupを使用してAmazon Japanから商品詳細をスクレイピングします。
- **通知システム**: 商品が在庫あり、かつ指定された価格条件を満たす場合に通知を送信します。
- **ユーザーインターフェース**: PyQt5で構築されたインタラクティブな体験。

## 必要条件

このプロジェクトを実行するには、以下のものがインストールされている必要があります。

- Python 3.x
- PyQt5
- pandas
- requests
- beautifulsoup4
- openpyxl

必要なライブラリは、次のコマンドでインストールできます。

```bash
pip install PyQt5 pandas requests beautifulsoup4 openpyxl
```

## 使用方法

1. このリポジトリをクローンするか、ソースコードをダウンロードします。
2. 設定用の有効な `settings.json` ファイルを用意します。
3. `product_list.xlsx` という名前のExcelファイルを作成し、以下のシートを含めます。
   - **product_list**: 監視する商品のリスト。
   - **settings**: 通知の設定を含む。
4. アプリケーションを実行します。

   ```bash
   python monitor_thread.py
   ```

5. アプリケーションがExcelファイルにリストされた商品を監視し始めます。

## コード概要

プロジェクトの主なコンポーネントは以下の通りです。

- **`monitor_thread.py`**: 監視ロジックとユーザーインタラクションを処理します。
- **`amazon_scraper.py`**: 商品の在庫状況と価格を取得するためのスクレイピングロジックを含みます。
- **`sns_posting.py`**: ソーシャルメディアへの投稿を管理します。
- **`utils.py`**: 商品の状態や設定を処理するためのユーティリティ関数。

## エラーハンドリング

アプリケーションは、以下のような問題を管理するためのエラーハンドリングを含んでいます。
- 商品データ取得中のネットワークエラー。
- HTMLレスポンスからのデータ解析エラー。

監視中にエラーが発生した場合、それらは `post_log.txt` に記録されます。

## サンプル設定

`settings.json` のサンプルは次のようになります。

```json
{
    "notification_start_time": "09:00",
    "notification_end_time": "21:00"
}
```

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- [Beautiful Soup ドキュメント](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [PyQt5 ドキュメント](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
```

### カスタマイズ
プロジェクトの具体的な内容に合わせて、必要に応じて内容を変更してください！


Here’s a detailed usage section for the built application, which you can include in your `README.md`:

```markdown
## 使用方法

このアプリケーションを使用するための手順は以下の通りです。

### 1. 環境の準備

- Python 3.x がインストールされていることを確認してください。
- 必要なライブラリをインストールします。

```bash
pip install PyQt5 pandas requests beautifulsoup4 openpyxl
```

### 2. 設定ファイルの準備

- プロジェクトのルートディレクトリに `settings.json` ファイルを作成します。
- 以下のような内容で設定します。

```json
{
    "notification_start_time": "09:00",
    "notification_end_time": "21:00"
}
```

### 3. 商品リストの作成

- `product_list.xlsx` という名前のExcelファイルを作成します。
- 次の2つのシートを追加します：

#### a. product_list シート

このシートには監視したい商品の情報を入力します。列の例：

| product_name                 | product_url                      | affiliate_link             | title               | description         | start_price | end_price |
|------------------------------|----------------------------------|----------------------------|---------------------|---------------------|-------------|-----------|
| iPhone16 無印 256 (ティール)  | https://example.com/product1     | https://affiliate.com/1    | new popular product | iPhone description  | 100000      | 120000    |

#### b. settings シート

このシートには、通知に関する設定を入力します。例：

| notification_start_time | notification_end_time |
|-------------------------|-----------------------|
| 09:00                   | 21:00                 |

### 4. アプリケーションの実行

以下のコマンドを使用してアプリケーションを起動します。

```bash
python monitor_thread.py
```

### 5. アプリケーションの操作

- アプリケーションが起動すると、GUIが表示されます。
- 商品リストが読み込まれ、在庫状況と価格が監視されます。
- 在庫がある場合、指定した条件に基づいてSNSに投稿されます。

### 6. ログの確認

- 監視中にエラーが発生した場合は、`post_log.txt` ファイルに記録されます。このファイルをチェックして、問題を確認できます。

### 7. アプリケーションの終了

- 監視を停止するには、アプリケーションのウィンドウを閉じてください。

この手順に従うことで、商品監視と投稿機能を利用できるようになります。
```

Feel free to modify any part of the text to better fit your project's specific details!