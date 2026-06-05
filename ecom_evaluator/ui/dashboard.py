"""Plotly dashboard and export UI."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone

import plotly.graph_objects as go
import streamlit as st

from ecom_evaluator.config import PLOTLY_CHART_CONFIG
from ecom_evaluator.models import MarketResearchAnalysis, MarketSearchHit, MarketingPlan, ProductEvaluationResponse
from ecom_evaluator.reports import build_markdown_report, slugify_filename
from ecom_evaluator.scoring import score_bar_color, verdict_label
from ecom_evaluator.ui.visuals import (
    CHANNEL_VISUALS,
    ROI_COLORS,
    make_competition_gauge,
    make_demand_gauge,
    make_dimension_radar_chart,
    make_organic_paid_chart,
    make_platform_fit_chart,
    platform_color,
    platform_emoji,
    platform_icon_url,
)


def make_score_gauge(title: str, score: int, *, height: int = 220, title_size: int = 14) -> go.Figure:
    bar_color = score_bar_color(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100", "font": {"size": 26, "color": "#0f172a"}},
            title={"text": title, "font": {"size": title_size, "color": "#334155"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#94a3b8"},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "#f8fafc",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#d1fae5"},
                ],
                "threshold": {
                    "line": {"color": "#0f172a", "width": 2},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=56, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Segoe UI, system-ui, sans-serif", "color": "#334155"},
    )
    return fig


def saturation_badge_html(level: str) -> str:
    palette = {
        "Low": ("#065f46", "#ecfdf5", "#6ee7b7"),
        "Medium": ("#92400e", "#fffbeb", "#fcd34d"),
        "High": ("#991b1b", "#fef2f2", "#fca5a5"),
    }
    text_color, bg, border = palette.get(level, ("#334155", "#f1f5f9", "#cbd5e1"))
    return (
        f'<span class="saturation-badge" style="color:{text_color};background:{bg};'
        f'border:1px solid {border};">{level}</span>'
    )


def roi_badge_html(level: str) -> str:
    color = ROI_COLORS.get(level, "#64748B")
    return (
        f'<span class="metric-pill" style="background:{color}22;color:{color};'
        f'border:1px solid {color}55;">ROI {html.escape(level)}</span>'
    )


def channel_icon_url(label: str) -> str:
    meta = CHANNEL_VISUALS.get(label, {"slug": "googlechrome", "color": "#64748B"})
    return f"https://cdn.simpleicons.org/{meta['slug']}/{meta['color'].lstrip('#')}"


def channel_header_html(label: str) -> str:
    meta = CHANNEL_VISUALS.get(label, {"emoji": "🌐", "color": "#64748B", "slug": "googlechrome"})
    icon = channel_icon_url(label)
    return (
        f'<div class="channel-head">'
        f'<img class="channel-logo" src="{icon}" alt="{html.escape(label)}" '
        f'onerror="this.style.display=\'none\'"/>'
        f'<span class="channel-emoji">{meta["emoji"]}</span>'
        f'<span class="channel-name">{html.escape(label)}</span></div>'
    )


def render_market_research_section(
    analysis: MarketResearchAnalysis,
    raw_hits: list[MarketSearchHit] | list[dict],
) -> None:
    st.markdown("### Market research analysis")
    st.caption("Live DuckDuckGo research · synthesized by Gemini")

    gauge_col, summary_col = st.columns([1, 2])
    with gauge_col:
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(
                make_competition_gauge(analysis.competitor_count_signal),
                use_container_width=True,
                config=PLOTLY_CHART_CONFIG,
            )
        with g2:
            st.plotly_chart(
                make_demand_gauge(analysis.demand_estimate.level),
                use_container_width=True,
                config=PLOTLY_CHART_CONFIG,
            )
    with summary_col:
        st.markdown(
            f'<div class="insight-card insight-card--hero">'
            f'<p class="card-kicker">Executive summary</p>'
            f"<p>{html.escape(analysis.executive_summary)}</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Demand note:** {html.escape(analysis.demand_estimate.estimated_sales_note)}",
            unsafe_allow_html=True,
        )

    st.markdown("#### Channel breakdown")
    channel_cols = st.columns(3)
    channel_blocks = [
        ("Amazon", analysis.amazon_landscape),
        ("AliExpress", analysis.aliexpress_landscape),
        ("Independent stores", analysis.independent_stores_landscape),
    ]
    for col, (label, text) in zip(channel_cols, channel_blocks, strict=True):
        with col:
            st.markdown(channel_header_html(label), unsafe_allow_html=True)
            st.markdown(
                f'<div class="research-channel-card">{html.escape(text)}</div>',
                unsafe_allow_html=True,
            )

    price_col, demand_col = st.columns(2)
    with price_col:
        st.markdown(
            '<div class="stat-tile"><p class="stat-tile-label">💰 Price range observed</p>'
            f"<p class=\"stat-tile-value\">{html.escape(analysis.price_range_observed)}</p></div>",
            unsafe_allow_html=True,
        )
    with demand_col:
        st.markdown(
            '<div class="stat-tile"><p class="stat-tile-label">📈 Demand reasoning</p>'
            f"<p class=\"stat-tile-body\">{html.escape(analysis.demand_estimate.reasoning)}</p></div>",
            unsafe_allow_html=True,
        )

    if analysis.key_competitors:
        st.markdown("#### Key competitors identified")
        for comp in analysis.key_competitors:
            st.markdown(
                f'<div class="competitor-row">'
                f'<span class="metric-pill">{html.escape(comp.platform)}</span> '
                f'<a href="{html.escape(comp.source_url)}">{html.escape(comp.listing_title)}</a>'
                f'<p class="competitor-meta"><strong>Price:</strong> {html.escape(comp.price_signal)} · '
                f"<strong>Similarity:</strong> {html.escape(comp.similarity_note)}</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown("**Strategic implications**")
    st.markdown(
        f'<div class="insight-card">{html.escape(analysis.strategic_implications)}</div>',
        unsafe_allow_html=True,
    )
    st.warning(f"Data limitations: {analysis.data_limitations}")

    with st.expander(f"Raw search sources ({len(raw_hits)} DuckDuckGo results)", expanded=False):
        if not raw_hits:
            st.caption("No raw search results were captured for this run.")
        else:
            for hit in raw_hits:
                channel = hit.get("channel", "Web")
                title = hit.get("title", "")
                url = hit.get("url", "")
                st.markdown(f"**[{channel}]** [{title}]({url})")
                if hit.get("snippet"):
                    st.caption(hit["snippet"])
                st.caption(f"Query: `{hit.get('query', '')}`")
                st.divider()


def render_marketing_section(plan: MarketingPlan) -> None:
    st.markdown("### Marketing playbook")
    st.caption("Organic content · paid ads · platform mix · audience fit")

    st.markdown(
        f'<div class="insight-card insight-card--hero insight-card--marketing">'
        f'<p class="card-kicker">How to market this product</p>'
        f"<p>{html.escape(plan.executive_summary)}</p></div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Target audience")
    aud = plan.target_audience
    aud_left, aud_right = st.columns([1.1, 1])
    with aud_left:
        st.markdown(
            f'<div class="persona-card">'
            f'<p class="persona-icon">👤</p>'
            f'<p class="persona-name">{html.escape(aud.persona_name)}</p>'
            f'<p class="persona-meta">Age {html.escape(aud.age_range)}</p>'
            f'<p class="persona-body">{html.escape(aud.psychographics)}</p></div>',
            unsafe_allow_html=True,
        )
    with aud_right:
        st.markdown("**Pain points**")
        for point in aud.pain_points:
            st.markdown(f"- {point}")
        st.markdown("**Where they spend time**")
        chip_html = " ".join(
            f'<span class="platform-chip">{platform_emoji(p)} {html.escape(p)}</span>'
            for p in aud.platforms_they_use
        )
        st.markdown(f'<div class="chip-row">{chip_html}</div>', unsafe_allow_html=True)

    st.markdown("#### Organic vs paid")
    mix_col, organic_col, paid_col = st.columns([1, 1.2, 1.2])
    with mix_col:
        st.plotly_chart(
            make_organic_paid_chart(plan),
            use_container_width=True,
            config=PLOTLY_CHART_CONFIG,
        )
    with organic_col:
        org = plan.organic_strategy
        st.markdown(
            '<div class="strategy-card strategy-card--organic">'
            '<p class="strategy-card-title">🌱 Organic content</p>'
            f"<p>{html.escape(org.overview)}</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**Cadence:** {org.posting_cadence}")
        for fmt in org.content_formats:
            st.markdown(f'<span class="format-chip">{html.escape(fmt)}</span>', unsafe_allow_html=True)
        with st.expander("Creator angles"):
            for angle in org.creator_angles:
                st.markdown(f"- {angle}")
    with paid_col:
        paid = plan.paid_ads_strategy
        st.markdown(
            '<div class="strategy-card strategy-card--paid">'
            '<p class="strategy-card-title">💳 Paid ads</p>'
            f"<p>{html.escape(paid.overview)}</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**Starter budget:** {paid.budget_starter_usd}")
        st.markdown(f"**ROI outlook:** {roi_badge_html(paid.roi_outlook)}", unsafe_allow_html=True)
        st.markdown(f"**Targeting:** {paid.targeting_approach}")
        st.markdown("**Channels:** " + ", ".join(paid.primary_channels))

    st.markdown("#### Best platforms for this product")
    st.plotly_chart(
        make_platform_fit_chart(plan.platform_recommendations),
        use_container_width=True,
        config=PLOTLY_CHART_CONFIG,
    )

    plat_cols = st.columns(min(len(plan.platform_recommendations), 3))
    for col, plat in zip(plat_cols, plan.platform_recommendations[:3], strict=False):
        with col:
            icon = platform_icon_url(plat.platform)
            st.markdown(
                f'<div class="platform-card" style="border-top: 4px solid {platform_color(plat.platform)};">'
                f'<div class="platform-card-head">'
                f'<img class="platform-logo" src="{icon}" alt="{html.escape(plat.platform)}" '
                f'onerror="this.style.display=\'none\'"/>'
                f'<span>{platform_emoji(plat.platform)}</span>'
                f"<strong>{html.escape(plat.platform)}</strong></div>"
                f'<p class="platform-score">{plat.fit_score}/100 fit · {html.escape(plat.organic_vs_paid)}</p>'
                f"{roi_badge_html(plat.roi_potential)}"
                f"<p class=\"platform-body\">{html.escape(plat.why_it_works)}</p>"
                f'<p class="platform-evidence"><em>Competitor signal:</em> '
                f"{html.escape(plat.competitor_success_signal)}</p></div>",
                unsafe_allow_html=True,
            )

    st.markdown("#### What competitors did best")
    st.markdown(
        f'<div class="insight-card">{html.escape(plan.competitor_marketing_insights)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Creative concepts to test first")
    concept_cols = st.columns(2)
    for col, concept in zip(concept_cols, plan.creative_concepts[:4], strict=False):
        with col:
            st.markdown(
                f'<div class="creative-card">'
                f'<p class="creative-format">{html.escape(concept.format)} · '
                f"{html.escape(concept.recommended_platform)}</p>"
                f'<p class="creative-title">{html.escape(concept.title)}</p>'
                f'<p class="creative-hook"><strong>Angle:</strong> {html.escape(concept.hook_angle)}</p>'
                f'<p class="creative-copy">{html.escape(concept.script_or_copy)}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown("#### Priority playbook — do this first")
    for idx, step in enumerate(plan.priority_playbook, start=1):
        st.markdown(
            f'<div class="playbook-step">'
            f'<span class="playbook-num">{idx}</span>'
            f"<span>{html.escape(step)}</span></div>",
            unsafe_allow_html=True,
        )


def render_dashboard(result: ProductEvaluationResponse, meta: dict | None = None) -> None:
    st.markdown(
        '<div class="status-banner status-banner--success">Evaluation complete · Gemini 2.5 Flash + live market research</div>',
        unsafe_allow_html=True,
    )

    if meta:
        analyzed_at = meta.get("analyzed_at", "")
        product_name = meta.get("product_name", "Product")
        if analyzed_at:
            st.markdown(
                f'<p class="report-meta">Report · <strong>{html.escape(product_name)}</strong> · '
                f'{analyzed_at[:19].replace("T", " ")} UTC</p>',
                unsafe_allow_html=True,
            )
        render_export_buttons(result, meta)

    st.markdown('<p class="section-eyebrow">Overview</p>', unsafe_allow_html=True)
    st.markdown("### Investment verdict")
    verdict_col, insight_col = st.columns([1.1, 1])

    with verdict_col:
        st.plotly_chart(
            make_score_gauge("Final investment score", result.final_score, height=300, title_size=16),
            use_container_width=True,
            config=PLOTLY_CHART_CONFIG,
        )

    with insight_col:
        st.markdown(
            f'<p class="verdict-label">{verdict_label(result.final_score)}</p>',
            unsafe_allow_html=True,
        )
        metric_a, metric_b = st.columns(2)
        with metric_a:
            st.markdown("#### Market saturation")
            st.markdown(saturation_badge_html(result.market_saturation.level), unsafe_allow_html=True)
            st.caption(result.market_saturation.motivation)
        with metric_b:
            st.markdown("#### Marketing fit")
            st.plotly_chart(
                make_score_gauge("Marketing", result.marketing_suitability.score, height=160, title_size=12),
                use_container_width=True,
                config=PLOTLY_CHART_CONFIG,
            )

        st.markdown("#### Shipping & logistics")
        st.markdown(
            f'<div class="insight-card">📦 {html.escape(result.estimated_shipping_category)}</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown('<p class="section-eyebrow">Market intelligence</p>', unsafe_allow_html=True)
    raw_hits = (meta or {}).get("web_research") or []
    render_market_research_section(result.market_research, raw_hits)

    st.divider()
    st.markdown('<p class="section-eyebrow">Scorecard</p>', unsafe_allow_html=True)
    st.markdown("### Dimension scores")

    dimension_specs = [
        ("Short-term potential", result.short_term_potential),
        ("Long-term stability", result.long_term_stability),
        ("Scalability", result.scalability),
        ("Marketing suitability", result.marketing_suitability),
    ]

    radar_col, gauge_col = st.columns([1, 1.4])
    with radar_col:
        st.plotly_chart(
            make_dimension_radar_chart(dimension_specs),
            use_container_width=True,
            config=PLOTLY_CHART_CONFIG,
        )
    with gauge_col:
        row1 = st.columns(2)
        row2 = st.columns(2)
        for col, (label, dim) in zip(
            (row1[0], row1[1], row2[0], row2[1]), dimension_specs, strict=True
        ):
            with col:
                st.plotly_chart(
                    make_score_gauge(label, dim.score, height=200, title_size=11),
                    use_container_width=True,
                    config=PLOTLY_CHART_CONFIG,
                )

    st.markdown("#### Panel rationale")
    rationale_cols = st.columns(2)
    for idx, (label, dim) in enumerate(dimension_specs):
        with rationale_cols[idx % 2]:
            with st.expander(f"{label} — {dim.score}/100", expanded=False):
                st.markdown(dim.motivation)

    st.divider()
    st.markdown('<p class="section-eyebrow">Marketing</p>', unsafe_allow_html=True)
    render_marketing_section(result.marketing_plan)

    st.divider()
    st.markdown('<p class="section-eyebrow">Operations</p>', unsafe_allow_html=True)
    st.markdown("### Go-to-market plan")
    with st.container(border=True):
        st.markdown(result.go_to_market_strategy)

    with st.expander("Raw JSON (Pydantic-validated)"):
        st.json(result.model_dump())


def render_export_buttons(result: ProductEvaluationResponse, meta: dict) -> None:
    product_name = meta.get("product_name", "product")
    analyzed_at = meta.get("analyzed_at", datetime.now(timezone.utc).isoformat())
    slug = slugify_filename(product_name)
    timestamp = analyzed_at[:10]

    json_payload = json.dumps(result.model_dump(), indent=2, ensure_ascii=False)
    markdown_payload = build_markdown_report(
        result, product_name=product_name, analyzed_at=analyzed_at, meta=meta
    )

    col_json, col_md, col_clear = st.columns([1, 1, 1])
    with col_json:
        st.download_button(
            label="Download JSON",
            data=json_payload,
            file_name=f"{slug}_analysis_{timestamp}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_md:
        st.download_button(
            label="Download Markdown report",
            data=markdown_payload,
            file_name=f"{slug}_analysis_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_clear:
        if st.button("Clear results", use_container_width=True):
            st.session_state["analysis_result"] = None
            st.session_state["analysis_meta"] = None
            st.session_state["market_research"] = None
            st.rerun()
