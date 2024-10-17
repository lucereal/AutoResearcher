
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import os
from web_page_reader import WebPageReader
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    author: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    publishedAt: Optional[datetime] = None
    content: Optional[object] = None
    
    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "author": self.author,
            "source": self.source,
            "description": self.description,
            "publishedAt": self.publishedAt.isoformat() if self.publishedAt else None,
            "content": self.content
        }
    
class CustomNewsApiClient:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.client = NewsApiClient(api_key=self.api_key)
        self.web_reader = WebPageReader()

    def gather_web_page_data(self, url):
        data = self.web_reader.extract_content(url)
        return data
    
    def get_news_api_results(self, q=None, sources=None, category=None, language=None, country=None):
        return self.client.get_top_headlines(q=q, sources=sources, category=category, language=language, country=country)
    
    def get_all_articles(self, q=None, sources=None, domains=None, from_param=None, to=None, language=None, sort_by=None, page=None, page_size=None):
        return self.client.get_everything(q=q, sources=sources, domains=domains, from_param=from_param, to=to, language=language, sort_by=sort_by,page_size=page_size, page=page)
    
    def get_all_articles_past_month(self, q=None):
        to_param = datetime.now().strftime('%Y-%m-%d')
        from_param = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        all_articles =custom_newsapi.get_all_articles(q=q, from_param=from_param, to=to_param, language='en', sort_by='relevancy', page=1, page_size=10)
        articles_list = []
        if all_articles["status"] == "ok":
            for article_data in all_articles["articles"][0:3]:
                article_content = self.gather_web_page_data(article_data['url'])
                if(article_content["success"]):
                    article = Article(
                        title=article_data['title'],
                        url=article_data['url'],
                        author=article_data.get('author'),
                        source=article_data.get('source', {}).get('name'),
                        description=article_data.get('description'),
                        publishedAt=datetime.strptime(article_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') if article_data.get('publishedAt') else None,
                        content=article_content["data"]
                    )
                    articles_list.append(article.to_dict())
            return {"success": True, "articles": articles_list}
        return {"success": False, "articles": []}
    
if __name__ == "__main__":
    custom_newsapi = CustomNewsApiClient()

    # Get top headlines
    all_articles = custom_newsapi.get_all_articles_past_month(q='bitcoin')
    print(all_articles)