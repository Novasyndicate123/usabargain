import sqlite3
from datetime import datetime

DB_PATH = 'data/bargains.db'

AFFILIATE_CODES = {
    'amazon': 'your-amazon-affiliate-code',
    'walmart': 'your-walmart-affiliate-code',
    # Add more affiliate codes per retailer here
}

def rewrite_affiliate_link(url):
    # Example: append affiliate code query param based on domain
    for retailer, code in AFFILIATE_CODES.items():
        if retailer in url:
            if 'affiliate_id=' not in url:
                connector = '&' if '?' in url else '?'
                return f"{url}{connector}affiliate_id={code}"
    return url

def track_click(user_id, deal_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO affiliate_clicks (user_id, deal_id, timestamp)
            VALUES (?, ?, ?)
        ''', (user_id, deal_id, datetime.utcnow().isoformat()))
        conn.commit()

def calculate_commissions():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT deal_id, COUNT(*) as clicks
            FROM affiliate_clicks
            GROUP BY deal_id
        ''')
        results = c.fetchall()
        commissions = {}
        for deal_id, clicks in results:
            # Example commission rate: $0.05 per click
            commissions[deal_id] = clicks * 0.05
        return commissions

if __name__ == "__main__":
    # Demo rewrite
    test_url = "https://www.amazon.com/product123"
    print("Affiliate Link:", rewrite_affiliate_link(test_url))
    
    # Demo commission calc
    commissions = calculate_commissions()
    print("Commissions:", commissions)
