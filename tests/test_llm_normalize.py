"""Tests for LLM payload normalization."""

from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload
from ecom_evaluator.models import ProductEvaluationResponse
from tests.test_models import _sample_payload


def test_string_scores_normalize_to_integers():
    normalized = normalize_free_evaluation_payload(_sample_payload())
    assert normalized["metric_market_saturation"] == 55
    assert normalized["overall_score"] == 70


def test_overall_score_tracks_metric_average():
    payload = _sample_payload()
    payload["overall_score"] = "99"
    payload["metric_market_saturation"] = "10"
    payload["metric_marketing_velocity"] = "10"
    payload["metric_logistics_margin"] = "10"
    payload["metric_seasonality"] = "10"
    payload["metric_brandability"] = "10"
    normalized = normalize_free_evaluation_payload(payload)
    assert normalized["overall_score"] == 10


def test_validates_from_sample():
    core = ProductEvaluationResponse.model_validate(normalize_free_evaluation_payload(_sample_payload()))
    assert core.marketing_primary_channel == "TikTok Organic"
