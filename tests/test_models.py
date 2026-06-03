"""Tests for Pydantic evaluation models."""

import pytest
from pydantic import ValidationError

from ecom_evaluator.models import ProductEvaluationResponse


def _sample_payload() -> dict:
    return {
        "final_score": 72,
        "market_research": {
            "executive_summary": "Moderate competition with room to niche.",
            "competitor_count_signal": "Moderate",
            "amazon_landscape": "Several similar listings on Amazon.",
            "aliexpress_landscape": "Many low-cost alternatives on AliExpress.",
            "independent_stores_landscape": "Few DTC brands found.",
            "price_range_observed": "$15–$35",
            "demand_estimate": {
                "level": "Medium",
                "estimated_sales_note": "Steady search interest; no exact sales data.",
                "reasoning": "Multiple listings and review language suggest ongoing demand.",
            },
            "key_competitors": [],
            "strategic_implications": "Differentiate on brand and creative.",
            "data_limitations": "Search snippets only; no verified sales figures.",
        },
        "short_term_potential": {"score": 70, "motivation": "Good margin and trend fit."},
        "long_term_stability": {"score": 60, "motivation": "Risk of commoditization."},
        "scalability": {"score": 65, "motivation": "Fulfillment is straightforward."},
        "marketing_suitability": {"score": 80, "motivation": "Strong visual demo potential."},
        "market_saturation": {"level": "Medium", "motivation": "Crowded but not saturated."},
        "estimated_shipping_category": "Small parcel; billable weight ~0.4 kg.",
        "tiktok_hooks": [
            {"hook_text": "Hook A", "visuals": "Visual A", "voiceover": "Voice A"},
            {"hook_text": "Hook B", "visuals": "Visual B", "voiceover": "Voice B"},
            {"hook_text": "Hook C", "visuals": "Visual C", "voiceover": "Voice C"},
        ],
        "go_to_market_strategy": "## Phase 1\nTest hooks on TikTok.",
    }


def test_product_evaluation_response_validates():
    result = ProductEvaluationResponse.model_validate(_sample_payload())
    assert result.final_score == 72
    assert result.market_research.demand_estimate.level == "Medium"
    assert len(result.tiktok_hooks) == 3


def test_product_evaluation_rejects_invalid_score():
    payload = _sample_payload()
    payload["final_score"] = 101
    with pytest.raises(ValidationError):
        ProductEvaluationResponse.model_validate(payload)


def test_product_evaluation_json_roundtrip():
    result = ProductEvaluationResponse.model_validate(_sample_payload())
    restored = ProductEvaluationResponse.model_validate_json(result.model_dump_json())
    assert restored.final_score == result.final_score
