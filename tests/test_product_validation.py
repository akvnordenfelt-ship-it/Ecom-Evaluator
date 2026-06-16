"""Tests for product name validation."""

from ecom_evaluator.product_links import parse_product_url
from ecom_evaluator.product_validation import validate_product_name


def test_rejects_non_product_single_word():
    result = validate_product_name("potato")
    assert not result.ok
    assert result.message is not None
    assert "potato" in result.message


def test_rejects_doodle():
    result = validate_product_name("doodle")
    assert not result.ok
    assert result.message is not None
    assert "doodle" in result.message
    assert "magnetic drawing board" in result.message or "specific" in result.message.lower()


def test_rejects_religious_or_random_single_word():
    assert not validate_product_name("jesus").ok
    assert not validate_product_name("asdfgh").ok


def test_accepts_specific_multi_word_product():
    assert validate_product_name("Wireless earbud cleaning kit").ok
    assert validate_product_name("Magnetic drawing board for kids").ok


def test_accepts_vague_name_when_listing_url_provided():
    link = parse_product_url("https://www.aliexpress.com/item/1005006123456789.html")
    assert link is not None
    assert validate_product_name("item", product_link=link).ok


def test_description_does_not_bypass_vague_single_word():
    assert not validate_product_name(
        "doodle",
        description="This is a doodle product for kids who like to draw.",
    ).ok


def test_rejects_two_generic_modifiers_only():
    assert not validate_product_name("smart wireless").ok


def test_rejects_vague_two_word_combo():
    assert not validate_product_name("cool gadget").ok
