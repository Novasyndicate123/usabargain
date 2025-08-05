import streamlit as st
import sqlite3
from modules.voting import cast_vote

DB_PATH = 'data/bargains.db'  # Adjust if necessary

# Connect to DB
def get_deals():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM deals ORDER BY ai_score DESC, timestamp DESC')
    deals = c.fetchall()
    conn.close()
    return deals

def color_for_score(score):
    # Map score (0 to max) to green (high) - red (low)
    # Normalize score to 0-1 for color gradient
    norm = min(max(score / 10, 0), 1)  # Assume 10+ is max score for gradient
    red = int(255 * (1 - norm))
    green = int(255 * norm)
    return f'background-color: rgb({red},{green},0)'

def main():
    st.title("NovaBargains — AI-Powered Deals")

    user_id = st.text_input("Enter your user ID:", "anon")

    deals = get_deals()
    if not deals:
        st.write("No deals found.")
        return

    for deal in deals:
        score = deal["ai_score"] or 0
        color_style = color_for_score(score)
        with st.container():
            st.markdown(f"<div style='{color_style};padding:10px;border-radius:5px;'>", unsafe_allow_html=True)
            st.subheader(deal["title"])
            st.write(f"Upvotes: {deal['upvotes'] or 0} | Downvotes: {deal['downvotes'] or 0} | AI Score: {score:.2f}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Upvote #{deal['id']}"):
                    cast_vote(deal["id"], "up", user_id)
                    st.experimental_rerun()
            with col2:
                if st.button(f"Downvote #{deal['id']}"):
                    cast_vote(deal["id"], "down", user_id)
                    st.experimental_rerun()
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
