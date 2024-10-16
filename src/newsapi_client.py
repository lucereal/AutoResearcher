
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import os

class CustomNewsApiClient:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.client = NewsApiClient(api_key=self.api_key)

    def get_news_api_results(self, q=None, sources=None, category=None, language=None, country=None):
        return self.client.get_top_headlines(q=q, sources=sources, category=category, language=language, country=country)
    
    def get_all_articles(self, q=None, sources=None, domains=None, from_param=None, to=None, language=None, sort_by=None, page=None, page_size=None):
        return self.client.get_everything(q=q, sources=sources, domains=domains, from_param=from_param, to=to, language=language, sort_by=sort_by,page_size=page_size, page=page)
    
    def get_all_articles_past_month(self, q=None):
        
        to_param = datetime.now().strftime('%Y-%m-%d')
        from_param = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        all_articles =custom_newsapi.get_all_articles(q=q, from_param=from_param, to=to_param, language='en', sort_by='relevancy', page=1, page_size=10)
        return all_articles
    
if __name__ == "__main__":
    custom_newsapi = CustomNewsApiClient()

    # Get top headlines
    all_articles = custom_newsapi.get_all_articles_past_month(q='bitcoin')
    print(all_articles)