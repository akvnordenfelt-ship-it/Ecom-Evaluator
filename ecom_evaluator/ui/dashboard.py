"""Six-section evaluation dashboard."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ecom_evaluator.config import PLOTLY_CHART_CONFIG
from ecom_evaluator.economics import (
    compute_economics_snapshot,
    compute_financial_summary,
    compute_scaling_matrix,
)
from ecom_evaluator.models import ProductEvaluationResponse, SentimentImprovement, SentimentPainPoint, SentimentShopifyHook
from ecom_evaluator.plans import PlanTier
from ecom_evaluator.report_sections import (
    LOCKED_SECTION_COPY,
    REPORT_SECTIONS,
    has_section_access,
    section_by_id,
)
from ecom_evaluator.reports import build_markdown_report, slugify_filename
from ecom_evaluator.scoring import score_bar_color, verdict_status
from ecom_evaluator.ui.subscription import get_subscription_tier, stripe_checkout_url


def make_overall_gauge(score: int) -> go.Figure:
    bar_color = score_bar_color(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100", "font": {"size": 32, "color": "#0f172a"}},
            title={"text": "Overall Product Score", "font": {"size": 16, "color": "#334155"}},
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
            },
        )
    )
    fig.update_layout(
        height=280,
        margin=dict(l=24, r=24, t=64, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def make_metric_bars(result: ProductEvaluationResponse) -> go.Figure:
    labels = [
        "Logistics & Margin",
        "Market Saturation",
        "Marketing Velocity",
        "Brandability & Longevity",
        "Seasonality",
    ]
    scores = [
        result.metric_logistics_margin,
        result.metric_market_saturation,
        result.metric_marketing_velocity,
        result.metric_brandability,
        result.metric_seasonality,
    ]
    colors = [score_bar_color(s) for s in scores]
    fig = go.Figure(
        go.Bar(
            x=scores,
            y=labels,
            orientation="h",
            marker_color=colors,
            text=[f"{s}%" for s in scores],
            textposition="outside",
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=12, r=48, t=12, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 105], title="Score"),
        showlegend=False,
    )
    return fig


def render_section_header(section_id: str) -> None:
    section = section_by_id(section_id)
    st.markdown(
        f'<p class="section-eyebrow">{html.escape(section.eyebrow)}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(f"### {html.escape(section.title)}")
    st.caption(section.subtitle)


def render_locked_card(*, section_id: str) -> None:
    section = section_by_id(section_id)
    body_html = LOCKED_SECTION_COPY[section_id]
    st.markdown(
        f"""
        <div class="locked-section-blur">
            <div class="locked-overlay">
                <p class="locked-icon">🔒</p>
                <p class="locked-kicker">Section {section.number} · Premium · $29/mo</p>
                <p class="locked-title">{html.escape(section.title)}</p>
                <div class="locked-copy"><p>{body_html}</p></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        "Upgrade to Premium — $29/mo",
        stripe_checkout_url(PlanTier.PREMIUM),
        type="primary",
        use_container_width=True,
        key=f"upgrade_{section_id}",
    )


def render_cliffhanger_banner() -> None:
    st.markdown(
        """
        <div class="cliffhanger-banner">
            <p class="cliffhanger-kicker">The cliffhanger</p>
            <p class="cliffhanger-title">You've seen the risks — now prove the opportunity</p>
            <p class="cliffhanger-copy">
                Red flags alone can't tell you if this product survives real logistics, ad costs, and sourcing math.
                Premium unlocks the financial verdict, marketing blueprint, live competitor intel, and review sentiment analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_1(result: ProductEvaluationResponse) -> None:
    render_section_header("product_profile")
    gauge_col, bars_col = st.columns([1, 1.3])
    with gauge_col:
        st.plotly_chart(make_overall_gauge(result.overall_score), use_container_width=True, config=PLOTLY_CHART_CONFIG)
        st.caption("Overall score is computed in Python from the five weighted metrics below.")
    with bars_col:
        st.plotly_chart(make_metric_bars(result), use_container_width=True, config=PLOTLY_CHART_CONFIG)

    st.markdown(
        f'<div class="insight-card insight-card--hero">'
        f'<p class="card-kicker">Product profile</p>'
        f"<p>{html.escape(result.product_profile_summary)}</p></div>",
        unsafe_allow_html=True,
    )

    blocks = [
        ("Physical weight", result.physical_weight_assessment),
        ("Fragility", result.fragility_assessment),
        ("Variants", result.variant_complexity),
        ("Shipping complexity", result.shipping_complexity),
    ]
    r1a, r1b = st.columns(2)
    r2a, r2b = st.columns(2)
    for col, (label, text) in zip((r1a, r1b, r2a, r2b), blocks, strict=True):
        with col:
            st.markdown(
                f'<div class="stat-tile"><p class="stat-tile-label">{html.escape(label)}</p>'
                f'<p class="stat-tile-body">{html.escape(text)}</p></div>',
                unsafe_allow_html=True,
            )

    notes = [
        ("Market saturation", result.metric_market_saturation_note),
        ("Marketing velocity", result.metric_marketing_velocity_note),
        ("Logistics & margin", result.metric_logistics_margin_note),
        ("Seasonality", result.metric_seasonality_note),
        ("Brandability", result.metric_brandability_note),
    ]
    with st.expander("Metric rationale (panel notes)", expanded=False):
        for label, note in notes:
            st.markdown(f"**{label}** — {note}")


def render_section_2(result: ProductEvaluationResponse) -> None:
    render_section_header("red_flags")
    st.markdown(
        f'<div class="insight-card" style="border-left:4px solid #DC2626;">'
        f'<p class="card-kicker">{html.escape(result.red_flag_headline)}</p>'
        f"<p>{html.escape(result.red_flag_analysis)}</p></div>",
        unsafe_allow_html=True,
    )
    for idx, flag in enumerate([result.red_flag_1, result.red_flag_2, result.red_flag_3], start=1):
        st.markdown(
            f'<div class="action-item action-item--risk">'
            f"<strong>Red flag {idx}:</strong> {html.escape(flag)}</div>",
            unsafe_allow_html=True,
        )


def render_section_3(meta: dict | None, overall_score: int, tier: PlanTier) -> None:
    render_section_header("margin_matrix")
    if not has_section_access("margin_matrix", tier):
        render_locked_card(section_id="margin_matrix")
        return

    if not meta:
        st.info("Financial inputs unavailable — re-run the evaluation.")
        return

    econ = compute_economics_snapshot(
        purchase_price=float(meta.get("purchase_price", 0)),
        sales_price=float(meta.get("sales_price", 0)),
        weight_kg=float(meta.get("weight_kg", 0)),
        length_cm=float(meta.get("length_cm", 0)),
        width_cm=float(meta.get("width_cm", 0)),
        height_cm=float(meta.get("height_cm", 0)),
    )
    fin = compute_financial_summary(econ)
    matrix = compute_scaling_matrix(econ)

    if meta.get("used_sales_price_estimate"):
        st.caption("Selling price was estimated at 3× purchase cost — confirm your target price before scaling.")
    if meta.get("used_physical_baseline"):
        st.caption("Shipping uses lightweight package baseline — add real weight/dimensions for precise logistics.")

    summary_df = pd.DataFrame(
        [
            {"Metric": "Gross margin (per unit)", "Value": f"${fin.gross_margin_usd:.2f} ({fin.gross_margin_pct:.1f}%)"},
            {"Metric": "ROI on product cost", "Value": f"{fin.roi_pct:.1f}%"},
            {"Metric": "Break-even CPA (after est. shipping)", "Value": f"${fin.break_even_cpa:.2f}"},
            {"Metric": "Est. shipping / unit", "Value": f"${fin.shipping_per_unit_usd:.2f}"},
        ]
    )
    st.markdown("#### Unit economics snapshot")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("#### Volume scaling matrix")
    matrix_df = pd.DataFrame(
        [
            {
                "Units / month": row.units_per_month,
                "Gross revenue": f"${row.gross_revenue:,.0f}",
                "Product cost": f"${row.total_product_cost:,.0f}",
                "Shipping": f"${row.total_shipping:,.0f}",
                "Net profit": f"${row.net_profit:,.0f}",
                "Net profit (shipping +20%)": f"${row.net_profit_stressed:,.0f}",
            }
            for row in matrix
        ]
    )
    st.dataframe(matrix_df, use_container_width=True, hide_index=True)
    st.caption(
        "Stress-test row assumes logistics costs spike 20% — common when carriers re-rate dimensional weight."
    )

    verdict = verdict_status(overall_score)
    st.markdown(
        f"""
        <div class="verdict-banner verdict-banner--{verdict.css_class}">
            <p class="verdict-banner-emoji">{verdict.emoji}</p>
            <div class="verdict-banner-copy">
                <p class="verdict-banner-label">{html.escape(verdict.label)}</p>
                <p class="verdict-banner-subtitle">{html.escape(verdict.subtitle)}</p>
            </div>
            <p class="verdict-banner-score">{overall_score}<span>/100</span></p>
        </div>
        <p class="verdict-banner-context">Products scoring above 70 statistically represent healthy e-commerce foundations.</p>
        """,
        unsafe_allow_html=True,
    )


def render_section_4(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("marketing_teaser")
    if not has_section_access("marketing_teaser", tier) or not result.has_marketing_teaser():
        render_locked_card(section_id="marketing_teaser")
        return

    hook_pct = (result.scroll_stopping_hook_index or 5) * 10
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown(
            f'<div class="stat-tile">'
            f'<p class="stat-tile-label">Scroll-stopping hook index</p>'
            f'<p class="stat-tile-value">{result.scroll_stopping_hook_index or 0}/10</p>'
            f'<p class="stat-tile-body">Visual stop-power for short-form feeds</p></div>',
            unsafe_allow_html=True,
        )
        st.progress(hook_pct / 100, text=f"Hook potential {hook_pct}%")
        st.markdown(
            f'<div class="stat-tile"><p class="stat-tile-label">Primary channel</p>'
            f'<p class="stat-tile-value" style="font-size:1.1rem;">'
            f"{html.escape(result.marketing_primary_channel or '')}</p></div>",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown("#### Core buyer persona")
        st.markdown(
            f'<div class="persona-card"><p>{html.escape(result.buyer_persona_hint or "")}</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown("#### Strategic marketing teaser")
        st.markdown(
            f'<div class="insight-card insight-card--marketing"><p>{html.escape(result.marketing_teaser or "")}</p></div>',
            unsafe_allow_html=True,
        )
    st.info("Section 6 unlocks competitor review sentiment analysis and product improvement directives on Premium.")


def render_section_5(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("web_intelligence")
    if not has_section_access("web_intelligence", tier) or not result.has_web_intelligence():
        render_locked_card(section_id="web_intelligence")
        return

    st.markdown(
        f'<div class="insight-card insight-card--hero">'
        f"<p>{html.escape(result.web_intelligence_summary or '')}</p></div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Amazon snapshot")
        st.markdown(result.web_amazon_snapshot or "")
        st.markdown("#### Competitor tracking")
        st.markdown(result.web_competitor_tracking or "")
    with c2:
        st.markdown("#### AliExpress / sourcing")
        st.markdown(result.web_aliexpress_sourcing or "")
        st.markdown("#### Sourcing links")
        st.markdown(result.web_sourcing_links or "")


def _anger_bar_html(score: int) -> str:
    width = max(0, min(100, score))
    return (
        f'<div class="s6-anger-track" aria-hidden="true">'
        f'<div class="s6-anger-fill" style="width:{width}%;"></div>'
        f"</div>"
        f'<p class="s6-anger-label">Anger / Frustration Index · <strong>{width}/100</strong></p>'
    )


def _render_pain_point_card(point: SentimentPainPoint) -> str:
    return (
        f'<div class="s6-pain-row">'
        f'<div class="s6-pain-row-head">'
        f'<p class="s6-pain-category">{html.escape(point.category)}</p>'
        f"{_anger_bar_html(point.anger_frustration_index)}"
        f"</div>"
        f'<p class="s6-pain-trend">{html.escape(point.negative_trend)}</p>'
        f'<p class="s6-pain-evidence"><span>Review signal:</span> {html.escape(point.review_evidence)}</p>'
        f"</div>"
    )


def _render_improvement_row(item: SentimentImprovement) -> str:
    badge_class = (
        "s6-roi-badge--high"
        if item.roi_badge == "High ROI Improvement"
        else "s6-roi-badge--low"
    )
    return (
        f'<div class="s6-win-row">'
        f'<div class="s6-win-row-head">'
        f'<p class="s6-win-category">{html.escape(item.linked_category)}</p>'
        f'<span class="s6-roi-badge {badge_class}">{html.escape(item.roi_badge)}</span>'
        f"</div>"
        f'<p class="s6-win-directive">{html.escape(item.engineering_directive)}</p>'
        f"</div>"
    )


def _render_shopify_hook_card(hook: SentimentShopifyHook) -> str:
    return (
        f'<div class="s6-hook-card">'
        f'<p class="s6-hook-angle">{html.escape(hook.angle)}</p>'
        f'<p class="s6-hook-copy">{html.escape(hook.copy_block)}</p>'
        f"</div>"
    )


def render_section_6(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("competitor_sentiment")
    if not has_section_access("competitor_sentiment", tier) or not result.has_competitor_sentiment():
        render_locked_card(section_id="competitor_sentiment")
        return

    pain_points = result.sentiment_pain_points or []
    improvements = result.sentiment_improvement_directives or []
    hooks = result.sentiment_shopify_hooks or []

    pain_html = "".join(_render_pain_point_card(point) for point in pain_points)
    win_html = "".join(_render_improvement_row(item) for item in improvements)
    hooks_html = "".join(_render_shopify_hook_card(hook) for hook in hooks)

    st.markdown(
        f"""
        <div class="s6-dashboard">
            <div class="s6-header">
                <p class="s6-kicker">Section 6 · Premium Analysis</p>
                <h4 class="s6-title">Competitor Review Sentiment Analysis</h4>
                <p class="s6-subtitle">AI-driven extraction of competitor weaknesses, negative review trends, and engineering solutions.</p>
                <p class="s6-summary">{html.escape(result.sentiment_executive_summary or "")}</p>
            </div>

            <div class="s6-card s6-card--pain">
                <p class="s6-card-title">The Critical Pain Points</p>
                <p class="s6-card-lead">What customers hate in competing products</p>
                <div class="s6-pain-grid">{pain_html}</div>
            </div>

            <div class="s6-card s6-card--win">
                <p class="s6-card-title">Strategic Engineering &amp; Manufacturing Directives</p>
                <p class="s6-card-lead">How to win against the weaknesses above</p>
                <div class="s6-win-grid">{win_html}</div>
            </div>

            <div class="s6-card s6-card--hooks">
                <p class="s6-card-title">Unfair Advantage Copywriting Hooks</p>
                <p class="s6-card-lead">Shopify-ready angles that call out competitor failures</p>
                <div class="s6-hook-grid">{hooks_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_export_buttons(result: ProductEvaluationResponse, meta: dict) -> None:
    product_name = meta.get("product_name", "product")
    analyzed_at = meta.get("analyzed_at", datetime.now(timezone.utc).isoformat())
    slug = slugify_filename(product_name)
    timestamp = analyzed_at[:10]

    col_json, col_md, col_clear = st.columns([1, 1, 1])
    with col_json:
        st.download_button(
            label="Download JSON",
            data=json.dumps(result.model_dump(), indent=2, ensure_ascii=False),
            file_name=f"{slug}_analysis_{timestamp}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_md:
        st.download_button(
            label="Download Markdown report",
            data=build_markdown_report(
                result,
                product_name=product_name,
                analyzed_at=analyzed_at,
                meta=meta,
                tier=meta.get("subscription_tier", PlanTier.FREE.value),
            ),
            file_name=f"{slug}_analysis_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_clear:
        if st.button("Clear results", use_container_width=True):
            st.session_state["analysis_result"] = None
            st.session_state["analysis_meta"] = None
            st.rerun()


def render_dashboard(result: ProductEvaluationResponse, meta: dict | None = None) -> None:
    tier = get_subscription_tier()
    unlocked = sum(1 for s in REPORT_SECTIONS if has_section_access(s.id, tier))

    st.markdown(
        f'<div class="status-banner status-banner--success">'
        f"Evaluation complete · {unlocked}/6 sections unlocked</div>",
        unsafe_allow_html=True,
    )

    if meta:
        product_name = meta.get("product_name", "Product")
        analyzed_at = meta.get("analyzed_at", "")
        if analyzed_at:
            st.markdown(
                f'<p class="report-meta">Report · <strong>{html.escape(product_name)}</strong> · '
                f'{analyzed_at[:19].replace("T", " ")} UTC</p>',
                unsafe_allow_html=True,
            )
        render_export_buttons(result, meta)

    render_section_1(result)
    st.divider()
    render_section_2(result)
    if tier == PlanTier.FREE:
        st.divider()
        render_cliffhanger_banner()
    st.divider()
    render_section_3(meta, result.overall_score, tier)
    st.divider()
    render_section_4(result, tier)
    st.divider()
    render_section_5(result, tier)
    st.divider()
    render_section_6(result, tier)

    with st.expander("Raw JSON"):
        st.json(result.model_dump())
