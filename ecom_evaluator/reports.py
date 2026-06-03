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

    lines.extend(
        [
            "## Shipping & logistics",
            "",
            result.estimated_shipping_category,
            "",
            "## TikTok creative concepts",
            "",
        ]
    )
    for i, hook in enumerate(result.tiktok_hooks, start=1):
        lines.extend(
            [
                f"### Hook {i}",
                "",
                f"**Hook:** {hook.hook_text}",
                "",
                f"**Visuals:** {hook.visuals}",
                "",
                f"**Voiceover:** {hook.voiceover}",
                "",
            ]
        )
    lines.extend(["## Go-to-market strategy", "", result.go_to_market_strategy, ""])
    return "\n".join(lines)
