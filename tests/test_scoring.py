"""Tests for scoring helpers."""

from ecom_evaluator.scoring import compute_overall_score, score_bar_color, verdict_label, verdict_status


def test_compute_overall_score_weighted():
    score = compute_overall_score(
        logistics=100,
        saturation=0,
        velocity=0,
        brandability=0,
        seasonality=0,
    )
    assert score == 30


def test_verdict_status_bands():
    assert verdict_status(85).label == "GO"
    assert verdict_status(65).label == "Caution"
    assert verdict_status(45).label == "High Risk"
    assert verdict_status(30).label == "Walk Away"


def test_verdict_label_bands():
    assert verdict_label(85) == "GO"
    assert verdict_label(8) == "Walk Away"


def test_compute_risk_score_from_severities():
    from ecom_evaluator.scoring import compute_risk_score, risk_tier_label

    score = compute_risk_score(["SEVERE", "HIGH", "LOW"])
    assert score == 43
    assert risk_tier_label(score) == "Moderate Risk"


def test_score_bar_color_bands():
    assert score_bar_color(80) == "#059669"
    assert score_bar_color(8) == "#dc2626"


def test_scoring_guidance_penalizes_negative_contribution():
    from ecom_evaluator.economics import compute_economics_snapshot
    from ecom_evaluator.scoring import format_scoring_guidance_for_prompt

    econ = compute_economics_snapshot(
        purchase_price=30.0,
        sales_price=32.0,
        weight_kg=2.0,
        length_cm=30,
        width_cm=20,
        height_cm=15,
    )
    guidance = format_scoring_guidance_for_prompt(econ)
    assert "below 25" in guidance or "20–45" in guidance
    assert "60–75" in guidance or "55–75" in guidance
