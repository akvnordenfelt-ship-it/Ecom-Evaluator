"""Tests for product listing URL helpers."""

from ecom_evaluator.product_links import format_product_link_for_prompt, parse_product_url, validate_product_url


def test_parse_aliexpress_url_extracts_listing_id_and_slug():
    link = parse_product_url(
        "https://www.aliexpress.com/item/3300123456789-portable-usb-blender-cup.html"
    )
    assert link is not None
    assert link.platform == "AliExpress"
    assert link.listing_id == "3300123456789"
    assert "Portable Usb Blender Cup" in (link.slug_hint or "")


def test_parse_amazon_url_extracts_asin():
    link = parse_product_url("https://www.amazon.com/dp/B0ABCDEF12")
    assert link is not None
    assert link.platform == "Amazon"
    assert link.listing_id == "B0ABCDEF12"


def test_validate_product_url_allows_empty():
    link, error = validate_product_url("")
    assert link is None
    assert error is None


def test_validate_product_url_rejects_invalid():
    link, error = validate_product_url("not-a-url")
    assert link is None
    assert error is not None


def test_format_product_link_for_prompt_includes_platform():
    link = parse_product_url("https://www.aliexpress.com/item/1005006123456789.html")
    assert link is not None
    text = format_product_link_for_prompt(link)
    assert "AliExpress" in text
    assert link.url in text
