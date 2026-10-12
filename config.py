"""
ニュース要約システムの設定ファイル
"""

# Gmail設定
GMAIL_ADDRESS = ""  # 送信元のGmailアドレス
GMAIL_APP_PASSWORD = ""  # Gmail アプリパスワード
RECIPIENT_EMAIL = ""  # 受信者メールアドレス

# ニュースAPI設定
NEWS_API_KEY = ""  # NewsAPI.org のAPIキー
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Anthropic API設定
ANTHROPIC_API_KEY = ""  # Anthropic API キー

# スケジューラー設定
SCHEDULE_TIME = "07:00"  # 実行時刻（朝7時）

# キーワード設定
KEYWORDS = {
    "biohacking_business": [
        "バイオハッキング ビジネス",
        "biohacking business",
        "バイオテクノロジー スタートアップ",
        "生物工学 起業",
        "NuSkin",
        "アンチエイジング ビジネス",
        "再生医療 ビジネス",
    ],
    "generative_ai": [
        "generative AI",
        "生成AI",
        'OpenAI OR Anthropic OR "Google Gemini"',
        '"large language model"',
    ],
    "sports_business": [
        "スポーツ ビジネス",
        "sports business",
        "スポーツ投資",
        "スポーツマーケティング",
        "スポーツ起業",
    ],
    "vintage_business": [
        "古着 ビジネス",
        "vintage clothing business",
        "古着販売",
        "サスティナブルファッション",
        "リサイクルファッション",
    ],
}

# 言語設定
LANGUAGE = "ja"  # 日本語

# 要約設定
MAX_ARTICLES_PER_CATEGORY = 5  # カテゴリーごとの最大記事数
SUMMARY_LENGTH = "short"  # 要約の長さ（short, medium, long）
