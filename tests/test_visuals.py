"""Tests for Plotly chart helpers."""

from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.ui.dashboard import make_metric_bars, make_overall_gauge
from tests.test_models import _sample_core_payload


def test_make_overall_gauge():
    result = ProductEvaluationResponse.model_validate(normalize_free_evaluation_payload(_sample_core_payload()))
    fig = make_overall_gauge(result.overall_score)
    assert fig.data[0].value == result.overall_score


def test_make_metric_bars():
    result = ProductEvaluationResponse.model_validate(normalize_free_evaluation_payload(_sample_core_payload()))
    fig = make_metric_bars(result)
    assert len(fig.data[0].x) == 5
