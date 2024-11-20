# src/newsapi_service.py
import asyncio
from researcher.data_source_clients.newsapi_client import CustomNewsApiClient
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_extraction_tools.web_page_reader import WebPageReader

class NewsApiService:
    def __init__(self):
        self.newsapi_client = CustomNewsApiClient()
        self.openai_client = OpenAIClient()
        self.web_reader = WebPageReader()
        self.article_pull_limit = 2

    async def fetch_and_check_usability(self, query):
        # Fetch articles from NewsAPI
        articles_result = self.newsapi_client.get_all_articles_day_range(query)
        
        if not articles_result["success"]:
            return {"success": False, "message": "Failed to fetch articles from NewsAPI"}

        articles = articles_result["articles"]

        # Process articles using OpenAI
        processed_articles = []
        for article in articles:
            article_preview = {"title": article["title"], "description": article["description"], "rawContent": article["rawContent"]}
            is_usable = await self.openai_client.is_news_article_preview_usable(article_preview, query)
            if is_usable:
                processed_articles.append(article)
        return {"success": True, "articles": processed_articles}
    
    async def scrape_article_content(self, url):
        return await self.web_reader.extract_content(url)

    async def fetch_articles(self, query):
        try:
            article_list = await self.fetch_and_check_usability(query)
            result_article_list = []
            if article_list["success"] == True:
                for article in article_list["articles"][0:self.article_pull_limit]:
                    article_content = await self.scrape_article_content(article["url"])
                    article["content"] = article_content
                    result_article_list.append(article)
                return {"success": True, "articles": result_article_list}
            else:
                return {"success": False, "articles": []}
        except Exception as e:
            print(f"An error occurred while fetching articles: {e}")
            return {"success": False, "articles": []}

async def main():
    service = NewsApiService()
    query = "trending in music industry"
    result = await service.fetch_and_check_usability(query)
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 