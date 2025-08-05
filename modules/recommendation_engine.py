import sqlite3
import numpy as np

DB_PATH = 'data/bargains.db'

class RecommendationEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def get_user_interactions(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT deal_id FROM user_interactions WHERE user_id = ?', (user_id,))
            return set(row[0] for row in c.fetchall())

    def get_deal_features(self, deal_id):
        # Example: Returns a vector of features (could be expanded)
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT ai_score, price, category_id FROM deals WHERE id = ?', (deal_id,))
            row = c.fetchone()
            if row:
                ai_score, price, category_id = row
                return np.array([ai_score or 0, price or 0, category_id or 0])
            return np.zeros(3)

    def get_all_deals(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id FROM deals')
            return [row[0] for row in c.fetchall()]

    def recommend(self, user_id, top_k=10):
        user_deals = self.get_user_interactions(user_id)
        all_deals = self.get_all_deals()

        # For demo: simple similarity score based on ai_score & category
        recommendations = []
        user_features = np.mean([self.get_deal_features(d) for d in user_deals], axis=0) if user_deals else np.zeros(3)

        for deal_id in all_deals:
            if deal_id in user_deals:
                continue
            features = self.get_deal_features(deal_id)
            similarity = np.dot(user_features, features) / (np.linalg.norm(user_features) * np.linalg.norm(features) + 1e-5)
            recommendations.append((deal_id, similarity))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [deal_id for deal_id, score in recommendations[:top_k]]

if __name__ == "__main__":
    engine = RecommendationEngine()
    user_id = 1  # Example user
    recs = engine.recommend(user_id)
    print(f"Recommended deals for user {user_id}: {recs}")
