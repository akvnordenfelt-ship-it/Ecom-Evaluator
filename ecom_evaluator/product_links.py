"""Parse and validate marketplace product listing URLs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

MARKETPLACE_HOSTS: dict[str, str] = {
    "aliexpress.com": "AliExpress",
    "www.aliexpress.com": "AliExpress",
    "amazon.com": "Amazon",
    "www.amazon.com": "Amazon",
    "amazon.co.uk": "Amazon UK",
    "www.amazon.co.uk": "Amazon UK",
    "amazon.de": "Amazon DE",
    "www.amazon.de": "Amazon DE",
    "alibaba.com": "Alibaba",
    "www.alibaba.com": "Alibaba",
    "ebay.com": "eBay",
    "www.ebay.com": "eBay",
    "temu.com": "Temu",
    "www.temu.com": "Temu",
    "etsy.com": "Etsy",
    "www.etsy.com": "Etsy",
}

_SLUG_SPLIT = re.compile(r"[-_+/]+")
_ASIN_RE = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})", re.IGNORECASE)
_ALIEXPRESS_ITEM_RE = re.compile(r"/item/(\d+)", re.IGNORECASE)
_ALIEXPRESS_SLUG_RE = re.compile(r"/item/\d+-(.+?)\.html", re.IGNORECASE)


@dataclass(frozen=True)
class ProductLinkInfo:
    url: str
    host: str
    platform: str
    listing_id: str | None
    slug_hint: str | None


def normalize_product_url(raw: str) -> str:
    value = raw.strip()
    if not value:
        return ""
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def parse_product_url(raw: str) -> ProductLinkInfo | None:
    """Return structured link metadata when the URL looks like a product listing."""
    normalized = normalize_product_url(raw)
    if not normalized:
        return None

    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None

    host = parsed.netloc.lower()
    if "." not in host:
        return None
    platform = MARKETPLACE_HOSTS.get(host, "Marketplace")
    path = parsed.path or ""

    listing_id: str | None = None
    slug_hint: str | None = None

    ali_match = _ALIEXPRESS_ITEM_RE.search(path)
    if ali_match:
        listing_id = ali_match.group(1)
        slug_match = _ALIEXPRESS_SLUG_RE.search(path)
        if slug_match:
            slug_hint = _slug_from_slug_text(slug_match.group(1))
        else:
            slug_hint = _slug_from_path(path, stop_tokens={"item", "html", listing_id})

    asin_match = _ASIN_RE.search(path)
    if asin_match:
        listing_id = asin_match.group(1).upper()
        slug_hint = _slug_from_path(path, stop_tokens={"dp", "gp", "product", listing_id.lower()})

    if not slug_hint:
        slug_hint = _slug_from_path(path)

    return ProductLinkInfo(
        url=normalized,
        host=host,
        platform=platform,
        listing_id=listing_id,
        slug_hint=slug_hint,
    )


def validate_product_url(raw: str) -> tuple[ProductLinkInfo | None, str | None]:
    """Validate an optional listing URL. Empty input is allowed."""
    if not raw.strip():
        return None, None

    link = parse_product_url(raw)
    if link is None:
        return None, (
            "Enter a valid product listing URL (https://…) from AliExpress, Amazon, eBay, "
            "Temu, Alibaba, or Etsy."
        )
    return link, None


def _slug_from_path(path: str, *, stop_tokens: set[str] | None = None) -> str | None:
    stop = {token.lower() for token in (stop_tokens or set())}
    tokens: list[str] = []
    for part in _SLUG_SPLIT.split(path):
        chunk = part.strip()
        if not chunk or chunk.isdigit() or chunk.lower() in stop:
            continue
        if len(chunk) <= 2:
            continue
        tokens.append(chunk.replace("%20", " "))
    if not tokens:
        return None
    phrase = " ".join(tokens[:8])
    return phrase.title() if phrase.islower() else phrase


def _slug_from_slug_text(raw: str) -> str | None:
    phrase = " ".join(_SLUG_SPLIT.split(raw.replace("%20", " "))).strip()
    if not phrase:
        return None
    return phrase.title() if phrase.islower() else phrase


def format_product_link_for_prompt(link: ProductLinkInfo) -> str:
    lines = [
        "## Supplier / listing link",
        f"- URL: {link.url}",
        f"- Platform: {link.platform}",
    ]
    if link.listing_id:
        lines.append(f"- Listing ID: {link.listing_id}")
    if link.slug_hint:
        lines.append(f"- Title hint from URL: {link.slug_hint}")
    lines.append(
        "Use this listing as primary context for category, features, positioning, and sourcing signals. "
        "If the product name is brief, infer specifics from the URL and listing platform."
    )
    return "\n".join(lines)
