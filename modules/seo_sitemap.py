import sqlite3
from datetime import datetime
import os

DB_PATH = 'data/bargains.db'  # Adjust if needed
SITEMAP_PATH = 'static/sitemap.xml'  # Ensure 'static' folder exists

BASE_URL = "https://yourdomain.com/deal/"  # Replace with actual domain

def fetch_deals_for_sitemap():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, title, timestamp FROM deals')
        return c.fetchall()

def escape_xml(text):
    return (text.replace("&", "&amp;")
                .replace("\"", "&quot;")
                .replace("'", "&apos;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

def generate_sitemap_xml(deals):
    urlset_open = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    urlset_close = '</urlset>'

    urls = ""
    for deal_id, title, timestamp in deals:
        lastmod = datetime.fromisoformat(timestamp).date().isoformat() if timestamp else datetime.utcnow().date().isoformat()
        url = f"{BASE_URL}{deal_id}"
        urls += f"  <url>\n" \
                f"    <loc>{url}</loc>\n" \
                f"    <lastmod>{lastmod}</lastmod>\n" \
                f"    <changefreq>daily</changefreq>\n" \
                f"    <priority>0.8</priority>\n" \
                f"  </url>\n"

    return urlset_open + urls + urlset_close

def save_sitemap(content):
    os.makedirs(os.path.dirname(SITEMAP_PATH), exist_ok=True)
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    deals = fetch_deals_for_sitemap()
    sitemap_xml = generate_sitemap_xml(deals)
    save_sitemap(sitemap_xml)
    print(f"Sitemap generated with {len(deals)} URLs at {SITEMAP_PATH}")

if __name__ == "__main__":
    main()
