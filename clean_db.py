# clean_db.py
import sqlite3

conn = sqlite3.connect("data/bargains.db")
cur = conn.cursor()

# Delete all dummy/sample deals
cur.execute("DELETE FROM deals WHERE title LIKE 'Sample Deal%'")
conn.commit()

print("[✔] Dummy deals removed.")

# Optional: print remaining deals for confirmation
cur.execute("SELECT title, price FROM deals")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()
