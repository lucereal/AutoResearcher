import json
from google_client import GoogleSearchClient
from openai_client import OpenAIClient
from web_page_reader import WebPageReader
from youtube_client import YouTubeClient

class DataGatherer:
    def __init__(self):
        self.google_client = GoogleSearchClient()
        self.openai_client = OpenAIClient()
        self.youtube_client = YouTubeClient()

    def gather_google_youtube_data(self, search_query):
        results = self.google_client.get_google_youtube_search_results(search_query)
        return results
    
    def gather_youtube_data(self, url):
        audio_file_json = self.youtube_client.download_audio_json(url)
        return audio_file_json
    
    def gather_google_data(self, search_query):
        results = self.google_client.get_google_search_results(search_query)
        return results

    def gather_queries_and_sources_youtube(self, user_topic):
        queryList = self.openai_client.create_queries_on_topic(user_topic)
        queries_and_sources = {"queries": queryList, "query_results": []}
        
        for query in queryList[:3]:
            google_results = self.gather_google_youtube_data(query)
            query_result = {"query": query, "google_results": google_results.to_dict()}
            queries_and_sources["query_results"].append(query_result)
        
        return queries_and_sources

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

    def gather_all_youtube_data(self, user_topic):
        print("\ngathering all data for user topic: ", user_topic)
        queries_and_sources = self.gather_queries_and_sources_youtube(user_topic)
        topic_sources_data = {"queries": queries_and_sources["queries"], "sources_data": []}

        for query_result in queries_and_sources["query_results"][0:1]:
            print("\tgetting sources data for query: ", query_result["query"])
            query_source_data = {"query": query_result["query"], "sources_data": []}
            for item in query_result["google_results"]["items"][0:1]:
                url = item["link"]
                print("\t\treading youtube data for url: ", url)
                audio_file_json = self.gather_youtube_data(url)
                audio_file_transcribed_chunks = self.openai_client.transcribe_audio_file_chunks(audio_file_json["chunks"])
                item_source_data = " ".join(audio_file_transcribed_chunks)
                item_data = {"link": url, "source_data": item_source_data }
                query_source_data["sources_data"].append(item_data)
            topic_sources_data["sources_data"].append(query_source_data)
        
        return topic_sources_data

    def gather_all_data(self, user_topic):
        print("\ngathering all data for user topic: ", user_topic)
        queries_and_sources = self.gather_queries_and_sources(user_topic)
        topic_sources_data = {"queries": queries_and_sources["queries"], "sources_data": []}

        for query_result in queries_and_sources["query_results"][0:2]:
            print("\tgetting sources data for query: ", query_result["query"])
            query_source_data = {"query": query_result["query"], "sources_data": []}
            for item in query_result["google_results"]["items"]:
                url = item["link"]
                print("\t\treading web page data for url: ", url)
                item_source_data = self.gather_web_page_data(url)
                if(item_source_data["success"] == True):
                    item_data = {"link": url, "source_data": item_source_data["data"] }
                    query_source_data["sources_data"].append(item_data)
                else:
                    print("\t\tError reading web page data for url: ", url)
            topic_sources_data["sources_data"].append(query_source_data)
        
        return topic_sources_data
    
    def gather_data_and_summarize_sources(self, user_topic):
        print(f"\nGathering data and summarizing sources for topic: {user_topic}")

        data = self.gather_all_data(user_topic)
        for query_sources in data["sources_data"]:
                print("\tSummarizing sources for query: " + query_sources["query"])
                for item in query_sources["sources_data"]:
                    web_page_data = item["source_data"]
                    # print("\t\tchecking if " + item["link"] + " is usable")
                    # Call the is_web_page_data_usable function
                    is_usable = self.openai_client.is_web_page_data_usable(web_page_data, user_topic)
                    print("\t\t" + item["link"] + " is usable: " + str(is_usable))
                    item["isUsable"] = is_usable
                    if is_usable:
                        # Call the summarize_web_page_data function
                        summary = self.openai_client.summarize_web_page_data(web_page_data, user_topic)
                        item["summary"] = summary
                        print("\t\tsummary: " + summary.replace('\n\n', ' ').replace('\n', ' ')[:200]+"...")
        return data

    def gather_youtube_data_and_summarize(self, user_topic):
        print(f"\nGathering data and summarizing sources for topic: {user_topic}")

        data = self.gather_all_youtube_data(user_topic)
        for query_sources in data["sources_data"]:
                print("\tSummarizing sources for query: " + query_sources["query"])
                for item in query_sources["sources_data"]:
                    youtube_transcript = item["source_data"]
                    # print("\t\tchecking if " + item["link"] + " is usable")
                    # Call the is_web_page_data_usable function

                    # i don't want to check if the youtube data is usable
                    # because its so much data. i should combine the usablity check and the summarization
                    # into one openai call with a structured output

                    # Call the summarize_web_page_data function
                    summary = self.openai_client.summarize_youtube_data(youtube_transcript, user_topic)
                    item["summary"] = summary
                    print("\t\tsummary: " + summary.replace('\n\n', ' ').replace('\n', ' ')[:200]+"...")
    
        return data

# Example usage:
if __name__ == "__main__":
    data_gatherer = DataGatherer()
    user_topic = "fantasy football advice"
    
    all_data = data_gatherer.gather_youtube_data_and_summarize(user_topic)
    print(all_data)
    # all_data = data_gatherer.gather_data_and_summarize_sources(user_topic)
    # # Save the results to a JSON file
    file_name = user_topic.replace(" ", "_") + "_results_with_summaries.json"
    with open("results/"+file_name, "w") as json_file:
        json.dump(all_data, json_file, indent=2)

    # all_data = data_gatherer.gather_all_data(user_topic)
    # # Save the results to a JSON file
    # with open("results/"+"results.json", "w") as json_file:
    #     json.dump(all_data, json_file, indent=2)
    
    print("Results have been saved to " + file_name)