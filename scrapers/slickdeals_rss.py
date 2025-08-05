
import feedparser
from datetime import datetime

def scrape_slickdeals_rss():
    url = "https://slickdeals.net/newsearch.php?searcharea=deals&searchin=first&rss=1"
    feed = feedparser.parse(url)
    print(f"📥 Slickdeals RSS: {len(feed.entries)} deals found")
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        pub_date = entry.published
        print(f"📰 {title} — {link} — {pub_date}")
