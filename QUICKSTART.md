# 📚 クイックスタートガイド

5分で始めるニュース要約メール配信システム

## ステップ 1: APIキーを取得（5分）

### 1.1 Anthropic API キー
1. https://console.anthropic.com にアクセス
2. ログイン（アカウント作成）
3. APIキーを生成してコピー

### 1.2 NewsAPI.org キー
1. https://newsapi.org にアクセス
2. サインアップ
3. APIキーをコピー（無料版で月100件のニュース取得可能）

### 1.3 Gmail アプリパスワード
1. https://myaccount.google.com にアクセス
2. 左メニュー「セキュリティ」
3. 2段階認証を有効化（有効な場合はスキップ）
4. 「アプリパスワード」から「メール」「Windows パソコン」を選択
5. 生成されたパスワードをコピー（16文字のコード）

## ステップ 2: セットアップ（3分）

```bash
# 1. 依存ライブラリをインストール
pip install -r requirements.txt

# 2. 環境設定ファイルを作成
cp .env.example .env

# 3. .env ファイルを編集してキーを設定
# Windows: notepad .env
# Mac/Linux: nano .env
#
# 以下を入力：
# GMAIL_ADDRESS=あなたのGmailアドレス
# GMAIL_APP_PASSWORD=取得したアプリパスワード
# RECIPIENT_EMAIL=ニュースの受信メールアドレス
# NEWS_API_KEY=取得したNewsAPI キー
```

## ステップ 3: テスト実行（2分）

```bash
# セットアップテストを実行
python test_setup.py

# または、ニュースを一度取得・要約して試す
python -c "from scheduler import NewsScheduler; NewsScheduler().run_once()"
```

## ステップ 4: 起動（1分）

### オプション A: 手動実行
```bash
python main.py
```

### オプション B: バックグラウンド実行
```bash
# Linux/Mac
nohup python main.py > news_daily.log 2>&1 &

# Windows (コマンドプロンプト)
# run_scheduler.bat をダブルクリック
```

## 確認事項

✅ メールが毎日朝7時に届いているか確認
✅ メール内容が正確か確認
✅ 必要なキーワードが含まれているか確認

## よくある質問

### Q: メールが届かない場合は？

A: 以下を確認してください
- GMAIL_ADDRESS と GMAIL_APP_PASSWORD が正しい
- 2段階認証が有効になっている
- アプリパスワード（16文字）を使用している
- 「安全でないアプリのアクセス」は無効になっている

### Q: ニュースが表示されない場合は？

A: 以下を確認してください
- NEWS_API_KEY が正しい
- 無料版の利用制限（月100件）に達していない
- インターネット接続が正常

### Q: 実行時刻を変更したい場合は？

A: `config.py` の `SCHEDULE_TIME` を変更
```python
SCHEDULE_TIME = "18:00"  # 朝6時に変更する場合
```

### Q: キーワードをカスタマイズしたい場合は？

A: `config.py` の `KEYWORDS` を編集
```python
KEYWORDS = {
    "custom_category": [
        "キーワード1",
        "キーワード2",
    ],
}
```

## トラブルシューティング

### メール認証エラー
```
❌ Gmail認証エラー
```
→ `GMAIL_APP_PASSWORD` を確認（スペースを含める）

### APIキー不正エラー
```
❌ News API エラー
```
→ `NEWS_API_KEY` を確認

### ライブラリエラー
```
ModuleNotFoundError: No module named 'anthropic'
```
→ `pip install -r requirements.txt` を実行

## ログ確認

バックグラウンド実行時のログを確認：
```bash
tail -f news_daily.log
```

## 次のステップ

1. ✅ セットアップが完了した
2. 🔄 毎日朝7時に自動実行されるようにスケジュール設定
3. 📊 ニュースが正確に要約されているか確認
4. 🎯 必要に応じてキーワードやスケジュールをカスタマイズ

---

詳細は [README.md](README.md) を参照してください
