"""Markdown report generation and export helpers."""

from __future__ import annotations

import re

from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.scoring import verdict_label


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
) -> str:
    lines = [
        f"# Shark Tank Analysis — {product_name}",
        "",
        f"*Generated: {analyzed_at}*",
        "",
        f"## Final score: {result.final_score}/100",
        f"**Verdict:** {verdict_label(result.final_score)}",
        "",
        "## Market research analysis",
        "",
        result.market_research.executive_summary,
        "",
        f"- **Competition density:** {result.market_research.competitor_count_signal}",
        f"- **Demand level:** {result.market_research.demand_estimate.level}",
        f"- **Sales/demand note:** {result.market_research.demand_estimate.estimated_sales_note}",
        f"- **Demand reasoning:** {result.market_research.demand_estimate.reasoning}",
        "",
        f"**Amazon:** {result.market_research.amazon_landscape}",
        "",
        f"**AliExpress:** {result.market_research.aliexpress_landscape}",
        "",
        f"**Independent stores:** {result.market_research.independent_stores_landscape}",
        "",
        f"**Price range observed:** {result.market_research.price_range_observed}",
        "",
        "**Key competitors:**",
        "",
    ]
    if result.market_research.key_competitors:
        for comp in result.market_research.key_competitors:
            lines.append(
                f"- [{comp.platform}] {comp.listing_title} — {comp.source_url} "
                f"(price: {comp.price_signal}; similarity: {comp.similarity_note})"
            )
    else:
        lines.append("- None identified from search results.")
    lines.extend(
        [
            "",
            f"**Strategic implications:** {result.market_research.strategic_implications}",
            "",
            f"**Data limitations:** {result.market_research.data_limitations}",
            "",
            "## Score breakdown",
            "",
        ]
    )
    lines.extend(
        [
            f"- **Short-term potential:** {result.short_term_potential.score}/100",
            f"  {result.short_term_potential.motivation}",
            "",
            f"- **Long-term stability:** {result.long_term_stability.score}/100",
            f"  {result.long_term_stability.motivation}",
            "",
            f"- **Scalability:** {result.scalability.score}/100",
            f"  {result.scalability.motivation}",
            "",
            f"- **Marketing suitability:** {result.marketing_suitability.score}/100",
            f"  {result.marketing_suitability.motivation}",
            "",
            "## Market saturation",
            "",
            f"**{result.market_saturation.level}** — {result.market_saturation.motivation}",
            "",
        ]
    )
    web_research = (meta or {}).get("web_research") or []
    if web_research:
        lines.extend(["## Web research sources", ""])
        for hit in web_research:
            lines.append(f"- **[{hit['channel']}]** {hit['title']} — {hit['url']}")
            if hit.get("snippet"):
                lines.append(f"  {hit['snippet']}")
        lines.append("")

    plan = result.marketing_plan
    lines.extend(
        [
            "## Shipping & logistics",
            "",
            result.estimated_shipping_category,
            "",
            "## Marketing playbook",
            "",
            plan.executive_summary,
            "",
            "### Target audience",
            "",
            f"**{plan.target_audience.persona_name}** ({plan.target_audience.age_range})",
            "",
            plan.target_audience.psychographics,
            "",
            "**Pain points:** " + "; ".join(plan.target_audience.pain_points),
            "",
            "**Platforms they use:** " + ", ".join(plan.target_audience.platforms_they_use),
            "",
            "### Organic content",
            "",
            plan.organic_strategy.overview,
            "",
            f"**Cadence:** {plan.organic_strategy.posting_cadence}",
            "",
            "**Formats:** " + ", ".join(plan.organic_strategy.content_formats),
            "",
            "### Paid ads",
            "",
            plan.paid_ads_strategy.overview,
            "",
            f"**Starter budget:** {plan.paid_ads_strategy.budget_starter_usd}",
            "",
            f"**ROI outlook:** {plan.paid_ads_strategy.roi_outlook}",
            "",
            f"**Targeting:** {plan.paid_ads_strategy.targeting_approach}",
            "",
            "**Channels:** " + ", ".join(plan.paid_ads_strategy.primary_channels),
            "",
            "### Platform recommendations",
            "",
        ]
    )
    for plat in plan.platform_recommendations:
        lines.extend(
            [
                f"- **{plat.platform}** — fit {plat.fit_score}/100, ROI {plat.roi_potential}, "
                f"{plat.organic_vs_paid}",
                f"  {plat.why_it_works}",
                f"  *Competitor signal:* {plat.competitor_success_signal}",
                "",
            ]
        )
    lines.extend(
        [
            "### Competitor marketing insights",
            "",
            plan.competitor_marketing_insights,
            "",
            "### Creative concepts",
            "",
        ]
    )
    for concept in plan.creative_concepts:
        lines.extend(
            [
                f"**{concept.title}** ({concept.format} · {concept.recommended_platform})",
                "",
                f"*Angle:* {concept.hook_angle}",
                "",
                concept.script_or_copy,
                "",
            ]
        )
    lines.extend(["### Priority playbook", ""])
    for idx, step in enumerate(plan.priority_playbook, start=1):
        lines.append(f"{idx}. {step}")
    lines.extend(["", "## Go-to-market strategy", "", result.go_to_market_strategy, ""])
    return "\n".join(lines)
