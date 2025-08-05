# NovaBargains/modules/verify_deal.py

import hashlib
from datetime import datetime

def clean_title(title):
    return title.strip().replace("\n", "").replace("\r", "")

def is_valid_deal(deal):
    required_fields = ["title", "url", "price"]
    return all(deal.get(field) for field in required_fields)

def hash_deal(deal):
    data = f"{deal.get('title')}{deal.get('url')}{deal.get('price')}"
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def deduplicate_deals(existing_hashes, incoming_deals):
    unique_deals = []
    new_hashes = set()
    for deal in incoming_deals:
        deal_hash = hash_deal(deal)
        if deal_hash not in existing_hashes and deal_hash not in new_hashes:
            deal["hash"] = deal_hash
            deal["timestamp"] = datetime.now().isoformat()
            unique_deals.append(deal)
            new_hashes.add(deal_hash)
    return unique_deals
