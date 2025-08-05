import sqlite3
import re

DB_PATH = 'data/bargains.db'

# Simple keyword-based spam/abuse patterns (expandable)
SPAM_PATTERNS = [
    r'(free money|click here|buy now|subscribe)',  # common spam phrases
    r'https?://[^\s]+',  # suspicious links
    r'cheap\s+viagra',
    r'work\s+from\s+home',
]

def is_spam(text):
    text_lower = text.lower()
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def flag_spam_content():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Check new deals
        c.execute('SELECT id, title, description FROM deals WHERE flagged = 0')
        deals = c.fetchall()
        for deal_id, title, desc in deals:
            if is_spam(title) or is_spam(desc or ''):
                c.execute('UPDATE deals SET flagged = 1 WHERE id = ?', (deal_id,))
                print(f"Flagged spam deal: {deal_id}")

        # Check new comments
        c.execute('SELECT id, comment_text FROM comments WHERE flagged = 0')
        comments = c.fetchall()
        for comment_id, text in comments:
            if is_spam(text):
                c.execute('UPDATE comments SET flagged = 1 WHERE id = ?', (comment_id,))
                print(f"Flagged spam comment: {comment_id}")
        conn.commit()

if __name__ == "__main__":
    flag_spam_content()
