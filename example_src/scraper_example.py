
from logging import PlaceHolder
import os, time, sys
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')
espn_key = os.environ.get('ESPN_KEY')

import re
from playwright.sync_api import Page, expect, TimeoutError 
from bs4 import BeautifulSoup
from langchain.llms import OpenAI 
import json 

MAX_MONTHS = 3
MAX_AVAILABILITY_COUNT = 3

# test code
#llm = OpenAI(openai_api_key=api_key, temperature=0.9)
#x = llm(prompt='What would be a good company name for a company that makes colorful socks?')
#print(x)

#TODO: move console logging to text

from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    # set a default for testing
    user = "lucerodavid1010@gmail.com"
    pwd = ""
    url = "https://www.espn.com/fantasy/"
    statsUrl = "https://www.espn.com/nfl/stats/player"
    
    page.goto(statsUrl)
    try:
        
        #    page.frame_locator("iframe").locator("div").filter(has_text=re.compile(r"^Email \*$")).click()
        clocator = page.locator('#fittPageContainer')
        dlocator = clocator.locator('.dropdown.dropdown--md.mr3.mt2.mb3.filters__seasonDropdown')
        slocator = dlocator.locator('select.dropdown__select').nth(0)
        #slocator.select_option(value='2020|3')
        options = slocator.locator('option').evaluate_all('nodes => nodes.map(n => n.value)')

        all_data = []
        pageIndex = 0
        for option_value in options:
                    # Set the dropdown value
            slocator.select_option(value=option_value)
            
            # Wait for the page to load its content after selecting an option (adjust timeout as needed)
            page.wait_for_timeout(2000)  # Waiting for 2 seconds as an example
                       
            showMoreCount = 0
            while True:
                if page.is_visible('.AnchorLink.loadMore__link'):                   
                    showMore = page.locator('.AnchorLink.loadMore__link')
                    showMore.click()
                    page.wait_for_timeout(1000)
                    
                    showMoreCount += 1
                    if showMoreCount > 1:
                        break
                else:
                    break
   
            x = page.inner_html('.ResponsiveTable')    
            all_data.append(x)
            # Get the page content
            # content = page.content()
            
            
            if pageIndex > 2: 
                break
            pageIndex+=1
            
            # Use BeautifulSoup to parse and scrape data
            # soup = BeautifulSoup(content, 'html.parser')
            # # Extract data here based on your scraping logic. As an example, I'm just storing the page title:
            # all_data.append(soup.title.string)
       
        
        # x = page.inner_html('.ResponsiveTable')
        # soup = BeautifulSoup(x, "html.parser")
        
        for x in all_data:
            soup = BeautifulSoup(x, "html.parser")
            tables = soup.findChildren('table')
            playerTable = tables[0]
            statsTable = tables[1]
            
            player_dict = {}
        
            # - get players from first table
            players = playerTable.findChildren(['tr'])
            for player in players[1:]:
                pIndex = player.get('data-idx')
                pd = player.findChildren('td')
                pRank = pd[0].text
                pName = pd[1].findChildren('a')[0].text
                pTeam = pd[1].findChildren('span')[0].text
                player_dict[pIndex] = [pRank,pName,pTeam]
                
            # - get stats for each player from second table
            stats = statsTable.findChildren('tr')
            for stat in stats[1:]:          
                sIndex = stat.get('data-idx')          
                sdi = [i.text for i in stat.findChildren('td')]
                for sdix in sdi:
                    player_dict[sIndex].append(sdix)
         
    except Exception as error:
        print("An exception occurred:", error) # An exception occurred: division by zero
        
    # Keep the browser open for a few seconds to observe the result.
    # You can adjust this or remove it based on your needs.
    page.wait_for_timeout(5000)

    # Close the browser
    browser.close()
    
    
    

with sync_playwright() as playwright:
    run(playwright)

#url = "https://www.espn.com/fantasy/"
#select login then enter credentials
# login_button = page.wait_for_selector("text=Log In", timeout=10000)
# if login_button:
#     login_button.click()
#     page.wait_for_timeout(2000)
#     frame = page.frame(name="oneid-iframe")
#     if frame:
#         frame.locator("#InputIdentityFlowValue").fill(user)
#         frame.locator("#BtnSubmit").click()
#         page.wait_for_timeout(1000)
#         frame.locator("#InputPassword").fill(pwd)
#         frame.locator("#BtnSubmit").click()
#     else:
#         print("Could not find email address form")

# else:
#     print("Login button not found.")

# expect(page.get_by_role("heading", name="Sign up")).to_be_visible()

# page.get_by_role("checkbox", name="Subscribe").check()


#
# values = [
#     "2023|2", "2022|3", "2022|2", "2021|3", "2021|2", "2020|3", "2020|2", 
#     "2019|3", "2019|2", "2018|3", "2018|2", "2017|3", "2017|2", "2016|3", 
#     "2016|2", "2015|3", "2015|2", "2014|3", "2014|2", "2013|3", "2013|2", 
#     "2012|3", "2012|2", "2011|3", "2011|2", "2010|3", "2010|2", "2009|3", 
#     "2009|2", "2008|3", "2008|2", "2007|3", "2007|2", "2006|3", "2006|2", 
#     "2005|3", "2005|2", "2004|3", "2004|2"
# ]
