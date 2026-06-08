"""Markdown report generation."""

from __future__ import annotations

import re

from ecom_evaluator.plans import PlanTier, coerce_plan_tier
from ecom_evaluator.report_sections import has_section_access
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.scoring import verdict_status


def slugify_filename(name: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[\s_-]+", "_", slug).strip("_")
    return slug[:48] or "product"


def build_markdown_report(
    result: ProductEvaluationResponse,
    *,
    product_name: str,
    analyzed_at: str,
    meta: dict | None = None,
    tier: PlanTier | str = PlanTier.FREE,
) -> str:
    tier = coerce_plan_tier(tier)
    verdict = verdict_status(result.overall_score)
    lines = [
        f"# ProductScore — {product_name}",
        "",
        f"*Generated: {analyzed_at}*",
        "",
        f"## Section 1 — Overall score: {result.overall_score}/100",
        "",
        result.product_profile_summary,
        "",
        f"- Logistics & margin: {result.metric_logistics_margin}/100 — {result.metric_logistics_margin_note}",
        f"- Market saturation: {result.metric_market_saturation}/100 — {result.metric_market_saturation_note}",
        f"- Marketing velocity: {result.metric_marketing_velocity}/100 — {result.metric_marketing_velocity_note}",
        f"- Seasonality: {result.metric_seasonality}/100 — {result.metric_seasonality_note}",
        f"- Brandability: {result.metric_brandability}/100 — {result.metric_brandability_note}",
        "",
        "## Section 2 — Red flags",
        "",
        f"**{result.red_flag_headline}**",
        "",
        result.red_flag_analysis,
        "",
        f"1. {result.red_flag_1}",
        f"2. {result.red_flag_2}",
        f"3. {result.red_flag_3}",
        "",
    ]

    if has_section_access("margin_matrix", tier):
        lines.extend(
            [
                "## Section 3 — Verdict",
                "",
                f"**{verdict.emoji} {verdict.label}** — {verdict.subtitle} ({result.overall_score}/100)",
                "",
            ]
        )

    if result.has_marketing_teaser() and has_section_access("marketing_teaser", tier):
        lines.extend(
            [
                "## Section 4 — Marketing teaser",
                "",
                f"- Primary channel: {result.marketing_primary_channel}",
                f"- Hook index: {result.scroll_stopping_hook_index}/10",
                f"- Persona: {result.buyer_persona_hint}",
                "",
                result.marketing_teaser or "",
                "",
            ]
        )

    if result.has_web_intelligence():
        lines.extend(
            [
                "## Section 5 — Web intelligence",
                "",
                result.web_intelligence_summary or "",
                "",
                result.web_sourcing_links or "",
                "",
            ]
        )

    if result.has_marketing_deep_dive():
        lines.extend(
            [
                "## Section 6 — Marketing deep-dive",
                "",
                result.marketing_ad_scripts or "",
                "",
            ]
        )

    return "\n".join(lines)
