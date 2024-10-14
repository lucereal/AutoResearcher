import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


class WebPageReader:
    def __init__(self):
        pass

    def read_web_page(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            stealth_sync(page)
            page.goto(url)
            page.wait_for_timeout(2000)  # Wait for 10 seconds to allow verification to complete
            content = page.content()
            browser.close()
            #need to handle case where captcha appears and to not use that source
            # if "captcha" in content.lower():
            #     return None
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    def extract_important_data(self, url):
        soup = self.read_web_page(url)
        if soup is None:
            return "CAPTCHA detected, skipping this URL."
        
        # Extract content within the <body> tag
        body = soup.body
        if body:
            # Remove script and style tags
            for script_or_style in body(["script", "style"]):
                script_or_style.decompose()
             # Extract text content from specific tags
            text_content = ''
            for tag in body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text_content += tag.get_text(separator=' ', strip=True) + '\n'
            
            # Extract table data
            tables = body.find_all("table")
            table_data = []
            for table in tables:
                table_rows = []
                for row in table.find_all("tr"):
                    row_data = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                    table_rows.append(row_data)
                table_data.append(table_rows)
            
            return {"text": text_content.strip(), "tables": table_data}
        
        return "No body content found."
    
    def prettify_web_page(self, url):
        soup = self.read_web_page(url)
        if soup:
            return soup.prettify()
        return "CAPTCHA detected, skipping this URL."

# Example usage:
if __name__ == "__main__":
    reader = WebPageReader()
    # url = 'https://www.coingecko.com/en/highlights/high-volume'
    url = 'https://explodingtopics.com/blog/cryptocurrency-trends'
    htlmResult = reader.extract_important_data(url)
    print(htlmResult)