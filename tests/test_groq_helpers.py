"""Tests for Groq client helpers (no live API calls)."""

from ecom_evaluator.groq_client import (
    build_user_prompt,
    extract_json_text,
    is_transient_api_error,
    logistics_summary,
    select_model,
)


class _FakeStatusError(Exception):
    status_code = 503

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def test_is_transient_api_error_for_503():
    assert is_transient_api_error(_FakeStatusError("Service unavailable"))


def test_is_transient_api_error_for_401():
    err = _FakeStatusError("Unauthorized")
    err.status_code = 401
    assert not is_transient_api_error(err)


def test_logistics_summary_dimensional_weight():
    summary = logistics_summary(weight_kg=0.5, length_cm=30, width_cm=20, height_cm=10)
    assert summary["volume_cm3"] == 6000
    assert summary["dimensional_weight_kg"] == 1.2
    assert summary["billable_weight_kg"] == 1.2


def test_build_user_prompt_includes_product_and_research():
    prompt = build_user_prompt(
        product_name="Test Widget",
        purchase_price=5.0,
        sales_price=19.99,
        weight_kg=0.3,
        length_cm=10,
        width_cm=10,
        height_cm=5,
        description="A useful widget for creators.",
        has_image=False,
        web_research_text="## Live web research\n- Example hit",
    )
    assert "Test Widget" in prompt
    assert "Live web research" in prompt
    assert "$19.99" in prompt


def test_extract_json_text_strips_fence():
    raw = '```json\n{"final_score": 70}\n```'
    assert extract_json_text(raw) == '{"final_score": 70}'


def test_select_model_uses_vision_when_image():
    assert "scout" in select_model(has_image=True).lower()
    assert select_model(has_image=False) == "llama-3.3-70b-versatile"
