"""Tests for report export."""

from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload, normalize_marketing_teaser_payload
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.reports import build_markdown_report, slugify_filename
from tests.test_models import _sample_core_payload, _sample_teaser_payload


def test_slugify_filename():
    assert slugify_filename("Silicone Spatula Set!") == "silicone_spatula_set"


def test_build_markdown_report_contains_sections():
    payload = {
        **normalize_free_evaluation_payload(_sample_core_payload()),
        **normalize_marketing_teaser_payload(_sample_teaser_payload()),
    }
    result = ProductEvaluationResponse.model_validate(payload)
    md = build_markdown_report(
        result,
        product_name="Test Widget",
        analyzed_at="2026-06-02T12:00:00+00:00",
    )
    assert "# ProductScore — Test Widget" in md
    assert "## Section 2 — Red flags" in md
    assert "## Section 3 — Verdict" in md
    assert "## Section 4 — Marketing teaser" in md
