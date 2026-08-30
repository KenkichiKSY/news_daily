"""
ニュース取得モジュール
"""
import requests
from typing import List, Dict
from datetime import datetime, timedelta
import config


class NewsFetcher:
    """ニュース取得クラス"""

    def __init__(self):
        self.api_key = config.NEWS_API_KEY
        self.api_url = config.NEWS_API_URL

    def fetch_news(self, keyword: str, days: int = 1) -> List[Dict]:
        """
        指定されたキーワードでニュースを取得

        Args:
            keyword: 検索キーワード
            days: 検索対象の日数

        Returns:
            ニュース記事のリスト
        """
        if not self.api_key:
            raise ValueError("NEWS_API_KEY が設定されていません")

        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "q": keyword,
            "from": from_date,
            "to": to_date,
            "language": config.LANGUAGE,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "pageSize": config.MAX_ARTICLES_PER_CATEGORY,
        }

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            return articles
        except requests.exceptions.RequestException as e:
            print(f"ニュース取得エラー: {e}")
            return []

    def fetch_news_by_categories(self) -> Dict[str, List[Dict]]:
        """
        設定されたすべてのカテゴリーでニュースを取得

        Returns:
            カテゴリーごとのニュース記事
        """
        results = {}

        for category, keywords in config.KEYWORDS.items():
            category_news = []
            for keyword in keywords:
                articles = self.fetch_news(keyword)
                category_news.extend(articles)

            # 重複を削除（URLが同じ記事）
            unique_articles = []
            seen_urls = set()
            for article in category_news:
                url = article.get("url")
                if url not in seen_urls:
                    unique_articles.append(article)
                    seen_urls.add(url)

            results[category] = unique_articles[: config.MAX_ARTICLES_PER_CATEGORY]

        return results


if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.fetch_news_by_categories()
    for category, articles in news.items():
        print(f"\n{category}: {len(articles)} 件")
        for article in articles[:2]:
            print(f"  - {article.get('title')}")
