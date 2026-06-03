"""Plotly dashboard and export UI."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone

import plotly.graph_objects as go
import streamlit as st

from ecom_evaluator.config import PLOTLY_CHART_CONFIG
from ecom_evaluator.models import MarketResearchAnalysis, MarketSearchHit, ProductEvaluationResponse
from ecom_evaluator.reports import build_markdown_report, slugify_filename
from ecom_evaluator.scoring import score_bar_color, verdict_label


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


def demand_badge_html(level: str) -> str:
    palette = {
        "Low": ("#065f46", "#ecfdf5", "#6ee7b7"),
        "Medium": ("#92400e", "#fffbeb", "#fcd34d"),
        "High": ("#991b1b", "#fef2f2", "#fca5a5"),
        "Unknown": ("#334155", "#f1f5f9", "#cbd5e1"),
    }
    text_color, bg, border = palette.get(level, palette["Unknown"])
    return (
        f'<span class="saturation-badge" style="color:{text_color};background:{bg};'
        f'border:1px solid {border};">{level}</span>'
    )


def render_market_research_section(
    analysis: MarketResearchAnalysis,
    raw_hits: list[MarketSearchHit] | list[dict],
) -> None:
    """Dedicated dashboard section for Gemini's web research analysis."""
    st.markdown("### Market research analysis")
    st.caption("Based on live DuckDuckGo searches — analyzed by Gemini, not raw data.")

    summary_col, signal_col = st.columns([2, 1])
    with summary_col:
        st.markdown(
            f'<div class="insight-card">{html.escape(analysis.executive_summary)}</div>',
            unsafe_allow_html=True,
        )
    with signal_col:
        st.markdown("**Competition density**")
        st.markdown(demand_badge_html(analysis.competitor_count_signal), unsafe_allow_html=True)
        st.markdown("**Demand estimate**")
        st.markdown(demand_badge_html(analysis.demand_estimate.level), unsafe_allow_html=True)
        st.caption(analysis.demand_estimate.estimated_sales_note)

    st.markdown("#### Channel breakdown")
    channel_cols = st.columns(3)
    channel_blocks = [
        ("Amazon", analysis.amazon_landscape),
        ("AliExpress", analysis.aliexpress_landscape),
        ("Independent stores", analysis.independent_stores_landscape),
    ]
    for col, (label, text) in zip(channel_cols, channel_blocks, strict=True):
        with col:
            st.markdown(f"**{label}**")
            st.markdown(
                f'<div class="research-channel-card">{html.escape(text)}</div>',
                unsafe_allow_html=True,
            )

    price_col, demand_col = st.columns(2)
    with price_col:
        st.markdown("**Price range observed**")
        st.info(analysis.price_range_observed)
    with demand_col:
        st.markdown("**Demand reasoning**")
        st.info(analysis.demand_estimate.reasoning)

    if analysis.key_competitors:
        st.markdown("#### Key competitors identified")
        for comp in analysis.key_competitors:
            st.markdown(
                f"**[{comp.platform}]** [{html.escape(comp.listing_title)}]({comp.source_url})  \n"
                f"*Price signal:* {html.escape(comp.price_signal)}  \n"
                f"*Similarity:* {html.escape(comp.similarity_note)}"
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


def render_dashboard(result: ProductEvaluationResponse, meta: dict | None = None) -> None:
    """Premium results dashboard with Plotly gauges."""
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
        st.markdown("#### Market saturation")
        st.markdown(saturation_badge_html(result.market_saturation.level), unsafe_allow_html=True)
        st.caption(result.market_saturation.motivation)
        st.markdown("#### Shipping & logistics")
        st.markdown(
            f'<div class="insight-card">{html.escape(result.estimated_shipping_category)}</div>',
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
    gauge_cols = st.columns(4)
    for col, (label, dim) in zip(gauge_cols, dimension_specs, strict=True):
        with col:
            st.plotly_chart(
                make_score_gauge(label, dim.score, height=230),
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
    st.markdown('<p class="section-eyebrow">Creative</p>', unsafe_allow_html=True)
    st.markdown("### TikTok concepts")
    hook_cols = st.columns(3)
    for col, hook in zip(hook_cols, result.tiktok_hooks, strict=True):
        with col:
            st.markdown(
                f"""
                <div class="hook-card">
                    <p class="hook-label">Hook</p>
                    <p class="hook-text">{html.escape(hook.hook_text)}</p>
                    <p class="hook-label">Visuals</p>
                    <p class="hook-body">{html.escape(hook.visuals)}</p>
                    <p class="hook-label">Voiceover</p>
                    <p class="hook-body">{html.escape(hook.voiceover)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
    st.markdown('<p class="section-eyebrow">Strategy</p>', unsafe_allow_html=True)
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
