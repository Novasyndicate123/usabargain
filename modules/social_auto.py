import sqlite3
import time
from datetime import datetime, timedelta
import random

DB_PATH = 'data/bargains.db'
POST_INTERVAL_SECONDS = 3600  # 1 hour

# Placeholder function: Replace with real API integration
def publish_to_social(platform, content):
    print(f"[{datetime.utcnow()}] Published to {platform}: {content}")

def fetch_deals_for_post():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, title FROM deals WHERE flagged=0 ORDER BY ai_score DESC LIMIT 20')
        return c.fetchall()

def generate_post_content(deal):
    deal_id, title = deal
    hashtags = ["#Deals", "#Savings", "#Discount", "#Bargain", "#ShopSmart"]
    hashtag_str = " ".join(random.sample(hashtags, 2))
    return f"🔥 Hot Deal: {title}! Don't miss out! {hashtag_str} https://yourdomain.com/deals/{deal_id}"

def social_scheduler_loop():
    platforms = ['Twitter', 'Facebook', 'Instagram']
    while True:
        deals = fetch_deals_for_post()
        if not deals:
            print("No deals available for posting.")
            time.sleep(POST_INTERVAL_SECONDS)
            continue

        deal = random.choice(deals)
        post_content = generate_post_content(deal)

        for platform in platforms:
            publish_to_social(platform, post_content)

        time.sleep(POST_INTERVAL_SECONDS)

if __name__ == "__main__":
    social_scheduler_loop()
