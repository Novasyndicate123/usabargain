import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('data/bargains.db')
cursor = conn.cursor()

cutoff = datetime.now() - timedelta(days=30)  # Purge deals older than 30 days

cursor.execute("DELETE FROM deals WHERE created_at < ?", (cutoff,))
deleted = cursor.rowcount

conn.commit()
conn.close()

print(f"AutoPurger complete. {deleted} old deals removed.")
