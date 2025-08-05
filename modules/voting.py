import sqlite3
from datetime import datetime

DB_PATH = 'data/bargains.db'  # Adjust path if needed

def cast_vote(deal_id: int, vote_type: str, user_id: str):
    if vote_type not in ('up', 'down'):
        raise ValueError("vote_type must be 'up' or 'down'")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Insert or ignore vote
        c.execute('''
            INSERT OR IGNORE INTO votes (deal_id, vote_type, user_id) VALUES (?, ?, ?)
        ''', (deal_id, vote_type, user_id))
        # Update vote if different
        c.execute('''
            UPDATE votes SET vote_type = ?, timestamp = ?
            WHERE deal_id = ? AND user_id = ? AND vote_type != ?
        ''', (vote_type, datetime.utcnow(), deal_id, user_id, vote_type))
        # Count votes
        c.execute('SELECT COUNT(*) FROM votes WHERE deal_id = ? AND vote_type = "up"', (deal_id,))
        upvotes = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM votes WHERE deal_id = ? AND vote_type = "down"', (deal_id,))
        downvotes = c.fetchone()[0]
        # Update deals
        c.execute('''
            UPDATE deals SET upvotes = ?, downvotes = ? WHERE id = ?
        ''', (upvotes, downvotes, deal_id))
        conn.commit()
