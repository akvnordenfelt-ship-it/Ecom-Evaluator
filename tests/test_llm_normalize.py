"""Tests for LLM payload normalization."""

from ecom_evaluator.llm_normalize import (
    normalize_competitor_sentiment_payload,
    normalize_free_evaluation_payload,
    normalize_marketing_teaser_payload,
)
from ecom_evaluator.models import CompetitorSentimentPayload, FreeCorePayload, ProductEvaluationResponse
from ecom_evaluator.scoring import compute_overall_score
from tests.test_models import _sample_core_payload, _sample_teaser_payload


def test_string_scores_normalize_to_integers():
    normalized = normalize_free_evaluation_payload(_sample_core_payload())
    assert normalized["metric_market_saturation"] == 55
    assert normalized["overall_score"] == compute_overall_score(85, 55, 78, 60, 70)


def test_overall_score_uses_weighted_formula():
    payload = _sample_core_payload()
    payload["metric_logistics_margin"] = "100"
    payload["metric_market_saturation"] = "0"
    payload["metric_marketing_velocity"] = "0"
    payload["metric_brandability"] = "0"
    payload["metric_seasonality"] = "0"
    normalized = normalize_free_evaluation_payload(payload)
    assert normalized["overall_score"] == 30


def test_validates_free_core_without_marketing():
    core = FreeCorePayload.model_validate(normalize_free_evaluation_payload(_sample_core_payload()))
    assert core.metric_logistics_margin == 85


def test_marketing_teaser_normalizes():
    teaser = normalize_marketing_teaser_payload(_sample_teaser_payload())
    full = ProductEvaluationResponse.model_validate(
        {**normalize_free_evaluation_payload(_sample_core_payload()), **teaser}
    )
    assert full.marketing_primary_channel == "TikTok Organic"


def test_competitor_sentiment_normalizes():
    payload = normalize_competitor_sentiment_payload(
        {
            "sentiment_executive_summary": "Buyers in this niche complain about brittle hinges and vague sizing.",
            "sentiment_pain_points": [
                {
                    "category": "Quality / Durability",
                    "negative_trend": "Hinges snap within weeks.",
                    "anger_frustration_index": "88",
                    "review_evidence": "Low-star reviews mention broken joints after light use.",
                }
            ],
            "sentiment_improvement_directives": [
                {
                    "linked_category": "Quality / Durability",
                    "engineering_directive": "Switch to glass-filled nylon hinges with a 50-cycle QC pull test.",
                    "roi_badge": "High ROI Improvement",
                }
            ],
            "sentiment_shopify_hooks": [
                {
                    "angle": "Built to last",
                    "copy_block": "Unlike flimsy alternatives, our reinforced hinge survives daily use.",
                }
            ],
        }
    )
    model = CompetitorSentimentPayload.model_validate(payload)
    assert len(model.sentiment_pain_points) == 3
    assert model.sentiment_pain_points[0].anger_frustration_index == 88
    assert model.sentiment_improvement_directives[0].roi_badge == "High ROI Improvement"
    assert len(model.sentiment_shopify_hooks) >= 2
