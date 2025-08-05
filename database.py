import sqlite3

def get_connection():
    return sqlite3.connect("data/bargains.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_deal(title, price, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO deals (title, price, url) VALUES (?, ?, ?)", (title, price, url))
    conn.commit()
    conn.close()

def create_votes_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deal_id INTEGER NOT NULL,
            vote_type TEXT CHECK(vote_type IN ('up', 'down')),
            user_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(deal_id, user_id)
        )
    ''')
    conn.commit()

def add_vote_counts(conn):
    # Add columns if not present
    try:
        conn.execute("ALTER TABLE deals ADD COLUMN upvotes INTEGER DEFAULT 0")
    except:
        pass
    try:
        conn.execute("ALTER TABLE deals ADD COLUMN downvotes INTEGER DEFAULT 0")
    except:
        pass
    conn.commit()


def add_hash_column(conn):
    try:
        conn.execute("ALTER TABLE deals ADD COLUMN hash TEXT;")
        conn.commit()
    except Exception as e:
        pass  # Likely already added
