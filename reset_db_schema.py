import sqlite3
conn = sqlite3.connect('data/bargains.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS deals")
c.execute("""
CREATE TABLE deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    description TEXT
)
""")
conn.commit()
conn.close()
print("✅ Database schema reset successfully.")
