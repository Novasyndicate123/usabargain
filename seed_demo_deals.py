import sqlite3
conn = sqlite3.connect('data/bargains.db')
c = conn.cursor()
demo_deals = [
    ("Ultra HD TV 50 - HALF PRICE", 499.99, "Crystal-clear display, smart features included."),
    ("Gaming Laptop Discount", 999.99, "High-performance laptop for gamers and creators."),
    ("Wireless Earbuds", 29.99, "Great sound quality with noise cancellation.")
]
c.executemany("INSERT INTO deals (title, price, description) VALUES (?, ?, ?)", demo_deals)
conn.commit()
conn.close()
print("[+] Demo deals inserted successfully.")
