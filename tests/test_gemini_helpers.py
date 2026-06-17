"""Tests for Gemini client helpers (no live API calls)."""

from ecom_evaluator.gemini_client import build_input_context, extract_json_text


def test_extract_json_text_strips_fences():
    raw = '```json\n{"a": "1"}\n```'
    assert extract_json_text(raw) == '{"a": "1"}'


def test_build_input_context_includes_computed_margin():
    text = build_input_context(
        product_name="Widget",
        purchase_price=0.10,
        sales_price=10.0,
        weight_kg=0.05,
        length_cm=10,
        width_cm=8,
        height_cm=3,
        description="Hair tie bundle",
        has_image=False,
    )
    assert "Gross margin:" in text
    assert "Computed economics" in text
    assert "Scoring anchors" in text
    assert "Web research" not in text or "Not available" in text


def test_build_input_context_includes_listing_link():
    from ecom_evaluator.product_links import parse_product_url

    link = parse_product_url("https://www.aliexpress.com/item/1005006123456789.html")
    text = build_input_context(
        product_name="USB blender",
        purchase_price=8.0,
        sales_price=24.0,
        weight_kg=0.4,
        length_cm=10,
        width_cm=8,
        height_cm=8,
        description="",
        has_image=False,
        product_link=link,
    )
    assert link is not None
    assert "Supplier / listing link" in text
    assert link.url in text
