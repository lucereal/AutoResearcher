# AutoResearcher :robot:
Automated Data Collection with LLM, Google Custom Search, Video Transcription, and Web Scraping

This Python project automates data collection on user provided topics. 

## Features

1. **Query Generation**: LLM creates relevant search queries.
2. **Data Collection**: NewsApi, YouTube, and Google Search to collect data on specific topics.
3. **Data Scraping**: Uses Playwright and BeautifulSoup to fetch and extract web content. Uses MoviePy to extract audio data from videos. Uses OpenAI Whisper Model to create audio transcriptions.
4. **Summarization**: LLM summarizes scraped data into concise reports.
5. **End-to-End Automation**: Fully automated from input to summarized output.
6. **Instagram Integration**:
    - Read a user's Instagram.
    - Process pictures using OpenAI vision.
    - Create an object-weighted graph based on object occurrences in the pictures.
    - Summarize picture settings and subjects.
    - Summarize the user's Instagram in total.

## Features

1. **Data Gathering**:
    - Gather data from news, Google, YouTube, and Instagram.
    - Use Playwright and BeautifulSoup for web scraping.
    - Use MoviePY for video transcription.

2. **Data Processing**:
    - Summarize scraped content using advanced language models including OpenAI Text Generation model.
    - Generate search queries based on input topics.

3. **Instagram Integration**:
    - Read a user's Instagram.
    - Process pictures using OpenAI vision.
    - Create an object-weighted graph based on object occurrences in the pictures.
    - Summarize picture settings and subjects.
    - Summarize the user's Instagram in total.


## Technologies

- **Python**, **OpenAI API**, **Google Custom Search API**
- **Playwright**, **BeautifulSoup**, **MoviePy**, **NewsAPI**
- **InstagramAPI**, **NetworkX**

## Setup

1. **Clone the repo**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up API keys**:  
   Create a `.env` file with:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_CUSTOM_SEARCH_API_KEY=your_google_custom_search_api_key
    GOOGLE_CX=your_google_cse_id
    NEWS_API_KEY=newsapi_key
    INSTAGRAM_CLIENT_ID=insagram_client_id
    INSTAGRAM_CLIENT_SECRET=insagram_client_secret
    INSTAGRAM_REDIRECT_URI=instagram_redirect_uri
    INSTAGRAM_ACCESS_CODE=insagram_access_code
    ```

4. **Run the script**:
    Currently only the "news" source is supported. 
    ```bash
    python src/researcher/main.py --topic "Your topic here" --source "[news, google, youtube, all]"
    ```

5. **Check Results Folder**:
    Find result json file in results folder

## Usage

1. Input a topic.
2. LLM generates search queries.
3. Data source retrieves results.
4. MoviePY transcribes video or Playwright & BeautifulSoup scrapes web pages.
5. LLM summarizes the scraped content.

## Future Enhancements

- Support for more search engines.
- Advanced query generation and filtering.
- Customizable summarization options.
- Add UI for visualizing results 
- Add subscription features for users to get updates on a schedule
  
## Needed Improvements

- Web page scraping in web_page_reader.py
- More abstract data_gatherer.py class 
- Chunking in openAI requests for large text especially in video summarization
- Potentially increase performance by decreasing run time?
- Add SerpApi
- Reduce number of LLM calls and increase relevancy of sumary data