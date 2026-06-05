"""Shared scoring helpers for dashboard and exports."""

from __future__ import annotations

from ecom_evaluator.models import ScoredDimension


def verdict_label(score: int) -> str:
    if score >= 75:
        return "Strong opportunity"
    if score >= 55:
        return "Proceed with caution"
    if score >= 35:
        return "High risk"
    return "Not recommended"


def score_bar_color(score: int) -> str:
    if score >= 70:
        return "#059669"
    if score >= 40:
        return "#d97706"
    return "#dc2626"


def dimension_average(
    short_term: ScoredDimension,
    long_term: ScoredDimension,
    scalability: ScoredDimension,
    marketing: ScoredDimension,
) -> int:
    return round(
        (short_term.score + long_term.score + scalability.score + marketing.score) / 4
    )


def reconcile_final_score(
    llm_final: int | None,
    short_term: ScoredDimension,
    long_term: ScoredDimension,
    scalability: ScoredDimension,
    marketing: ScoredDimension,
) -> int:
    """Final score always matches the four dimension gauges."""
    return dimension_average(short_term, long_term, scalability, marketing)
