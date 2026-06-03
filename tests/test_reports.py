"""Tests for report and scoring utilities."""

from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.reports import build_markdown_report, slugify_filename
from ecom_evaluator.scoring import score_bar_color, verdict_label
from tests.test_models import _sample_payload


def test_slugify_filename():
    assert slugify_filename("Silicone Spatula Set!") == "silicone_spatula_set"


def test_verdict_label_bands():
    assert verdict_label(80) == "Strong opportunity"
    assert verdict_label(60) == "Proceed with caution"
    assert verdict_label(20) == "Not recommended"


def test_score_bar_color_bands():
    assert score_bar_color(80) == "#059669"
    assert score_bar_color(50) == "#d97706"
    assert score_bar_color(20) == "#dc2626"


def test_build_markdown_report_contains_sections():
    result = ProductEvaluationResponse.model_validate(_sample_payload())
    md = build_markdown_report(
        result,
        product_name="Test Widget",
        analyzed_at="2026-06-02T12:00:00+00:00",
    )
    assert "# Shark Tank Analysis — Test Widget" in md
    assert "## Market research analysis" in md
    assert "## Go-to-market strategy" in md
