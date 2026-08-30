"""
スケジューラーモジュール
"""
import schedule
import time
from datetime import datetime
from news_fetcher import NewsFetcher
from news_summarizer import NewsSummarizer
from email_sender import EmailSender
import config


class NewsScheduler:
    """ニュース配信スケジューラー"""

    def __init__(self):
        self.fetcher = NewsFetcher()
        self.summarizer = NewsSummarizer()
        self.email_sender = EmailSender()

    def run_news_job(self):
        """
        ニュース取得、要約、メール送信を実行
        """
        print(f"\n🔄 ニュース配信ジョブを開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # ニュースを取得
            print("📡 ニュースを取得中...")
            news = self.fetcher.fetch_news_by_categories()

            # ニュースを要約
            print("✍️  ニュースを要約中...")
            summary = self.summarizer.summarize_all_categories(news)

            # メールで送信
            print("📧 メールを送信中...")
            if self.email_sender.send_news_summary(summary):
                print("✅ ニュース配信完了")
            else:
                print("❌ メール送信に失敗しました")

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")

    def schedule_daily_news(self):
        """
        毎日朝7時にニュース配信をスケジュール
        """
        schedule.every().day.at(config.SCHEDULE_TIME).do(self.run_news_job)
        print(f"✅ スケジューラーを設定: 毎日 {config.SCHEDULE_TIME} にニュースを配信します")

    def start(self):
        """
        スケジューラーを開始（無限ループ）
        """
        self.schedule_daily_news()

        print(f"🚀 ニュース配信システムを起動しました")
        print(f"現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Ctrl+C で終了します\n")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1分ごとにチェック
        except KeyboardInterrupt:
            print("\n\n🛑 スケジューラーを停止しました")

    def run_once(self):
        """
        一度だけ実行（テスト用）
        """
        print("🧪 テスト実行モード: 一度だけ実行します")
        self.run_news_job()


if __name__ == "__main__":
    scheduler = NewsScheduler()

    # テスト実行する場合：
    # scheduler.run_once()

    # スケジューラーを起動する場合：
    scheduler.start()
