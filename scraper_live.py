import requests
from bs4 import BeautifulSoup
import sqlite3
import os

DB_PATH = os.path.join("data", "bargains.db")
DEALS_URL = "https://slickdeals.net/deals/"

def scrape_slickdeals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(DEALS_URL, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"[ERROR] HTTP Error: {e}")
        return 0
    except requests.RequestException as e:
        print(f"[ERROR] Request Exception: {e}")
        return 0

    soup = BeautifulSoup(response.text, "html.parser")

    deals_list = []

    # Updated selector to match current Slickdeals deal items
    deal_items = soup.select("div.dealRow")

    if not deal_items:
        print("[WARNING] Deals list is empty after parsing.")
        return 0

    for item in deal_items:
        title_elem = item.select_one("a.dealTitle")
        price_elem = item.select_one("span.price") or item.select_one("div.price")

        if not title_elem:
            continue

        title = title_elem.get_text(strip=True)
        url = title_elem.get("href")
        if url and not url.startswith("http"):
            url = "https://slickdeals.net" + url

        price = price_elem.get_text(strip=True) if price_elem else "N/A"

        deals_list.append((title, price, url))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted_count = 0
    for title, price, url in deals_list:
        cursor.execute("SELECT id FROM deals WHERE url = ?", (url,))
        if cursor.fetchone():
            continue
        cursor.execute(
            "INSERT INTO deals (title, price, url) VALUES (?, ?, ?)",
            (title, price, url),
        )
        inserted_count += 1

    conn.commit()
    conn.close()

    return inserted_count


if __name__ == "__main__":
    count = scrape_slickdeals()
    print(f"Inserted {count} new deals from Slickdeals homepage")
