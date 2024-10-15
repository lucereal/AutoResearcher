# AutoResearcher :robot:
Automated Data Collection with GPT, Google Custom Search, and Web Scraping

This Python project automates data collection on user provided topics. 

## Features

- **Query Generation**: GPT creates relevant search queries.
- **Search & Scraping**: Uses Google Custom Search API, Playwright, and BeautifulSoup to fetch and extract web content.
- **Summarization**: GPT summarizes scraped data into concise reports.
- **End-to-End Automation**: Fully automated from input to summarized output.

## Technologies

- **Python**, **OpenAI API**, **Google Custom Search API**
- **Playwright**, **BeautifulSoup**

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
    ```

4. **Run the script**:
    ```bash
    python main.py --topic "Your topic here"
    ```

## Usage

1. Input a topic.
2. GPT generates search queries.
3. Google Custom Search retrieves results.
4. Playwright & BeautifulSoup scrape web pages.
5. GPT summarizes the scraped content.

## Future Enhancements

- Support for more search engines.
- Advanced query generation and filtering.
- Customizable summarization options.
- Video summaries
  

