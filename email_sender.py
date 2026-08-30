"""
Gmail送信モジュール
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config


class EmailSender:
    """Email送信クラス"""

    def __init__(self):
        self.gmail_address = config.GMAIL_ADDRESS
        self.gmail_app_password = config.GMAIL_APP_PASSWORD
        self.recipient_email = config.RECIPIENT_EMAIL
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def validate_credentials(self) -> bool:
        """
        メール設定が正しく設定されているか確認

        Returns:
            設定が有効かどうか
        """
        if not self.gmail_address or not self.gmail_app_password or not self.recipient_email:
            raise ValueError(
                "Gmail設定が不完全です。config.py の以下を設定してください:\n"
                "- GMAIL_ADDRESS\n"
                "- GMAIL_APP_PASSWORD\n"
                "- RECIPIENT_EMAIL"
            )
        return True

    def send_email(self, subject: str, body: str, html_body: str = None) -> bool:
        """
        メールを送信

        Args:
            subject: メールの件名
            body: メール本文（テキスト）
            html_body: メール本文（HTML）

        Returns:
            送信成功したかどうか
        """
        try:
            self.validate_credentials()

            # メッセージの作成
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.gmail_address
            msg["To"] = self.recipient_email

            # テキスト部分とHTML部分を追加
            msg.attach(MIMEText(body, "plain", "utf-8"))
            if html_body:
                msg.attach(MIMEText(html_body, "html", "utf-8"))

            # SMTP接続とメール送信
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.gmail_address, self.gmail_app_password)
                server.send_message(msg)

            print(f"✅ メール送信成功: {self.recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            print(
                "❌ Gmail認証エラー: \n"
                "- GMAIL_APP_PASSWORD が正しいか確認してください\n"
                "- 2段階認証が有効か確認してください\n"
                "- アプリパスワードを使用しているか確認してください"
            )
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP エラー: {e}")
            return False
        except Exception as e:
            print(f"❌ メール送信エラー: {e}")
            return False

    def send_news_summary(self, summary_text: str) -> bool:
        """
        ニュース要約をメールで送信

        Args:
            summary_text: ニュース要約テキスト

        Returns:
            送信成功したかどうか
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        subject = f"📰 本日のニュース要約 - {today}"

        # HTML形式のメール本文を生成
        html_body = self._create_html_body(summary_text)

        return self.send_email(subject, summary_text, html_body)

    def _create_html_body(self, text: str) -> str:
        """
        HTML形式のメール本文を生成

        Args:
            text: プレーンテキスト

        Returns:
            HTML形式のメール本文
        """
        html = """
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                h2 { color: #34495e; margin-top: 20px; }
                .category { background-color: #ecf0f1; padding: 15px; margin: 15px 0; border-left: 4px solid #3498db; }
                .article { margin: 10px 0; }
                .title { font-weight: bold; color: #2980b9; }
                .source { color: #7f8c8d; font-size: 0.9em; }
                .url { color: #3498db; text-decoration: none; }
                hr { border: none; border-top: 1px solid #bdc3c7; margin: 20px 0; }
            </style>
        </head>
        <body>
        """

        html += "<h1>📰 本日のニュース要約</h1>"
        html += text.replace("\n", "<br>").replace("📌", "<h2>📌")
        html += """
        </body>
        </html>
        """

        return html


if __name__ == "__main__":
    sender = EmailSender()
    test_summary = """
    本日のニュース要約です。

    📌 バイオハッキングに関するビジネス情報
    1. 新しいバイオハッキング企業が設立されました。
    2. バイオテクノロジーの投資が増加しています。

    📌 ClaudeCodeに関する活用方法
    1. ClaudeCodeを使った新しいプログラミング手法が注目されています。
    """
    sender.send_news_summary(test_summary)
