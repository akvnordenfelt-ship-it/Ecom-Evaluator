"""Tests for dashboard chart helpers."""

from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.ui.dashboard import make_metric_bars, make_overall_gauge
from tests.test_models import _sample_payload
from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload


def test_make_overall_gauge():
    result = ProductEvaluationResponse.model_validate(normalize_free_evaluation_payload(_sample_payload()))
    fig = make_overall_gauge(result.overall_score)
    assert len(fig.data) == 1


def test_make_metric_bars():
    result = ProductEvaluationResponse.model_validate(normalize_free_evaluation_payload(_sample_payload()))
    fig = make_metric_bars(result)
    assert len(fig.data) == 1
