from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup


# Headers to use for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/134.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
}


def fetch_google_news_rss(query, max_results=50):
    try:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, "lxml-xml")
        items = soup.find_all("item")[:max_results]

        news_list = []
        for item in items:
            news_list.append({
                "title": item.title.text if item.title else "No title",
                "link": item.link.text if item.link else "#",
                "published": item.pubDate.text if item.pubDate else "No date",
                "source": item.source.text if item.source else "Unknown source"
            })
        return news_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google News RSS: {e}")
        return []

def get_content_from_link(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]

        if not paragraphs:
            return "No readable content found."

        return " ".join(paragraphs[:10])  # Get content from the first 10 paragraphs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from link {url}: {e}")
        return "Could not fetch content."
    except Exception as e:
        print(f"An unexpected error occurred while scraping {url}: {e}")
        return "Could not fetch content."
