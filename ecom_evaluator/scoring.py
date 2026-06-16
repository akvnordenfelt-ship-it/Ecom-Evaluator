"""Shared scoring helpers for dashboard and exports."""

from __future__ import annotations

from dataclasses import dataclass

from ecom_evaluator.economics import EconomicsSnapshot


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
            "metric_logistics_margin must be **below 25**."
        )
    elif econ.contribution_margin_usd < 8:
        lines.append(
            f"- Contribution after shipping is only ${econ.contribution_margin_usd:.2f} — "
            "metric_logistics_margin should usually be **20–45**."
        )
    elif econ.gross_margin_pct >= 55 and econ.contribution_margin_usd >= 15:
        lines.append(
            f"- Strong unit economics (${econ.contribution_margin_usd:.2f} contribution) — "
            "metric_logistics_margin may reach **70–92** if shipping stays light."
        )

    if econ.gross_margin_pct < 25:
        lines.append(
            f"- Gross margin is only {econ.gross_margin_pct:.1f}% — "
            "do not score metric_logistics_margin above **45** without a sharp justification."
        )

    lines.append(
        "- metric_market_saturation: score **market opportunity** (100 = open niche, 0 = hyper-saturated red ocean)."
    )
    lines.append(
        "- If red_flag_analysis describes deal-breakers, at least two metrics must be **below 40**."
    )
    return "\n".join(lines)


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
