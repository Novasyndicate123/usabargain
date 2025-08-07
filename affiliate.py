AFFILIATE_TAGS = {
    "amazon": "tag=workfrom09dda-20",
    "ebay": "campid=yourcampid",
    "walmart": "affp1=youraffid",
}

def inject_affiliate_link(url):
    if "amazon.com" in url:
        return f"{url}&{AFFILIATE_TAGS['amazon']}" if "?" in url else f"{url}?{AFFILIATE_TAGS['amazon']}"
    elif "ebay.com" in url:
        return f"{url}&{AFFILIATE_TAGS['ebay']}" if "?" in url else f"{url}?{AFFILIATE_TAGS['ebay']}"
    elif "walmart.com" in url:
        return f"{url}&{AFFILIATE_TAGS['walmart']}" if "?" in url else f"{url}?{AFFILIATE_TAGS['walmart']}"
    else:
        return url


