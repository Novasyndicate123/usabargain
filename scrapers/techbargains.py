
import requests
from bs4 import BeautifulSoup

def scrape_techbargains():
    url = "https://www.techbargains.com/"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("div.card-body")
        print(f"📥 TechBargains: {len(cards)} deals found")
        for card in cards[:5]:
            title = card.select_one("h4.card-title")
            link = card.find_parent("a")["href"]
            if title:
                print(f"📰 {title.text.strip()} — {link}")
    except Exception as e:
        print(f"[ERROR] TechBargains: {e}")
