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
    assert verdict_status(75).label == "GO"
    assert verdict_status(55).label == "PROCEED WITH CAUTION"
    assert verdict_status(40).label == "NO-GO"


def test_verdict_label_bands():
    assert verdict_label(80) == "GO"
    assert verdict_label(8) == "NO-GO"


def test_score_bar_color_bands():
    assert score_bar_color(80) == "#059669"
    assert score_bar_color(8) == "#dc2626"
