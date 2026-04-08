import feedparser
import json
import os
import urllib.parse
from datetime import datetime

# --- Configuration ---
NEWS_FILE = "src/data/news.json"

FEEDS = {
    "Bee Culture": {"url": "https://beeculture.com/feed/", "category": "Global"},
    "BeeLife EU": {"url": "https://www.bee-life.eu/blog-feed.xml", "category": "Global"},
    "Radio Warroza": {"url": "https://castopod.warroza.pl/@radiowarroza/feed.xml", "category": "Local"}
}

GOOGLE_NEWS_QUERIES = [
    {"q": "pszczelarstwo Wołomin", "label": "Local Alert"},
    {"q": "cena miodu 2026", "label": "Market"}
]

def clean_summary(html_text):
    """Simple helper to remove HTML tags and truncate."""
    from re import sub
    if not html_text:
        return ""
    clean = sub('<[^<]+?>', '', html_text)
    return clean[:180] + "..." if len(clean) > 180 else clean

def fetch_news():
    all_news = []

    # 1. Fetch RSS Feeds
    for source, info in FEEDS.items():
        print(f"Fetching {source}...")
        feed = feedparser.parse(info["url"])
        for entry in feed.entries[:3]:
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "source": source,
                "category": info["category"],
                "summary": clean_summary(entry.get("summary", entry.get("description", ""))),
                "date": entry.get("published", datetime.now().strftime("%Y-%m-%d"))
            })

    # 2. Fetch Google News RSS Proxy
    for item in GOOGLE_NEWS_QUERIES:
        print(f"Fetching Google News: {item['q']}...")
        query = urllib.parse.quote(item["q"])
        url = f"https://news.google.com/rss/search?q={query}&hl=pl&gl=PL&ceid=PL:pl"
        feed = feedparser.parse(url)
        for entry in feed.entries[:2]:
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "source": f"Google News ({item['label']})",
                "category": "Local",
                "summary": "",  # Google News RSS usually doesn't have good summaries
                "date": entry.get("published", datetime.now().strftime("%Y-%m-%d"))
            })

    # 3. Save to JSON
    os.makedirs(os.path.dirname(NEWS_FILE), exist_ok=True)
    with open(NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully updated news. Total articles: {len(all_news)}")

if __name__ == "__main__":
    fetch_news()
