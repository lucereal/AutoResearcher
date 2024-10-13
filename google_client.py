import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()

class GoogleSearchClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.api_cx = os.getenv("GOOGLE_CX")
        self.api_url = "https://www.googleapis.com/customsearch/v1"

    def get_request_url(self, query):
        return f"{self.api_url}?key={self.api_key}&cx={self.api_cx}&q={query}"

    def get_google_search_results(self, query):
        request_url = self.get_request_url(query)
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()

# Example usage:
client = GoogleSearchClient()
results = client.get_google_search_results("find the best restaurant in San Francisco")
print(json.dumps(results, indent=2))