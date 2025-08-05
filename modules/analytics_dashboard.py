import streamlit as st
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

DB_PATH = 'data/bargains.db'

# Email alert config
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USER = 'alert@yourdomain.com'
SMTP_PASS = 'yourpassword'
ALERT_TO = 'you@yourdomain.com'
ALERT_THRESHOLD = 5  # Minimum new deals per day before alert

def get_metrics():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM deals')
        total_deals = c.fetchone()[0]
        cutoff = (datetime.utcnow() - timedelta(days=1)).isoformat()
        c.execute('SELECT COUNT(*) FROM deals WHERE timestamp >= ?', (cutoff,))
        deals_last_24h = c.fetchone()[0]
        c.execute('SELECT AVG(ai_score) FROM deals')
        avg_score = c.fetchone()[0] or 0
    return total_deals, deals_last_24h, avg_score

def send_alert(deals_last_24h):
    subject = "NovaBargains Alert: Low Deal Activity"
    body = f"Warning: Only {deals_last_24h} new deals posted in the last 24 hours."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_TO

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, ALERT_TO, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send alert email: {e}")
        return False

def main():
    st.title("NovaBargains Analytics Dashboard")

    total_deals, deals_last_24h, avg_score = get_metrics()

    st.metric("Total Deals", total_deals)
    st.metric("Deals Last 24h", deals_last_24h)
    st.metric("Average AI Score", f"{avg_score:.2f}")

    if deals_last_24h < ALERT_THRESHOLD:
        st.warning(f"Low deal activity detected: only {deals_last_24h} deals in last 24 hours!")
        if st.button("Send Alert Email Now"):
            if send_alert(deals_last_24h):
                st.success("Alert email sent successfully.")
            else:
                st.error("Failed to send alert email.")

if __name__ == "__main__":
    main()
