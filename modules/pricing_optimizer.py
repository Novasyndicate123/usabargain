import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'

def get_recent_deal_performance(deal_id, days=7):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        c.execute('''
            SELECT COUNT(*) FROM user_interactions
            WHERE deal_id = ? AND timestamp > ?
        ''', (deal_id, since))
        interactions = c.fetchone()[0] or 0

        c.execute('SELECT price, original_price FROM deals WHERE id = ?', (deal_id,))
        row = c.fetchone()
        if row:
            price, original_price = row
        else:
            price, original_price = None, None
    return interactions, price, original_price

def optimize_discount(deal_id):
    interactions, price, original_price = get_recent_deal_performance(deal_id)
    if not price or not original_price or original_price <= price:
        return None  # No discount possible

    discount_rate = (original_price - price) / original_price
    # Simple rule: increase discount if low interaction, decrease if high interaction
    if interactions < 10:
        discount_rate = min(discount_rate + 0.05, 0.5)  # cap 50%
    elif interactions > 50:
        discount_rate = max(discount_rate - 0.05, 0.05)  # minimum 5%

    new_price = round(original_price * (1 - discount_rate), 2)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE deals SET price = ? WHERE id = ?', (new_price, deal_id))
        conn.commit()
    return new_price

def optimize_all_deals():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM deals WHERE flagged = 0')
        deal_ids = [row[0] for row in c.fetchall()]
    for deal_id in deal_ids:
        new_price = optimize_discount(deal_id)
        if new_price:
            print(f"Deal {deal_id} price updated to {new_price}")

if __name__ == "__main__":
    optimize_all_deals()
