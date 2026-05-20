import feedparser
import json
import os

FEED_URLS = [
    "https://www.reddit.com/r/ADHD/.rss",
    "https://www.additudemag.com/feed/",
    "https://adhddd.com/feed/"
]

def fetch_all_feeds():
    combined_entries = []
    
    for url in FEED_URLS:
        print(f"Scraping: {url}")
        feed = feedparser.parse(url)
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
            
    with open("feed.json", "w") as f:
        json.dump(combined_entries, f, indent=4)
    print(f"Successfully saved {len(combined_entries)} items to feed.json")

if __name__ == "__main__":
    fetch_all_feeds()
