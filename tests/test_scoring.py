"""Tests for scoring helpers."""

from ecom_evaluator.scoring import score_bar_color, verdict_label


def test_verdict_label_bands():
    assert verdict_label(80) == "Strong opportunity"
    assert verdict_label(8) == "Not recommended"


def test_score_bar_color_bands():
    assert score_bar_color(80) == "#059669"
    assert score_bar_color(8) == "#dc2626"
