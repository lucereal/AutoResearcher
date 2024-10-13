import json
from google_client import GoogleSearchClient
from openai_client import OpenAIClient

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

    def gather_all_data(self, user_topic):
        queryList = self.openai_client.create_queries_on_topic(user_topic)
        all_data = {"queries": queryList, "query_results": []}
        
        for query in queryList[:3]:
            google_results = self.gather_google_data(query)
            query_result = {"query": query, "google_results": google_results}
            all_data["query_results"].append(query_result)
        
        return all_data

# Example usage:
if __name__ == "__main__":
    data_gatherer = DataGatherer()
    user_topic = "cryptocurrency trading"
    
    all_data = data_gatherer.gather_all_data(user_topic)
    print(json.dumps(all_data, indent=2))