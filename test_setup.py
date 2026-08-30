#!/usr/bin/env python3
"""
ニュース要約システムのテストスクリプト
"""
import os
from dotenv import load_dotenv


def test_environment():
    """環境設定をテスト"""
    print("=" * 60)
    print("🧪 環境設定テスト")
    print("=" * 60 + "\n")

    # .env ファイルを読み込み
    load_dotenv()

    import config

    config.GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", config.GMAIL_ADDRESS)
    config.GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", config.GMAIL_APP_PASSWORD)
    config.RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", config.RECIPIENT_EMAIL)
    config.NEWS_API_KEY = os.getenv("NEWS_API_KEY", config.NEWS_API_KEY)
    config.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", config.ANTHROPIC_API_KEY)

    # 1. Gmail設定
    print("1️⃣ Gmail設定の確認")
    if config.GMAIL_ADDRESS and "@gmail.com" in config.GMAIL_ADDRESS:
        print("   ✅ GMAIL_ADDRESS: 設定済み")
    else:
        print("   ❌ GMAIL_ADDRESS: 未設定または不正")

    if config.GMAIL_APP_PASSWORD and len(config.GMAIL_APP_PASSWORD.replace(" ", "")) >= 16:
        print("   ✅ GMAIL_APP_PASSWORD: 設定済み")
    else:
        print("   ❌ GMAIL_APP_PASSWORD: 未設定または不正")

    if config.RECIPIENT_EMAIL and "@" in config.RECIPIENT_EMAIL:
        print("   ✅ RECIPIENT_EMAIL: 設定済み")
    else:
        print("   ❌ RECIPIENT_EMAIL: 未設定または不正")

    # 2. NewsAPI設定
    print("\n2️⃣ NewsAPI設定の確認")
    if config.NEWS_API_KEY and len(config.NEWS_API_KEY) > 10:
        print("   ✅ NEWS_API_KEY: 設定済み")
    else:
        print("   ❌ NEWS_API_KEY: 未設定")

    # 3. Anthropic API設定
    print("\n3️⃣ Anthropic API設定の確認")
    if config.ANTHROPIC_API_KEY and len(config.ANTHROPIC_API_KEY) > 10:
        print("   ✅ ANTHROPIC_API_KEY: 設定済み")
    else:
        print("   ❌ ANTHROPIC_API_KEY: 未設定")

    # 4. キーワード設定
    print("\n4️⃣ キーワード設定の確認")
    print(f"   ✅ カテゴリー数: {len(config.KEYWORDS)}")
    for category, keywords in config.KEYWORDS.items():
        print(f"      - {category}: {len(keywords)} 個のキーワード")

    # 5. 必要なライブラリの確認
    print("\n5️⃣ 必要なライブラリの確認")
    libraries = ["anthropic", "requests", "schedule", "dotenv"]
    for lib in libraries:
        try:
            __import__(lib)
            print(f"   ✅ {lib}: インストール済み")
        except ImportError:
            print(f"   ❌ {lib}: 未インストール")


def test_news_fetcher():
    """ニュース取得をテスト"""
    print("\n" + "=" * 60)
    print("🧪 ニュース取得テスト")
    print("=" * 60 + "\n")

    load_dotenv()
    import config

    config.NEWS_API_KEY = os.getenv("NEWS_API_KEY", config.NEWS_API_KEY)

    if not config.NEWS_API_KEY:
        print("❌ NEWS_API_KEY が設定されていません")
        return

    try:
        from news_fetcher import NewsFetcher

        fetcher = NewsFetcher()
        print("📡 ニュースを取得中...\n")

        news = fetcher.fetch_news_by_categories()

        for category, articles in news.items():
            print(f"{category}: {len(articles)} 件")
            if articles:
                print(f"  - {articles[0].get('title', 'N/A')[:70]}...")

        print("\n✅ ニュース取得成功")

    except Exception as e:
        print(f"❌ エラー: {e}")


def test_email_sender():
    """メール送信をテスト"""
    print("\n" + "=" * 60)
    print("🧪 メール送信テスト")
    print("=" * 60 + "\n")

    load_dotenv()
    import config

    config.GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", config.GMAIL_ADDRESS)
    config.GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", config.GMAIL_APP_PASSWORD)
    config.RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", config.RECIPIENT_EMAIL)

    try:
        from email_sender import EmailSender

        sender = EmailSender()
        sender.validate_credentials()

        print("テストメールを送信しますか？ (y/n): ", end="")
        if input().lower() == "y":
            sender.send_email(
                subject="🧪 テスト: ニュース要約システム",
                body="これはテストメールです。システムが正常に動作しています。",
            )
        else:
            print("スキップしました")

    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
    except Exception as e:
        print(f"❌ エラー: {e}")


def test_summarizer():
    """ニュース要約をテスト"""
    print("\n" + "=" * 60)
    print("🧪 ニュース要約テスト")
    print("=" * 60 + "\n")

    try:
        from news_summarizer import NewsSummarizer

        summarizer = NewsSummarizer()

        # テスト記事
        test_article = {
            "title": "新しいバイオハッキング企業が設立",
            "description": "バイオテクノロジー分野の新興企業が資金調達に成功しました",
            "content": "これは要約のテストです。このテキストは実際のニュース記事ではなく、システムの動作確認のためのものです。",
        }

        print("📝 テスト記事を要約中...\n")
        summary = summarizer.summarize_article(test_article)
        print(f"要約結果:\n{summary}")
        print("\n✅ 要約成功")

    except Exception as e:
        print(f"❌ エラー: {e}")


def main():
    """メイン関数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  📰 ニュース要約システム - セットアップテスト".ljust(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")

    # テスト実行
    test_environment()
    test_news_fetcher()
    test_summarizer()
    test_email_sender()

    print("\n" + "=" * 60)
    print("✅ テスト完了")
    print("=" * 60 + "\n")

    print("💡 次のステップ:")
    print("1. .env ファイルに必要な設定を入力してください")
    print("2. 以下のコマンドでシステムを起動してください:")
    print("   python main.py")


if __name__ == "__main__":
    main()
