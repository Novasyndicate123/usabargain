import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'

def get_deal_stats():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM deals WHERE flagged=0')
        total_deals = c.fetchone()[0] or 0
        c.execute('SELECT COUNT(*) FROM deals WHERE flagged=1')
        flagged_deals = c.fetchone()[0] or 0
    return total_deals, flagged_deals

def get_user_activity_stats():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        since = (datetime.utcnow() - timedelta(days=1)).isoformat()
        c.execute('SELECT COUNT(*) FROM user_interactions WHERE timestamp > ?', (since,))
        interactions = c.fetchone()[0] or 0
    return interactions

def alert_on_thresholds(total_deals, flagged_deals, interactions):
    alerts = []
    if flagged_deals > total_deals * 0.1:
        alerts.append(f"Warning: High flagged deals ratio: {flagged_deals}/{total_deals}")
    if interactions < 10:
        alerts.append("Warning: Low user activity detected in last 24h.")
    return alerts

def generate_report():
    total_deals, flagged_deals = get_deal_stats()
    interactions = get_user_activity_stats()
    alerts = alert_on_thresholds(total_deals, flagged_deals, interactions)

    report = f"""
    === NovaBargains Analytics Report ===
    Total Deals: {total_deals}
    Flagged Deals: {flagged_deals}
    User Interactions (24h): {interactions}
    Alerts:
    """
    report += "\n".join(alerts) if alerts else "None"
    return report.strip()

if __name__ == "__main__":
    print(generate_report())
