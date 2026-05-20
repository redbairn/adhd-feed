import feedparser
import json
import os
import socket
from urllib.parse import urlparse

# Define structured paths relative to the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEEDS_FILE = os.path.join(BASE_DIR, "feeds.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "feed.json")

def load_feed_urls():
    """Reads URLs from feeds.txt, cleans whitespace, and ignores comments (#)"""
    if not os.path.exists(FEEDS_FILE):
        print(f"⚠️ {FEEDS_FILE} not found! Using default empty list.")
        return []
    
    with open(FEEDS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def is_valid_url(url):
    """Ensures the string is a strictly formed HTTP/HTTPS web address"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def fetch_all_feeds():
    feed_urls = load_feed_urls()
    combined_entries = []
    
    print(f"🎯 Loaded {len(feed_urls)} sources from feeds.txt")
    
    # Set a strict global timeout (10 seconds) so slow or malicious servers
    # cannot hang your background Pi runner process indefinitely
    socket.setdefaulttimeout(10)
    
    for url in feed_urls:
        # Security Gate 1: Drop malformed strings or local file paths immediately
        if not is_valid_url(url):
            print(f"⚠️ Security Skip: Malicious or invalid URL layout ignored -> {url}")
            continue
            
        print(f"🔄 Scraping: {url}")
        
        try:
            feed = feedparser.parse(url)
            
            # Security Gate 2: Check if the parser encountered XML corruption errors
            if feed.bozo:
                print(f"⚠️ Processing Alert: Malformed XML structure at {url}. Attempting to parse anyway...")
                
            source_title = feed.feed.get("title", "Unknown Source")
            
            for entry in feed.entries:
                raw_date = entry.get("published", entry.get("updated", ""))
                formatted_date = raw_date if raw_date else "Recent"

                combined_entries.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", "#"),
                    "source": source_title,
                    "date": formatted_date
                })
        except Exception as e:
            # Security Gate 3: Catch networking/timeout errors gracefully without crashing the pipeline
            print(f"❌ Error processing {url}: {e}")
            
    # Save the sanitized payload
    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined_entries, f, indent=4)
        
    print(f"✅ Successfully saved {len(combined_entries)} items to feed.json")

if __name__ == "__main__":
    fetch_all_feeds()
