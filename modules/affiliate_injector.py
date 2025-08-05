import sqlite3
import re

DB_PATH = 'data/bargains.db'  # Adjust as necessary

# Example affiliate domains and their tracking query params
AFFILIATE_DOMAINS = {
    'amazon.com': 'tag=your-affiliate-tag',
    'bestbuy.com': 'ref=your-affiliate-code',
    # Add more affiliate programs here
}

def inject_affiliate_links(deal_url: str) -> str:
    """
    Detects affiliate-supported domains in URLs and appends tracking parameters.
    """
    for domain, param in AFFILIATE_DOMAINS.items():
        if domain in deal_url:
            if '?' in deal_url:
                if param not in deal_url:
                    return deal_url + '&' + param
            else:
                return deal_url + '?' + param
    return deal_url

def update_deals_with_affiliate_links():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, url FROM deals')
        deals = c.fetchall()
        for deal_id, url in deals:
            if not url:
                continue
            new_url = inject_affiliate_links(url)
            if new_url != url:
                c.execute('UPDATE deals SET url = ? WHERE id = ?', (new_url, deal_id))
        conn.commit()

if __name__ == "__main__":
    update_deals_with_affiliate_links()
    print("Affiliate link injection completed.")
