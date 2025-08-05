import sqlite3
from datetime import datetime

conn = sqlite3.connect('data/bargains.db')
cursor = conn.cursor()

# Add created_at column if it doesn't exist
try:
    cursor.execute("ALTER TABLE deals ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
except sqlite3.OperationalError as e:
    print(f"Warning: {e} (probably column already exists)")

# Update existing rows with current timestamp if null
cursor.execute("UPDATE deals SET created_at = ? WHERE created_at IS NULL", (datetime.now(),))

conn.commit()
conn.close()

print("Database schema updated with created_at column.")
