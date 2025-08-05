import sqlite3
from datetime import datetime

DB_PATH = 'data/bargains.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT,
            url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Insert dummy deals if table empty
    c.execute('SELECT COUNT(*) FROM deals')
    count = c.fetchone()[0]
    if count == 0:
        sample_deals = [
            ("Ultra HD TV 50\" Sale", "$499", "https://example.com/deal1"),
            ("Wireless Earbuds", "$29", "https://example.com/deal2"),
            ("Gaming Laptop Discount", "$999", "https://example.com/deal3"),
        ]
        for title, price, url in sample_deals:
            c.execute("INSERT INTO deals (title, price, url, created_at) VALUES (?, ?, ?, ?)",
                      (title, price, url, datetime.now()))
        conn.commit()
        print(f"Inserted {len(sample_deals)} dummy deals.")
    else:
        print("Deals table already has data, skipping insert.")

    conn.close()

if __name__ == "__main__":
    init_db()
