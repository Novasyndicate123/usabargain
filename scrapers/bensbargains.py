
import requests
from bs4 import BeautifulSoup

def scrape_bensbargains():
    url = "https://bensbargains.com/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("div.node-title")
        print(f"📥 BensBargains: {len(items)} deals found")
        for item in items[:5]:
            title = item.get_text(strip=True)
            link = item.find_parent("a")["href"]
            print(f"📰 {title} — {link}")
    except Exception as e:
        print(f"[ERROR] BensBargains: {e}")
