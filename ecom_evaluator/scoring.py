"""Shared scoring helpers for dashboard and exports."""

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
