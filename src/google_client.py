import os
from dotenv import load_dotenv
import requests
import json
from standard_article import ArticleContent, StandardArticle
from web_page_reader import WebPageReader

# Load environment variables from .env file
load_dotenv()

class GoogleSearchClient():
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.api_cx = os.getenv("GOOGLE_CX")
        self.api_url = "https://www.googleapis.com/customsearch/v1"
        self.web_reader = WebPageReader()

    def get_request_url(self, query):

        #currently can't filter out more than one site at a time
        #google search api kinda of sucks
        filterSites = "youtube.com"  # Filter out YouTube results
        return f"{self.api_url}?key={self.api_key}&cx={self.api_cx}&q={query}&dateRestrict=m1&siteSearch={filterSites}&siteSearchFilter=e"

    def get_request_url_with_youtube(self, query):

        #currently can't filter out more than one site at a time
        #google search api kinda of sucks
        filterSites = "youtube.com"  # Filter out YouTube results
        return f"{self.api_url}?key={self.api_key}&cx={self.api_cx}&q={query}&dateRestrict=m1&siteSearch={filterSites}&siteSearchFilter=i"

    def get_google_search_results(self, query):
        request_url = self.get_request_url(query)
        response = requests.get(request_url)
        response.raise_for_status()
        
        return GoogleSearchResult.from_json(response.json())
    
    def get_search_result_articles(self, query):
        try:
            request_url = self.get_request_url(query)
            response = requests.get(request_url)
            response.raise_for_status()
            googleSearchResult = GoogleSearchResult.from_json(response.json()) 
            articles = []
            for item in googleSearchResult.items[0:3]:
                article_content = self.web_reader.extract_content(item.link)
                if(article_content["success"]):
                    article = StandardArticle(
                        title=item.title,
                        url=item.link,
                        content=ArticleContent.from_dict(article_content["data"])
                    )
                    articles.append(article.to_dict())
            return {"success": True, "articles": articles}
        except Exception as e:
            print(f"An error occurred while fetching Google search results: {e}")
            return {"success": False, "articles": []}
        
    def get_google_youtube_search_results(self, query):
        request_url = self.get_request_url_with_youtube(query)
        response = requests.get(request_url)
        response.raise_for_status()
        
        return GoogleSearchResult.from_json(response.json())


class GoogleSearchResult:
    def __init__(self, url, items):
        self.url = url
        self.items = items

    @classmethod
    def from_json(cls, json_data):
        url = json_data.get("url", "")
        items = [GoogleSearchItem.from_json(item) for item in json_data.get("items", [])]
        return cls(url, items)
    
    def print_items(self):
        for item in self.items:
            print(f"Title: {item.title}")
            print(f"Link: {item.link}")
            print(f"Snippet: {item.snippet}")
            print(f"Display Link: {item.displayLink}")
            print(f"Formatted URL: {item.formattedUrl}")
            print(f"HTML Title: {item.htmlTitle}")
            print(f"HTML Snippet: {item.htmlSnippet}")
            print(f"HTML Formatted URL: {item.htmlFormattedUrl}")
            # print(f"PageMap: {json.dumps(item.pagemap, indent=2)}")
            print("-" * 40) 
    
    def to_dict(self):
        return {
            "url": self.url,
            "items": [item.to_dict() for item in self.items]
        }   

class GoogleSearchItem:
    def __init__(self, kind, title, htmlTitle, link, displayLink, snippet, htmlSnippet, formattedUrl, htmlFormattedUrl):
        self.kind = kind
        self.title = title
        self.htmlTitle = htmlTitle
        self.link = link
        self.displayLink = displayLink
        self.snippet = snippet
        self.htmlSnippet = htmlSnippet
        self.formattedUrl = formattedUrl
        self.htmlFormattedUrl = htmlFormattedUrl
        # self.pagemap = pagemap

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("kind", ""),
            json_data.get("title", ""),
            json_data.get("htmlTitle", ""),
            json_data.get("link", ""),
            json_data.get("displayLink", ""),
            json_data.get("snippet", ""),
            json_data.get("htmlSnippet", ""),
            json_data.get("formattedUrl", ""),
            json_data.get("htmlFormattedUrl", ""),
            # json_data.get("pagemap", {})
        )
    
    def to_dict(self):
        return {
            "kind": self.kind,
            "title": self.title,
            "htmlTitle": self.htmlTitle,
            "link": self.link,
            "displayLink": self.displayLink,
            "snippet": self.snippet,
            "htmlSnippet": self.htmlSnippet,
            "formattedUrl": self.formattedUrl,
            "htmlFormattedUrl": self.htmlFormattedUrl
            # "pagemap": self.pagemap.to_dict() if self.pagemap else {}
        }
    
if __name__ == "__main__":
    # Example usage:
    client = GoogleSearchClient()
    results = client.get_search_result_articles("find the best restaurant in San Francisco")
    # results.print_items()
    print(json.dumps(results, indent=2))