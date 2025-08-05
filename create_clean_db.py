import sqlite3
import os

db_path = "data/bargains.db"

# Ensure data folder exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Drop table if exists (to clean slate)
c.execute("DROP TABLE IF EXISTS deals")

# Create fresh deals table
c.execute("""
CREATE TABLE deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price TEXT,
    url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert clean sample deals with proper prices
deals = [
    ("Wireless Earbuds", "$29", "https://example.com/earbuds"),
    ("Gaming Laptop Discount", "$999", "https://example.com/laptop"),
    ('Ultra HD TV 50" Sale', "$499", "https://example.com/tv"),
]

c.executemany("INSERT INTO deals (title, price, url) VALUES (?, ?, ?)", deals)

conn.commit()
conn.close()

print(f"✅ Clean database created at {db_path}")
