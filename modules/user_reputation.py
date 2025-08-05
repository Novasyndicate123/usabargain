import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'

REPUTATION_WEIGHTS = {
    'post_deal': 10,
    'vote_up': 3,
    'vote_down': -1,
    'comment': 5,
    'flagged': -20,
}

def calculate_reputation(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Count posts
        c.execute('SELECT COUNT(*) FROM deals WHERE user_id = ?', (user_id,))
        posts = c.fetchone()[0] or 0
        # Votes received on user's deals
        c.execute('''
            SELECT SUM(CASE WHEN vote=1 THEN 1 ELSE 0 END),
                   SUM(CASE WHEN vote=-1 THEN 1 ELSE 0 END)
            FROM votes JOIN deals ON votes.deal_id = deals.id
            WHERE deals.user_id = ?
        ''', (user_id,))
        vote_up, vote_down = c.fetchone()
        vote_up = vote_up or 0
        vote_down = vote_down or 0
        # Comments count
        c.execute('SELECT COUNT(*) FROM comments WHERE user_id = ?', (user_id,))
        comments = c.fetchone()[0] or 0
        # Flags against user content
        c.execute('SELECT COUNT(*) FROM flags WHERE target_user_id = ?', (user_id,))
        flags = c.fetchone()[0] or 0

        reputation = (
            posts * REPUTATION_WEIGHTS['post_deal'] +
            vote_up * REPUTATION_WEIGHTS['vote_up'] +
            vote_down * REPUTATION_WEIGHTS['vote_down'] +
            comments * REPUTATION_WEIGHTS['comment'] +
            flags * REPUTATION_WEIGHTS['flagged']
        )
        # Ensure reputation floor
        reputation = max(reputation, 0)
        # Update or insert reputation score
        c.execute('''
            INSERT INTO user_reputation (user_id, reputation, last_updated)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            reputation=excluded.reputation,
            last_updated=excluded.last_updated
        ''', (user_id, reputation, datetime.utcnow().isoformat()))
        conn.commit()
        return reputation

def update_all_reputations():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM users')
        user_ids = [row[0] for row in c.fetchall()]
    for uid in user_ids:
        rep = calculate_reputation(uid)
        print(f"Updated reputation for user {uid}: {rep}")

if __name__ == "__main__":
    update_all_reputations()
