"""Shared scoring helpers for dashboard and exports."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VerdictStatus:
    emoji: str
    label: str
    subtitle: str
    css_class: str


def compute_overall_score(
    logistics: int,
    saturation: int,
    velocity: int,
    brandability: int,
    seasonality: int,
) -> int:
    """Weighted overall score — computed in Python, never from the LLM."""
    raw = (
        logistics * 0.30
        + saturation * 0.25
        + velocity * 0.20
        + brandability * 0.15
        + seasonality * 0.10
    )
    return max(0, min(100, round(raw)))


def verdict_status(score: int) -> VerdictStatus:
    if score >= 70:
        return VerdictStatus(
            emoji="🟢",
            label="GO",
            subtitle="High potential, solid foundation",
            css_class="go",
        )
    if score >= 50:
        return VerdictStatus(
            emoji="🟡",
            label="PROCEED WITH CAUTION",
            subtitle="Viable, but check the Red Flags",
            css_class="caution",
        )
    return VerdictStatus(
        emoji="🔴",
        label="NO-GO",
        subtitle="High risk or weak margins",
        css_class="nogo",
    )


def verdict_label(score: int) -> str:
    return verdict_status(score).label


def score_bar_color(score: int) -> str:
    if score >= 70:
        return "#059669"
    if score >= 40:
        return "#d97706"
    return "#dc2626"
