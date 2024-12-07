import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


class WebPageReader:
    def __init__(self):
        pass

    def handle_page_error(error):
        print(f"JavaScript error on page: {error}")

    async def read_web_page(self, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            #page = browser.new_page()
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            # context = browser.new_context(
            #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            #     ignore_https_errors=True,
            #     bypass_csp=True,
            #     extra_http_headers={"Upgrade-Insecure-Requests": "1"}
            # )
            page = await context.new_page()

            await stealth_async(page)

            # page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            try:
                # page.on('pageerror', self.handle_page_error)
                await page.goto(url, timeout=60000)  # Set a timeout of 60 seconds
                await page.wait_for_load_state('networkidle')  # Wait for the network to be idle

                # Handle "accept cookies" pop-up
                try:
                    accept_button = await page.query_selector("button:has-text('Accept')")
                    if accept_button:
                        if await accept_button.is_visible():
                            await accept_button.click()
                            await page.wait_for_timeout(2000)  # Wait for 2 seconds to allow the pop-up to close
                except Exception as e:
                    print(f"Error handling cookies pop-up: {e}")

                content = await page.content()


                # Handle case where captcha appears and do not use that source
                # if "captcha" in content.lower():
                #     print("Captcha detected, skipping this source.")
                #     browser.close()
                #     return None

            except Exception as e:
                print(f"Error navigating to {url}: {e}")
                await browser.close()
                return None


            await browser.close()
        soup = BeautifulSoup(content, 'html.parser')
        return soup

    async def extract_content(self, url):
        soup = await self.read_web_page(url)
        if soup is None:
            return {
                "success": False,
                "data": "couldn't read web page"
            }
        
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
            
            return {
                "success": True,
                "data": {
                    "text_content": text_content,
                    "table_data": table_data
                }
            }
        else:
            return {
                "success": False,
                "data": "No body tag found"
            }                    
    
    async def prettify_web_page(self, url):
        soup = await self.read_web_page(url)
        if soup:
            return soup.prettify()
        return "CAPTCHA detected, skipping this URL."
    
# Example usage:

async def main():
    reader = WebPageReader()
    # url = 'https://www.coingecko.com/en/highlights/high-volume'
    url = 'https://explodingtopics.com/blog/cryptocurrency-trends'
    #url = 'https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2023-generative-ais-breakout-year'
    result = await reader.extract_content(url)
    if result["success"]:
        print("Page data extracted successfully:")
        print(result["data"])
    else:
        print("Failed to extract page data:")
        print(result["data"])

if __name__ == "__main__":
    asyncio.run(main())