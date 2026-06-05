"""Tests for Gemini client helpers (no live API calls)."""

from ecom_evaluator.gemini_client import (
    build_product_context,
    extract_json_text,
    logistics_summary,
)


def test_extract_json_text_strips_fences():
    raw = '```json\n{"a": 1}\n```'
    assert extract_json_text(raw) == '{"a": 1}'


def test_logistics_summary():
    result = logistics_summary(0.5, 20, 15, 10)
    assert result["volume_dm3"] == 3.0
    assert result["billable_weight_kg"] == 0.6


def test_build_product_context_includes_computed_margin():
    text = build_product_context(
        product_name="Widget",
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
        description="Test product",
        has_image=False,
        web_research_text="## Live web research\nNone",
    )
    assert "Gross margin: $15.00" in text
    assert "Computed unit economics" in text
