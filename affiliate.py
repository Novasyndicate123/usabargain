"""Affiliate link helpers: tagging, UTM params, and compliant <a> markup."""
import os
from html import escape
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# (domain suffix, query param name, tag value). Tags without a real value are skipped.
AFFILIATE_PROGRAMS = [
    ("amazon.com", "tag", os.getenv("AMAZON_TAG", "workfrom09dda-20")),
    ("ebay.com", "campid", os.getenv("EBAY_CAMPID", "")),
    ("walmart.com", "affp1", os.getenv("WALMART_AFFID", "")),
]

UTM_SOURCE = os.getenv("UTM_SOURCE", "novabargains")
DISCLOSURE = ("As an Amazon Associate I earn from qualifying purchases. "
              "Some links on this site are affiliate links; we may earn a commission at no extra cost to you.")


def _host_matches(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def inject_affiliate_link(url: str, campaign: str = "deals") -> str:
    """Add the affiliate tag (replacing any existing one) plus UTM params. Non-affiliate URLs pass through."""
    if not url:
        return url
    parts = urlparse(url)
    host = (parts.hostname or "").lower()
    for domain, param, value in AFFILIATE_PROGRAMS:
        if _host_matches(host, domain):
            if not value:
                return url  # no real tag configured; don't pollute the URL
            query = dict(parse_qsl(parts.query))
            query[param] = value
            query.setdefault("utm_source", UTM_SOURCE)
            query.setdefault("utm_medium", "affiliate")
            query.setdefault("utm_campaign", campaign)
            return urlunparse(parts._replace(query=urlencode(query)))
    return url


def affiliate_anchor(url: str, text: str = "View deal", campaign: str = "deals") -> str:
    """Return an HTML link with rel="sponsored nofollow noopener" (escaped)."""
    href = escape(inject_affiliate_link(url, campaign), quote=True)
    return f'<a href="{href}" target="_blank" rel="sponsored nofollow noopener">{escape(text)}</a>'
