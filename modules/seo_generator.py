import sqlite3
from datetime import datetime
import xml.etree.ElementTree as ET

DB_PATH = 'data/bargains.db'
SITEMAP_PATH = 'data/sitemap.xml'

def generate_seo_description(title):
    # Simplistic SEO template — replace with AI generation if available
    return f"Get the best deals on {title}. Updated daily with exclusive offers and savings."

def update_deal_descriptions():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, title, description FROM deals WHERE description IS NULL OR description = ""')
        deals = c.fetchall()
        for deal_id, title, _ in deals:
            desc = generate_seo_description(title)
            c.execute('UPDATE deals SET description = ? WHERE id = ?', (desc, deal_id))
        conn.commit()

def generate_sitemap():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id FROM deals')
        deal_ids = [row[0] for row in c.fetchall()]

    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    base_url = "https://yourdomain.com/deals/"

    for deal_id in deal_ids:
        url = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = f"{base_url}{deal_id}"
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = datetime.utcnow().date().isoformat()
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'daily'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.8'

    tree = ET.ElementTree(urlset)
    tree.write(SITEMAP_PATH, encoding='utf-8', xml_declaration=True)

def main():
    update_deal_descriptions()
    generate_sitemap()
    print("SEO descriptions updated and sitemap.xml generated.")

if __name__ == "__main__":
    main()
