import sqlite3
import math
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'  # Adjust if needed

class DealScorer:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def fetch_deals(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                SELECT id, upvotes, downvotes, timestamp
                FROM deals
            ''')
            rows = c.fetchall()
        return rows

    def score_deal(self, upvotes, downvotes, timestamp):
        """Calculate a score based on votes and recency"""
        net_votes = upvotes - downvotes
        # Time decay: newer deals score higher; timestamp expected ISO string
        try:
            deal_time = datetime.fromisoformat(timestamp)
        except Exception:
            deal_time = datetime.utcnow()

        age_hours = (datetime.utcnow() - deal_time).total_seconds() / 3600
        decay_factor = math.exp(-age_hours / 48)  # half-life ~2 days

        score = net_votes * decay_factor
        return max(score, 0)  # no negative scores

    def update_scores(self):
        deals = self.fetch_deals()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            for deal_id, upvotes, downvotes, timestamp in deals:
                score = self.score_deal(upvotes or 0, downvotes or 0, timestamp or '')
                c.execute('UPDATE deals SET ai_score = ? WHERE id = ?', (score, deal_id))
            conn.commit()

    def generate_heatmap_data(self):
        """
        Returns a dict: {deal_id: score} for frontend heatmap visualization.
        """
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, ai_score FROM deals')
            return {row[0]: row[1] for row in c.fetchall()}

if __name__ == "__main__":
    scorer = DealScorer()
    scorer.update_scores()
    heatmap = scorer.generate_heatmap_data()
    print("Current deal heatmap scores:")
    for deal_id, score in heatmap.items():
        print(f"Deal {deal_id}: Score {score:.2f}")
