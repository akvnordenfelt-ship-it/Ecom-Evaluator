"""Shared scoring helpers for dashboard and exports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from ecom_evaluator.economics import EconomicsSnapshot

Severity = Literal["SEVERE", "HIGH", "MEDIUM", "LOW"]
SEVERITY_POINTS: dict[str, int] = {
    "SEVERE": 25,
    "HIGH": 15,
    "MEDIUM": 8,
    "LOW": 3,
}


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


def compute_confidence_percentage(*, input_count: int, max_inputs: int = 8) -> int:
    """Higher when more product inputs were provided."""
    if max_inputs <= 0:
        return 50
    return max(25, min(98, round((input_count / max_inputs) * 100)))


def compute_risk_score(severities: list[str]) -> int:
    """Section 2 risk score from flag severities — computed in Python."""
    total = 0
    for severity in severities:
        total += SEVERITY_POINTS.get(str(severity).upper(), 0)
    return min(100, total)


def risk_tier_label(risk_score: int) -> str:
    if risk_score <= 30:
        return "Low Risk"
    if risk_score <= 55:
        return "Moderate Risk"
    if risk_score <= 75:
        return "High Risk"
    return "Very High Risk"


def format_scoring_guidance_for_prompt(econ: EconomicsSnapshot) -> str:
    """Deterministic anchors so the LLM does not cluster every product in the 60–80 band."""
    lines = [
        "## Scoring anchors (mandatory — higher = better for the seller on every metric)",
        "- Use the full 0–100 range. Most products are NOT winners — score low without hesitation when warranted.",
        "- Do NOT cluster all five metrics between 55–75 unless the product is genuinely average on every axis.",
        "- Exceptional winner (clear edge + economics): 82–96 on strongest metrics.",
        "- Solid but competitive: 62–78 on strengths, 40–58 on weaknesses.",
        "- Mediocre / commoditized: 35–52.",
        "- Structurally weak (bad margins, saturated, fad, compliance risk): 8–32.",
    ]

    if econ.contribution_margin_usd <= 0:
        lines.append(
            f"- Contribution after shipping is ${econ.contribution_margin_usd:.2f} — "
            "logistics_score must be **below 25**."
        )
    elif econ.contribution_margin_usd < 8:
        lines.append(
            f"- Contribution after shipping is only ${econ.contribution_margin_usd:.2f} — "
            "logistics_score should usually be **20–45**."
        )
    elif econ.gross_margin_pct >= 55 and econ.contribution_margin_usd >= 15:
        lines.append(
            f"- Strong unit economics (${econ.contribution_margin_usd:.2f} contribution) — "
            "logistics_score may reach **70–92** if shipping stays light."
        )

    if econ.gross_margin_pct < 25:
        lines.append(
            f"- Gross margin is only {econ.gross_margin_pct:.1f}% — "
            "do not score logistics_score above **45** without a sharp justification."
        )

    lines.append(
        "- saturation_score: score **market opportunity** (100 = open niche, 0 = hyper-saturated red ocean)."
    )
    lines.append(
        "- If flags describe deal-breakers, at least two sub-scores must be **below 40**."
    )
    return "\n".join(lines)


def verdict_status(score: int) -> VerdictStatus:
    if score >= 90:
        return VerdictStatus(
            emoji="🟢",
            label="Strong GO",
            subtitle="High conviction opportunity",
            css_class="go",
        )
    if score >= 80:
        return VerdictStatus(
            emoji="🟢",
            label="GO",
            subtitle="Solid fundamentals",
            css_class="go",
        )
    if score >= 60:
        return VerdictStatus(
            emoji="🟡",
            label="Caution",
            subtitle="Validate before scaling",
            css_class="caution",
        )
    if score >= 40:
        return VerdictStatus(
            emoji="🟠",
            label="High Risk",
            subtitle="Major concerns to resolve",
            css_class="caution",
        )
    return VerdictStatus(
        emoji="🔴",
        label="Walk Away",
        subtitle="Fundamentals too weak",
        css_class="nogo",
    )


def verdict_label(score: int) -> str:
    return verdict_status(score).label


def score_bar_color(score: int) -> str:
    if score >= 80:
        return "#059669"
    if score >= 60:
        return "#d97706"
    if score >= 40:
        return "#ea580c"
    return "#dc2626"
