"""Tests for Pydantic evaluation models."""

import pytest
from pydantic import ValidationError

from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload, normalize_marketing_teaser_payload
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.scoring import compute_overall_score


def _sample_core_payload() -> dict:
    return {
        "product_profile_summary": "Compact kitchen gadget with strong visual demo potential.",
        "physical_weight_assessment": "Lightweight unit suitable for small-parcel shipping.",
        "fragility_assessment": "Low fragility — rigid plastic construction.",
        "variant_complexity": "Single SKU with optional color variants.",
        "shipping_complexity": "Standard parcel; no oversized dimensional weight risk.",
        "metric_market_saturation": "55",
        "metric_market_saturation_note": "Moderate category crowding from generic listings.",
        "metric_marketing_velocity": "78",
        "metric_marketing_velocity_note": "High TikTok organic potential with demo-friendly visuals.",
        "metric_logistics_margin": "85",
        "metric_logistics_margin_note": "Strong markup relative to weight and size.",
        "metric_seasonality": "70",
        "metric_seasonality_note": "Year-round utility with mild Q4 gift lift.",
        "metric_brandability": "60",
        "metric_brandability_note": "Brandable with consistent creative, but not inherently unique IP.",
        "red_flag_headline": "Three risks before you scale",
        "red_flag_analysis": "Margin is healthy but differentiation and ad costs could compress returns.",
        "red_flag_1": "Amazon race-to-the-bottom pricing on similar SKUs.",
        "red_flag_2": "Return risk if sizing or expectations mismatch listing copy.",
        "red_flag_3": "Paid CAC may exceed break-even if creative fatigue hits quickly.",
    }


def _sample_teaser_payload() -> dict:
    return {
        "marketing_primary_channel": "TikTok Organic",
        "scroll_stopping_hook_index": "8",
        "buyer_persona_hint": "Millennial home-cook who loves compact kitchen wins.",
        "marketing_teaser": "Lead with a 3-second problem hook and overhead demo; paid retargeting second.",
    }


def test_product_evaluation_validates():
    core = normalize_free_evaluation_payload(_sample_core_payload())
    result = ProductEvaluationResponse.model_validate(core)
    expected = compute_overall_score(85, 55, 78, 60, 70)
    assert result.overall_score == expected


def test_rejects_invalid_hook_index():
    payload = {
        **normalize_free_evaluation_payload(_sample_core_payload()),
        **normalize_marketing_teaser_payload(_sample_teaser_payload()),
    }
    payload["scroll_stopping_hook_index"] = 11
    with pytest.raises(ValidationError):
        ProductEvaluationResponse.model_validate(payload)
