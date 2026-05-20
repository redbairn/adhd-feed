import feedparser
import json
import os
from datetime import datetime

# Add your favorite ADHD RSS feeds here
FEED_URLS = [
    "https://www.reddit.com/r/ADHD/.rss",
    "https://www.additudemag.com/feed/",
    "https://adhddd.com/feed/",
    "https://media.rss.com/absolutelyadhd/feed.xml"
]

def fetch_all():
    combined_posts = []
    
    for url in FEED_URLS:
        print(f"Fetching: {url}")
        feed = feedparser.parse(url)
        source_title = feed.feed.get('title', 'Unknown Source')
        
        for entry in feed.entries:
            # Standardize date parsed into an ISO string
            pub_date = entry.get('published', entry.get('updated', ''))
            
            combined_posts.append({
                "title": entry.get('title', 'No Title'),
                "link": entry.get('link', '#'),
                "summary": entry.get('summary', entry.get('description', ''))[:300] + "...",
                "source": source_title,
                "date": pub_date
            })
            
    # Quick fallback sorting (most recent first)
    combined_posts.sort(key=lambda x: x['date'], reverse=True)
    
    with open("feed.json", "w", encoding="utf-8") as f:
        json.dump(combined_posts[:100], f, indent=2) # Keep the top 100 posts

if __name__ == "__main__":
    fetch_all()