import json
from google_client import GoogleSearchClient
from openai_client import OpenAIClient
from web_page_reader import WebPageReader

class DataGatherer:
    def __init__(self):
        self.google_client = GoogleSearchClient()
        self.openai_client = OpenAIClient()

    def gather_google_data(self, search_query):
        results = self.google_client.get_google_search_results(search_query)
        return results

    def gather_openai_data(self, user_topic):
        response = self.openai_client.create_queries_on_topic(user_topic)
        return response

    def gather_queries_and_sources(self, user_topic):
        queryList = self.openai_client.create_queries_on_topic(user_topic)
        queries_and_sources = {"queries": queryList, "query_results": []}
        
        for query in queryList[:3]:
            google_results = self.gather_google_data(query)
            query_result = {"query": query, "google_results": google_results.to_dict()}
            queries_and_sources["query_results"].append(query_result)
        
        return queries_and_sources

    def gather_web_page_data(self, url):
        reader = WebPageReader()
        data = reader.extract_important_data(url)
        return data

    def gather_all_data(self, user_topic):
        print("\ngathering all data for user topic: ", user_topic)
        queries_and_sources = self.gather_queries_and_sources(user_topic)
        topic_sources_data = {"queries": queries_and_sources["queries"], "sources_data": []}

        for query_result in queries_and_sources["query_results"][0:1]:
            print("\tgetting sources data for query: ", query_result["query"])
            query_source_data = {"query": query_result["query"], "sources_data": []}
            for item in query_result["google_results"]["items"]:
                url = item["link"]
                print("\t\treading web page data for url: ", url)
                item_source_data = self.gather_web_page_data(url)
                item_data = {"link": url, "source_data": item_source_data }
                query_source_data["sources_data"].append(item_data)
            topic_sources_data["sources_data"].append(query_source_data)
        
        return topic_sources_data
    
# Example usage:
if __name__ == "__main__":
    data_gatherer = DataGatherer()
    user_topic = "cryptocurrency trading"
    
    all_data = data_gatherer.gather_all_data(user_topic)
    # Save the results to a JSON file
    with open("results.json", "w") as json_file:
        json.dump(all_data, json_file, indent=2)
    
    print("Results have been saved to results.json")