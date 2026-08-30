"""
ニュース要約モジュール
"""
import anthropic
from typing import List, Dict
import config


class NewsSummarizer:
    """ニュース要約クラス"""

    def __init__(self):
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY が設定されていません")
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"

    def summarize_article(self, article: Dict) -> str:
        """
        単一の記事を要約

        Args:
            article: ニュース記事（title, description, content を含む）

        Returns:
            要約されたテキスト
        """
        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")

        # テキストを組み立て
        article_text = f"タイトル: {title}\n説明: {description}\nコンテンツ: {content}"

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[
                    {
                        "role": "user",
                        "content": f"以下のニュース記事を日本語で1-2文で簡潔に要約してください：\n\n{article_text}",
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            print(f"要約エラー: {e}")
            # エラーが発生した場合は、説明を要約として使用
            return description or title

    def summarize_category(self, category: str, articles: List[Dict]) -> str:
        """
        カテゴリーのニュースを要約

        Args:
            category: カテゴリー名
            articles: ニュース記事のリスト

        Returns:
            要約結果
        """
        if not articles:
            return f"\n📌 {category}\n該当するニュースはありません。\n"

        summary_text = f"\n📌 {category}\n"

        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "")
            url = article.get("url", "")
            source = article.get("source", {}).get("name", "")
            published_at = article.get("publishedAt", "")

            # 要約を生成
            article_summary = self.summarize_article(article)

            summary_text += f"\n{i}. {title}\n"
            summary_text += f"   {article_summary}\n"
            if source:
                summary_text += f"   出典: {source}\n"
            if url:
                summary_text += f"   URL: {url}\n"

        return summary_text

    def summarize_all_categories(self, news_by_category: Dict[str, List[Dict]]) -> str:
        """
        すべてのカテゴリーのニュースを要約

        Args:
            news_by_category: カテゴリーごとのニュース記事

        Returns:
            すべてのカテゴリーの要約
        """
        full_summary = "📰 本日のニュース要約\n"
        full_summary += "=" * 50 + "\n"

        for category, articles in news_by_category.items():
            category_summary = self.summarize_category(category, articles)
            full_summary += category_summary

        return full_summary


if __name__ == "__main__":
    from news_fetcher import NewsFetcher

    fetcher = NewsFetcher()
    news = fetcher.fetch_news_by_categories()

    summarizer = NewsSummarizer()
    summary = summarizer.summarize_all_categories(news)
    print(summary)
