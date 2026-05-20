import feedparser
import json
import os
import socket
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDS_FILE = os.path.join(BASE_DIR, "feeds.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "feed.json")

def load_feed_urls():
    if not os.path.exists(FEEDS_FILE):
        print(f"⚠️ {FEEDS_FILE} not found! Using default empty list.")
        return []
    with open(FEEDS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def fetch_all_feeds():
    feed_urls = load_feed_urls()
    combined_entries = []
    
    print(f"🎯 Loaded {len(feed_urls)} sources from feeds.txt")
    socket.setdefaulttimeout(10)
    
    for url in feed_urls:
        if not is_valid_url(url):
            print(f"⚠️ Security Skip: Malicious or invalid URL layout ignored -> {url}")
            continue
            
        print(f"🔄 Scraping: {url}")
        
        try:
            feed = feedparser.parse(url)
            source_title = feed.feed.get("title", "Unknown Source")
            
            for entry in feed.entries:
                raw_date = entry.get("published", entry.get("updated", ""))
                formatted_date = raw_date if raw_date else "Recent"
                
                # Safely capture the author name, fallback to "Anonymous" if blank
                author_name = entry.get("author", entry.get("author_detail", {}).get("name", "Anonymous"))

                combined_entries.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "#"),
                    "source": source_title,
                    "date": formatted_date,
                    "author": author_name
                })
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            
    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined_entries, f, indent=4)
        
    print(f"✅ Successfully saved {len(combined_entries)} items to feed.json")

if __name__ == "__main__":
    fetch_all_feeds()
