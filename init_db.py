import sqlite3
import os

DB_PATH = os.path.join("data", "bargains.db")

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT,
            url TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized with deals table.")

if __name__ == "__main__":
    init_db()
