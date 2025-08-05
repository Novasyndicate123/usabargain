$debugScript = @'
import requests
from bs4 import BeautifulSoup

def scrape_slickdeals():
    url = "https://slickdeals.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    response = requests.get(url, headers=headers)

    print("✅ Page fetch status:", response.status_code)
    print("🧾 Page content preview:\n", response.text[:500], "\n\n")

    soup = BeautifulSoup(response.text, "html.parser")
    deal_items = soup.select(".fpItem")

    print("🔍 Number of .fpItem deals found:", len(deal_items))

    for i, item in enumerate(deal_items[:3]):
        print(f"\n🧪 Deal {i+1} HTML preview:\n", item.prettify()[:300], "\n")

if __name__ == "__main__":
    scrape_slickdeals()
'@

Set-Content -Path "scraper_debug.py" -Value $debugScript -Encoding UTF8
python scraper_debug.py
