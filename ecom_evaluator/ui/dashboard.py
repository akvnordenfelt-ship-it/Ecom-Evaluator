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
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.plans import PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, has_section_access, section_by_id
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


def render_locked_card(*, section_id: str, tier_required: PlanTier, body_html: str) -> None:
    section = section_by_id(section_id)
    price = "$29/mo" if tier_required == PlanTier.PREMIUM else "$79/mo"
    plan_label = "Premium" if tier_required == PlanTier.PREMIUM else "Pro"
    st.markdown(
        f"""
        <div class="locked-section-blur">
            <div class="locked-overlay">
                <p class="locked-icon">🔒</p>
                <p class="locked-kicker">Section {section.number} · {html.escape(plan_label)}</p>
                <p class="locked-title">{html.escape(section.title)}</p>
                <div class="locked-copy">{body_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    checkout_tier = PlanTier.PREMIUM if tier_required == PlanTier.PREMIUM else PlanTier.PRO
    st.link_button(
        f"Upgrade to {plan_label} — {price}",
        stripe_checkout_url(checkout_tier),
        type="primary",
        use_container_width=True,
        key=f"upgrade_{section_id}",
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


def render_section_3(meta: dict | None, overall_score: int) -> None:
    render_section_header("margin_matrix")
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
        render_locked_card(
            section_id="marketing_teaser",
            tier_required=PlanTier.PREMIUM,
            body_html=(
                "<p>Upgrade to <strong>Premium ($29/mo)</strong> to unlock the Marketing Viability Teaser. "
                "Discover the primary recommended channel (TikTok Organic vs Meta Paid), the "
                "Scroll-Stopping Visual Hook Index (1–10), and the Core Buyer Persona mapping.</p>"
            ),
        )
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
    st.info("Full ad scripts, targeting stacks, and influencer DMs unlock in Section 6 (Pro).")


def render_section_5(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("web_intelligence")
    if not has_section_access("web_intelligence", tier) or not result.has_web_intelligence():
        render_locked_card(
            section_id="web_intelligence",
            tier_required=PlanTier.PREMIUM,
            body_html=(
                "<p>Upgrade to <strong>Premium ($29/mo)</strong> to unlock real-time web search, "
                "active AliExpress/CJ sourcing supplier matches, and live competitor price tracking "
                "across Amazon &amp; Shopify.</p>"
            ),
        )
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


def render_section_6(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("marketing_deep_dive")
    if not has_section_access("marketing_deep_dive", tier) or not result.has_marketing_deep_dive():
        render_locked_card(
            section_id="marketing_deep_dive",
            tier_required=PlanTier.PRO,
            body_html="""<p>Upgrade to <strong>Pro ($79/mo)</strong> to unlock the Ultimate Marketing Blueprint powered by Claude Opus. Includes:</p>
<ul class="locked-list">
<li>5× Ad Script Engine (complete TikTok/Reels scripts with visual cues)</li>
<li>Precision Targeting Blueprint (exact Facebook &amp; TikTok Ads interests and demographics)</li>
<li>Influencer Outreach Templates (high-conversion copy-paste DMs)</li>
<li>Multi-Angle Positioning Matrix (3 distinct marketing angles to crush competitors)</li>
</ul>""",
        )
        return

    st.markdown("#### 5× Ad Script Engine")
    st.markdown(result.marketing_ad_scripts or "")
    st.markdown("#### Precision targeting blueprint")
    st.markdown(result.marketing_targeting_blueprint or "")
    st.markdown("#### Influencer outreach templates")
    st.markdown(result.marketing_influencer_templates or "")
    st.markdown("#### Multi-angle positioning matrix")
    st.markdown(result.marketing_positioning_matrix or "")


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
            data=build_markdown_report(result, product_name=product_name, analyzed_at=analyzed_at, meta=meta),
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
        f"Evaluation complete · {unlocked}/6 sections · Gemini 2.5 Flash</div>",
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
    st.divider()
    render_section_3(meta, result.overall_score)
    st.divider()
    render_section_4(result, tier)
    st.divider()
    render_section_5(result, tier)
    st.divider()
    render_section_6(result, tier)

    with st.expander("Raw JSON"):
        st.json(result.model_dump())
