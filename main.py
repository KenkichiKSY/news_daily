#!/usr/bin/env python3
"""
ニュース要約メールシステムのメインスクリプト
"""
import sys
import os
from dotenv import load_dotenv
from scheduler import NewsScheduler


def load_environment():
    """環境変数を読み込む"""
    # .env ファイルから環境変数を読み込み
    load_dotenv()

    import config

    # 環境変数から設定を上書き
    config.GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", config.GMAIL_ADDRESS)
    config.GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", config.GMAIL_APP_PASSWORD)
    config.RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", config.RECIPIENT_EMAIL)
    config.NEWS_API_KEY = os.getenv("NEWS_API_KEY", config.NEWS_API_KEY)
    config.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", config.ANTHROPIC_API_KEY)


def main():
    """メイン関数"""
    print("=" * 60)
    print("📰 ニュース要約メール配信システム")
    print("=" * 60)

    # 環境変数を読み込む
    load_environment()

    # 必要なライブラリをチェック
    try:
        import anthropic
        import requests
        import schedule
    except ImportError as e:
        print(f"❌ 必要なライブラリが見つかりません: {e}")
        print("以下を実行してください:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # 設定をチェック
    try:
        scheduler = NewsScheduler()
        scheduler.email_sender.validate_credentials()
    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
        print("\n💡 セットアップ方法:")
        print("1. .env.example を参考に .env ファイルを作成してください")
        print("2. 以下の情報を設定してください:")
        print("   - GMAIL_ADDRESS: あなたのGmailアドレス")
        print("   - GMAIL_APP_PASSWORD: Gmailのアプリパスワード")
        print("   - RECIPIENT_EMAIL: ニュースの受信メールアドレス")
        print("   - NEWS_API_KEY: NewsAPI.org から取得したAPIキー")
        sys.exit(1)

    # スケジューラーを起動
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n\n✅ システムを停止しました")
        sys.exit(0)


if __name__ == "__main__":
    main()
