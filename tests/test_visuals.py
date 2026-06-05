"""Tests for dashboard chart helpers."""

from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.ui.visuals import make_dimension_radar_chart, make_platform_fit_chart
from tests.test_models import _sample_payload


def test_make_dimension_radar_chart():
    result = ProductEvaluationResponse.model_validate(_sample_payload())
    specs = [
        ("Short-term", result.short_term_potential),
        ("Long-term", result.long_term_stability),
        ("Scalability", result.scalability),
        ("Marketing", result.marketing_suitability),
    ]
    fig = make_dimension_radar_chart(specs)
    assert len(fig.data) == 1


def test_make_platform_fit_chart():
    result = ProductEvaluationResponse.model_validate(_sample_payload())
    fig = make_platform_fit_chart(result.marketing_plan.platform_recommendations)
    assert len(fig.data) == 1
