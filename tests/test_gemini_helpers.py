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
    assert "Web research" not in text or "Not available" in text
