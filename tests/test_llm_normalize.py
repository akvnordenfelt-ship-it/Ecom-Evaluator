"""Tests for LLM payload normalization."""

from ecom_evaluator.llm_normalize import normalize_core_payload, normalize_evaluation_payload
from ecom_evaluator.models import ProductCoreResponse, ProductEvaluationResponse
from tests.test_models import _sample_payload


def test_coerce_competitor_count_signal_medium_to_moderate():
    payload = _sample_payload()
    payload["market_research"]["competitor_count_signal"] = "Medium"
    normalized = normalize_core_payload(payload)
    assert normalized["market_research"]["competitor_count_signal"] == "Moderate"


def test_coerce_lowercase_competitor_count():
    payload = _sample_payload()
    payload["market_research"]["competitor_count_signal"] = "many"
    normalized = normalize_core_payload(payload)
    assert normalized["market_research"]["competitor_count_signal"] == "Many"


def test_normalized_payload_validates():
    payload = _sample_payload()
    payload["market_research"]["competitor_count_signal"] = "high"
    payload["market_research"]["demand_estimate"]["level"] = "moderate"
    payload["market_saturation"]["level"] = "medium"
    result = ProductEvaluationResponse.model_validate(normalize_evaluation_payload(payload))
    assert result.market_research.competitor_count_signal == "Many"
    assert result.market_research.demand_estimate.level == "Medium"


def test_does_not_invent_fake_competitor_urls():
    payload = _sample_payload()
    payload["market_research"]["key_competitors"] = [
        {
            "platform": "Amazon",
            "listing_title": "",
            "source_url": "",
            "price_signal": "$10",
            "similarity_note": "Similar",
        }
    ]
    normalized = normalize_core_payload(payload)
    assert normalized["market_research"]["key_competitors"] == []


def test_core_payload_validates_from_sample():
    payload = _sample_payload()
    core = ProductCoreResponse.model_validate(normalize_core_payload(payload))
    assert core.final_score == 72
