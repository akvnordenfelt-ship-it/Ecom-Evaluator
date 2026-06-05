"""Tests for user-facing analysis error messages."""

from ecom_evaluator.ui.session import friendly_analysis_error


def test_incomplete_report_does_not_show_quota_tip():
    message = (
        "Product evaluation: incomplete report near ('market_research', 'amazon_landscape'). "
        "The model did not generate enough detail — try again."
    )
    result = friendly_analysis_error(message)
    assert "free API quota" not in result
    assert "auto-retries" in result.lower() or "run analysis" in result.lower()


def test_rate_limit_still_shows_quota_tip():
    message = "Groq rate limit: too many requests"
    result = friendly_analysis_error(message)
    assert "quota" in result.lower() or "try again later" in result.lower()
