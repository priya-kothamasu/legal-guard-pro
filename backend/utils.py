import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    try:
        # Standard browser headers to bypass basic bot blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Clean the page of non-textual data
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.extract()

        text = soup.get_text()
        
        # Professional whitespace cleaning
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return clean_text
    except Exception as e:
        print(f"Scraping Error: {e}")
        return ""