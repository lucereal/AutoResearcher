
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import os
from data_extraction_tools.web_page_reader import WebPageReader
from dataclasses import dataclass, field
from typing import Optional
from models.standard_article import ArticleContent, StandardArticle

@dataclass
class NewsApiArticle(StandardArticle):
    author: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    publishedAt: Optional[datetime] = None
    
    def to_dict(self):
        article_dict = super().to_dict()
        article_dict.update({
            "author": self.author,
            "source": self.source,
            "description": self.description,
            "publishedAt": self.publishedAt.isoformat() if self.publishedAt else None
        })
        return article_dict
    
class CustomNewsApiClient:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.client = NewsApiClient(api_key=self.api_key)
        self.web_reader = WebPageReader()

    def gather_web_page_data(self, url):
        data = self.web_reader.extract_content(url)
        return data
    
    def get_all_articles(self, q=None, sources=None, domains=None, from_param=None, to=None, language=None, sort_by=None, page=None, page_size=None):
        try:
            return self.client.get_everything(q=q, sources=sources, domains=domains, from_param=from_param, to=to, language=language, sort_by=sort_by,page_size=page_size, page=page)
        except Exception as e:
            print(f"An error occurred while fetching all articles: {e}")
            return None    

    def get_all_articles_past_month(self, q=None):
        try:
            to_param = datetime.now().strftime('%Y-%m-%d')
            from_param = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            all_articles =self.get_all_articles(q=q, from_param=from_param, to=to_param, language='en', sort_by='relevancy', page=1, page_size=10)
            if all_articles is None:
                return {"success": False, "articles": []}            
            articles_list = []
            if all_articles["status"] == "ok":
                for article_data in all_articles["articles"][0:3]:
                    article_content = self.gather_web_page_data(article_data['url'])
                    if(article_content["success"]):
                        article = NewsApiArticle(
                            title=article_data['title'],
                            url=article_data['url'],
                            author=article_data.get('author'),
                            source=article_data.get('source', {}).get('name'),
                            description=article_data.get('description'),
                            publishedAt=datetime.strptime(article_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') if article_data.get('publishedAt') else None,
                            content=ArticleContent.from_dict(article_content["data"])
                        )
                        articles_list.append(article.to_dict())
                return {"success": True, "articles": articles_list}
            return {"success": False, "articles": []}
        except Exception as e:
            print(f"An error occurred while fetching articles from the past month: {e}")
            return {"success": False, "articles": []}
    
if __name__ == "__main__":
    custom_newsapi = CustomNewsApiClient()

    # Get top headlines
    all_articles = custom_newsapi.get_all_articles_past_month(q='bitcoin')
    print(all_articles)