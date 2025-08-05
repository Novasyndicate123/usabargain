from database import insert_deal

# Sample function to insert mock deals
def ingest_mock_deals():
    deals = [
        ("Wireless Mouse", "14.99", "https://example.com/mouse"),
        ("Mechanical Keyboard", "49.99", "https://example.com/keyboard"),
        ("Free VPN Trial", "Free", "https://example.com/vpn"),
    ]
    for title, price, url in deals:
        insert_deal(title, price, url)

if __name__ == "__main__":
    ingest_mock_deals()
    print("✅ Mock deals ingested.")