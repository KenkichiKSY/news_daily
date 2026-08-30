# 📰 ニュース要約メール配信システム

毎日朝7時に、関連するニュースの要約をGmailで送信するシステムです。

## 機能

- 🔍 4つのカテゴリーからニュース自動取得
  - バイオハッキングに関するビジネス情報
  - ClaudeCodeに関する活用方法
  - スポーツのビジネス情報
  - 古着ビジネスにおける情報

- ✍️ Claude AIを使用した自然な要約
- 📧 毎日朝7時にGmailで自動配信
- 🎯 複数キーワードでの検索対応

## セットアップ

### 1. 必要な情報を準備

#### Gmail アプリパスワード
1. Google アカウントにアクセス: https://myaccount.google.com
2. セキュリティ → 2段階認証を有効化（有効な場合はスキップ）
3. セキュリティ → アプリパスワードを取得
4. 「メール」と「Windows パソコン」を選択してアプリパスワードを生成

#### NewsAPI.org キー
1. https://newsapi.org/ にアクセス
2. サインアップして無料APIキーを取得

#### Anthropic API キー
1. https://console.anthropic.com にアクセス
2. APIキーを生成

### 2. リポジトリをセットアップ

```bash
cd news_daily

# 依存ライブラリをインストール
pip install -r requirements.txt

# 環境変数ファイルを作成
cp .env.example .env

# .env ファイルを編集して以下を設定
# - GMAIL_ADDRESS
# - GMAIL_APP_PASSWORD
# - RECIPIENT_EMAIL
# - NEWS_API_KEY
```

### 3. 環境変数を設定

`.env` ファイルを開いて以下を入力：

```env
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
RECIPIENT_EMAIL=recipient@example.com
NEWS_API_KEY=your_news_api_key_here
```

### 4. テスト実行

```bash
python -c "from scheduler import NewsScheduler; NewsScheduler().run_once()"
```

## 使用方法

### オプション1: 手動実行

```bash
python main.py
```

Ctrl+C で終了

### オプション2: バックグラウンド実行（推奨）

#### Linux/Mac の場合

```bash
nohup python main.py > news_daily.log 2>&1 &
```

#### Windows の場合

バッチファイル `run_scheduler.bat` を作成：

```batch
@echo off
python main.py
pause
```

ダブルクリックで実行

### オプション3: cron/タスクスケジューラで管理

#### Linux/Mac（cron）

```bash
# crontab を編集
crontab -e

# 毎日朝7時に実行
0 7 * * * cd /path/to/news_daily && python main.py >> news_daily.log 2>&1
```

#### Windows（タスクスケジューラ）

1. タスクスケジューラを開く
2. 基本タスクの作成
3. トリガー：毎日 07:00
4. アクション：プログラムの開始 `python main.py`

## カスタマイズ

### キーワードの変更

`config.py` の `KEYWORDS` を編集：

```python
KEYWORDS = {
    "category_name": [
        "keyword1",
        "keyword2",
    ],
}
```

### 実行時刻の変更

`config.py` の `SCHEDULE_TIME` を編集：

```python
SCHEDULE_TIME = "07:00"  # 朝7時
```

### 記事数の変更

`config.py` の `MAX_ARTICLES_PER_CATEGORY` を編集：

```python
MAX_ARTICLES_PER_CATEGORY = 5  # カテゴリーごと5件
```

## トラブルシューティング

### ❌ メール送信エラー

- Gmail 2段階認証が有効か確認
- アプリパスワード（16文字）を使用しているか確認
- `GMAIL_APP_PASSWORD` のスペースを確認

### ❌ ニュース取得エラー

- `NEWS_API_KEY` が正しいか確認
- NewsAPI.org の利用制限を確認（無料版は月100件）

### ❌ API エラー

- Anthropic APIキーが設定されているか確認
- API利用制限を確認

## ファイル構成

```
news_daily/
├── main.py                 # メインスクリプト
├── config.py              # 設定ファイル
├── news_fetcher.py        # ニュース取得モジュール
├── news_summarizer.py     # ニュース要約モジュール
├── email_sender.py        # メール送信モジュール
├── scheduler.py           # スケジューラーモジュール
├── requirements.txt       # 依存ライブラリ
├── .env.example          # 環境変数テンプレート
└── README.md             # このファイル
```

## ログ

ログはコンソールに出力されます。バックグラウンド実行の場合は以下で確認：

```bash
tail -f news_daily.log
```

## ライセンス

MIT License

## サポート

問題が発生した場合は、ログを確認してエラーメッセージを確認してください。
