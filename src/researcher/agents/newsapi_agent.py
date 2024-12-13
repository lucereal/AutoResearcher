import json
import asyncio
from researcher.data_source_clients.google_client import GoogleSearchClient
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_extraction_tools.web_page_reader import WebPageReader
from researcher.data_source_clients.youtube_client import YouTubeClient
from researcher.data_source_clients.newsapi_client import CustomNewsApiClient
from researcher.services.newsapi_service import NewsApiService



class NewsApiAgent:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.newsapi_service = NewsApiService()

    async def gather_newsapi_articles(self, search_query, articles_to_pull=1):
        results = await self.newsapi_service.fetch_articles(search_query, articles_to_pull)
        return results
    
    async def generate_search_phrases(self, user_topic):
        return await self.openai_client.create_phrases_on_topic(user_topic)
    
    async def gather_news_api_data(self, user_topic, topic_phrases=None, articles_to_pull=1):
       
        results = []
        truncated_topic = user_topic[:500]
        user_topic_articles = await self.gather_newsapi_articles(truncated_topic, articles_to_pull)
        if user_topic_articles["success"]:
            user_topic_articles_results = {"query": truncated_topic, "results": user_topic_articles["articles"]}
            results.append(user_topic_articles_results)

        for phrase in topic_phrases:
            phrase_articles = await self.gather_newsapi_articles(phrase, articles_to_pull)
            if phrase_articles["success"]:
                phrase_result = {"query": phrase, "results": phrase_articles["articles"]}
                results.append(phrase_result)
        
        return results
    
    async def summarize_news_data(self, user_topic, news_data):
        executive_summary = await self.openai_client.executive_summary_web_page_data(news_data["content"], user_topic)
        news_data["executive_summary"] = executive_summary
        # bullet_points = await self.openai_client.bulletpoint_web_page_data(news_data["content"], user_topic)
        # news_data["bullet_points"] = bullet_points
        # key_figures = await self.openai_client.key_figures_web_page_data(news_data["content"], user_topic)
        # news_data["key_figures"] = key_figures
        return news_data

        
    async def gather_topic_summarization(self, user_topic, num_phrases=1, num_articles=1):
        print(f"\nGathering data and summarizing sources for topic: {user_topic}")

        phrase_list = await self.generate_search_phrases(user_topic)

        phrase_results = await self.gather_news_api_data(user_topic, phrase_list[0:num_phrases], num_articles)

        topic_result = {"queries": [], "phrases": phrase_list, "phrase_results": []}
        for result in phrase_results:
                print("\tSummarizing sources for query: " + result["query"])
                for item in result["results"][0:num_articles]:
                    result_data = await self.summarize_news_data(user_topic, item)
                            
        topic_result["phrase_results"] = phrase_results
        return topic_result
    


# Example usage:
async def main():
    newsapi_agent = NewsApiAgent()
    user_topic = "Virtual Reality in Education"
    file_name = user_topic.replace(" ", "_") + "_results_with_summaries.json"
    print("in data_gatherer main")
    result = await newsapi_agent.gather_topic_summarization(user_topic, 1,5)
    with open("results/"+file_name, "w") as json_file:
        json.dump(result, json_file, indent=2)

    print("Results have been saved to " + file_name)
    #print(result)

if __name__ == "__main__":
    asyncio.run(main())