import sqlite3

conn = sqlite3.connect('data/bargains.db')
cursor = conn.cursor()

# Demo deals data with corrected string quotes
demo_deals = [
    ("Wireless Earbuds", "High-quality sound with noise cancellation.", "https://example.com/deal1", "https://example.com/image1.jpg", 29.99),
    ("Gaming Laptop Discount", "Powerful gaming laptop with RTX 4060.", "https://example.com/deal2", "https://example.com/image2.jpg", 999.99),
    ('📺 Ultra HD TV 50" - HALF PRICE', "Crystal-clear display, smart features included.", "https://example.com/deal3", "https://example.com/image3.jpg", 499.99)
]

for deal in demo_deals:
    cursor.execute("""
        INSERT INTO deals (title, description, url, image_url, price)
        VALUES (?, ?, ?, ?, ?)
    """, deal)

conn.commit()
conn.close()

print("Demo deals seeded successfully.")
