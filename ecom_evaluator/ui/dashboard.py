"""Six-section evaluation dashboard."""

from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from ecom_evaluator.config import PLOTLY_CHART_CONFIG
from ecom_evaluator.economics import (
    compute_all_platform_economics,
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

_METRIC_ICONS = {
    "seasonality": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
    ),
    "brandability": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path d="M12 2l2.2 6.8H21l-5.5 4 2.1 6.7L12 16.8 6.4 19.5l2.1-6.7L3 8.8h6.8L12 2z"/></svg>'
    ),
    "velocity": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z"/></svg>'
    ),
    "market": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-7"/></svg>'
    ),
    "logistics": (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
        '<path d="M16 16h6v6H16z"/><path d="M2 16h6v6H2z"/><path d="M9 6h6v6H9z"/>'
        '<path d="M5 16V9h4M15 16V9h4"/></svg>'
    ),
}

_FLAG_IMPACTS = ("Severe", "High", "Moderate")


def _display_verdict_label(score: int) -> tuple[str, str]:
    if score >= 90:
        return "STRONG GO", "go"
    if score >= 70:
        return "GO", "go"
    if score >= 50:
        return "CAUTION", "caution"
    if score >= 40:
        return "HIGH RISK", "risk"
    return "WALK AWAY", "walk"


def _risk_summary_score(overall: int) -> int:
    if overall >= 70:
        return max(12, 100 - overall)
    if overall >= 50:
        return 55 + (70 - overall) // 2
    return min(95, 70 + (50 - overall))


def _risk_label(risk_score: int) -> str:
    if risk_score >= 80:
        return "Very High Risk"
    if risk_score >= 60:
        return "High Risk"
    if risk_score >= 40:
        return "Moderate Risk"
    return "Lower Risk"


def _gauge_needle_deg(score: int) -> float:
    return -90 + (max(0, min(100, score)) / 100) * 180


def _short_flag_title(flag: str) -> str:
    text = flag.strip()
    if len(text) <= 72:
        return text
    return text[:69].rstrip() + "…"


def _flag_detail(flag: str, analysis: str, index: int) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", analysis) if s.strip()]
    if index < len(sentences):
        return sentences[index]
    return analysis


def _why_score_items(result: ProductEvaluationResponse) -> list[str]:
    items: list[str] = []
    metric_notes = [
        ("Market opportunity", result.metric_market_saturation, result.metric_market_saturation_note),
        ("Marketing velocity", result.metric_marketing_velocity, result.metric_marketing_velocity_note),
        ("Logistics & margin", result.metric_logistics_margin, result.metric_logistics_margin_note),
        ("Seasonality", result.metric_seasonality, result.metric_seasonality_note),
        ("Brandability", result.metric_brandability, result.metric_brandability_note),
    ]
    for label, score, note in metric_notes:
        if score < 55 and note:
            items.append(f"{label} scored {score}/100 — {note}")
    for flag in (result.red_flag_1, result.red_flag_2, result.red_flag_3):
        if flag and len(items) < 5:
            items.append(flag)
    if not items:
        items.append(result.red_flag_analysis)
    return items[:5]


def _crow_verdict_copy(result: ProductEvaluationResponse, verdict_label: str) -> str:
    if result.overall_score < 50:
        return (
            f"{verdict_label}. {result.red_flag_headline} "
            "The fundamentals don't support a confident launch without major changes."
        )
    if result.overall_score < 70:
        return (
            f"{verdict_label}. {result.product_profile_summary[:180]}"
            f"{'…' if len(result.product_profile_summary) > 180 else ''}"
        )
    return (
        f"{verdict_label}. {result.product_profile_summary[:200]}"
        f"{'…' if len(result.product_profile_summary) > 200 else ''}"
    )


def _metric_rows_html(result: ProductEvaluationResponse) -> str:
    rows = [
        ("seasonality", "Seasonality", result.metric_seasonality),
        ("brandability", "Brandability & Longevity", result.metric_brandability),
        ("velocity", "Marketing Velocity", result.metric_marketing_velocity),
        ("market", "Market Opportunity", result.metric_market_saturation),
        ("logistics", "Logistics & Margin", result.metric_logistics_margin),
    ]
    parts: list[str] = []
    for key, label, score in rows:
        color = score_bar_color(score)
        parts.append(
            f'<div class="rpt-metric-row">'
            f'<span class="rpt-metric-icon">{_METRIC_ICONS[key]}</span>'
            f'<p class="rpt-metric-label">{html.escape(label)}</p>'
            f'<div class="rpt-metric-track"><div class="rpt-metric-fill" '
            f'style="width:{score}%; --metric-color:{color};"></div></div>'
            f'<span class="rpt-metric-score">{score}/100</span>'
            f"</div>"
        )
    return "".join(parts)


def _glance_rows_html(result: ProductEvaluationResponse, meta: dict | None) -> str:
    meta = meta or {}
    purchase = meta.get("purchase_price")
    sales = meta.get("sales_price")
    weight = meta.get("weight_kg")
    length = meta.get("length_cm")
    width = meta.get("width_cm")
    height = meta.get("height_cm")

    price_bits: list[str] = []
    if purchase:
        price_bits.append(f"Cost ${float(purchase):.2f}")
    if sales:
        price_bits.append(f"Target ${float(sales):.2f}")
    price_text = " · ".join(price_bits) if price_bits else "Add pricing in inputs for margin context"

    dim_bits: list[str] = []
    if weight and float(weight) > 0:
        dim_bits.append(f"{float(weight):.2f} kg")
    if length and width and height:
        dim_bits.append(f"{float(length):.0f}×{float(width):.0f}×{float(height):.0f} cm")
    dim_text = " · ".join(dim_bits) if dim_bits else result.physical_weight_assessment

    product_name = str(meta.get("product_name", "") or "Your product").strip()
    rows = [
        ("Product", product_name),
        ("Category", "Consumer / e-commerce"),
        ("Product type", result.variant_complexity),
        ("Main use case", result.product_profile_summary[:120] + ("…" if len(result.product_profile_summary) > 120 else "")),
        ("Size & weight", result.physical_weight_assessment),
        ("Package & shipping", result.shipping_complexity),
        ("Dims & price point", f"{dim_text} · {price_text}"),
        ("Fragility", result.fragility_assessment),
    ]
    cells = "".join(
        f'<div class="rpt-glance-item"><p class="rpt-glance-key">{html.escape(key)}</p>'
        f'<p class="rpt-glance-val">{html.escape(str(val))}</p></div>'
        for key, val in rows
    )
    return f'<div class="rpt-glance-grid">{cells}</div>'


def _section_rail_html(*, section_id: str, extra_rail: str = "") -> str:
    section = section_by_id(section_id)
    return (
        f'<aside class="rpt-section-rail">'
        f'<span class="rpt-section-kicker">Section {section.number}</span>'
        f'<h3 class="rpt-section-title">{html.escape(section.title)}</h3>'
        f'<p class="rpt-section-lead">{html.escape(section.subtitle)}</p>'
        f"{extra_rail}"
        f"</aside>"
    )


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
        "Market Opportunity",
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


def render_section_1(result: ProductEvaluationResponse, meta: dict | None = None) -> None:
    verdict_label, verdict_class = _display_verdict_label(result.overall_score)
    verdict_box_class = "nogo" if result.overall_score < 50 else ("go" if result.overall_score >= 70 else "caution")
    verdict_symbol = "✕" if result.overall_score < 50 else ("✓" if result.overall_score >= 70 else "!")
    why_items = _why_score_items(result)
    why_list = "".join(f"<li>{html.escape(item)}</li>" for item in why_items)

    rail_extra = (
        '<div class="rpt-rail-note">'
        '<p class="rpt-rail-note-kicker">About the score</p>'
        "<p>Overall score is computed in Python from five weighted metrics — "
        "not guessed by the model. Higher is better for the seller on every axis.</p>"
        "</div>"
    )
    gauge_html = (
        f'<div class="rpt-gauge-wrap">'
        f'<div class="rpt-gauge" role="img" aria-label="Overall score {result.overall_score}">'
        f'<div class="rpt-gauge-arc"></div>'
        f'<div class="rpt-gauge-needle" style="--needle-deg:{_gauge_needle_deg(result.overall_score)}deg;"></div>'
        f'<div class="rpt-gauge-hub"></div>'
        f'<div class="rpt-gauge-readout">'
        f'<span class="rpt-gauge-value">{result.overall_score}</span>'
        f'<span class="rpt-gauge-verdict rpt-gauge-verdict--{verdict_class}">{html.escape(verdict_label)}</span>'
        f"</div></div>"
        f'<p class="rpt-gauge-caption">Overall Product Score</p></div>'
    )

    st.markdown(
        f"""
        <section class="rpt-section rpt-section--s1">
            <div class="rpt-section-layout">
                {_section_rail_html("product_profile", extra_rail=rail_extra)}
                <div class="rpt-section-body">
                    <div class="rpt-s1-top">
                        <div class="rpt-card">{gauge_html}</div>
                        <div class="rpt-card">
                            <p class="rpt-card-title">Metric breakdown</p>
                            <div class="rpt-metric-list">{_metric_rows_html(result)}</div>
                        </div>
                    </div>
                    <div class="rpt-card">
                        <p class="rpt-card-title">Product at a glance</p>
                        {_glance_rows_html(result, meta)}
                    </div>
                    <div class="rpt-s1-bottom">
                        <div class="rpt-verdict-box rpt-verdict-box--{verdict_box_class}">
                            <div class="rpt-verdict-box-head">
                                <span aria-hidden="true">{verdict_symbol}</span>
                                <p class="rpt-verdict-box-title">Crow Verdict</p>
                            </div>
                            <p class="rpt-verdict-box-copy">{html.escape(_crow_verdict_copy(result, verdict_label))}</p>
                        </div>
                        <div class="rpt-why-box">
                            <div class="rpt-why-box-head">
                                <span aria-hidden="true">?</span>
                                <p class="rpt-why-box-title">Why this score?</p>
                            </div>
                            <ul class="rpt-why-list{"" if result.overall_score < 70 else " rpt-why-list--positive"}">{why_list}</ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Metric rationale (panel notes)", expanded=False):
        notes = [
            ("Market opportunity", result.metric_market_saturation_note),
            ("Marketing velocity", result.metric_marketing_velocity_note),
            ("Logistics & margin", result.metric_logistics_margin_note),
            ("Seasonality", result.metric_seasonality_note),
            ("Brandability", result.metric_brandability_note),
        ]
        for label, note in notes:
            st.markdown(f"**{label}** — {note}")


def render_section_2(result: ProductEvaluationResponse) -> None:
    risk_score = _risk_summary_score(result.overall_score)
    risk_pct = risk_score / 100
    invest_yes = result.overall_score >= 55
    invest_class = "yes" if invest_yes else "no"
    invest_icon = "✓" if invest_yes else "✕"
    invest_answer = "Maybe — validate further." if invest_yes and result.overall_score < 70 else (
        "Yes — fundamentals look investable." if invest_yes else "No — not recommended at this stage."
    )

    flags = [result.red_flag_1, result.red_flag_2, result.red_flag_3]
    flag_rows = []
    for idx, flag in enumerate(flags):
        impact = _FLAG_IMPACTS[min(idx, len(_FLAG_IMPACTS) - 1)].lower()
        flag_rows.append(
            f'<div class="rpt-flag-row">'
            f'<span class="rpt-flag-icon" aria-hidden="true">⚠</span>'
            f'<div><p class="rpt-flag-title">{html.escape(_short_flag_title(flag))}</p>'
            f'<p class="rpt-flag-desc">{html.escape(_flag_detail(flag, result.red_flag_analysis, idx))}</p></div>'
            f'<span class="rpt-flag-impact rpt-flag-impact--{impact}">{_FLAG_IMPACTS[min(idx, 2)]}</span>'
            f"</div>"
        )

    rail_extra = (
        '<span class="rpt-rail-badge" aria-hidden="true">☠ We don\u2019t sugarcoat it</span>'
    )

    st.markdown(
        f"""
        <section class="rpt-section rpt-section--s2">
            <div class="rpt-section-layout">
                {_section_rail_html("red_flags", extra_rail=rail_extra)}
                <div class="rpt-section-body">
                    <div class="rpt-s2-grid">
                        <div class="rpt-card">
                            <p class="rpt-card-title">Top red flags</p>
                            <div class="rpt-flag-list">{"".join(flag_rows)}</div>
                        </div>
                        <div class="rpt-risk-panel">
                            <div class="rpt-card rpt-risk-ring-card">
                                <p class="rpt-card-title">Risk summary</p>
                                <div class="rpt-risk-ring" style="--risk-pct:{risk_pct:.4f};" role="img"
                                     aria-label="Risk score {risk_score} out of 100">
                                    <div class="rpt-risk-ring-readout">
                                        <p class="rpt-risk-ring-value">{risk_score}<span>/100</span></p>
                                    </div>
                                </div>
                                <p class="rpt-risk-ring-label">{html.escape(_risk_label(risk_score))}</p>
                                <p class="rpt-risk-ring-caption">Composite risk from score + red-flag severity</p>
                            </div>
                            <div class="rpt-invest-box rpt-invest-box--{invest_class}">
                                <div class="rpt-invest-box-head">
                                    <span class="rpt-invest-box-icon" aria-hidden="true">{invest_icon}</span>
                                    <p class="rpt-invest-box-title">Would we invest?</p>
                                </div>
                                <p class="rpt-invest-box-copy"><strong>{html.escape(invest_answer)}</strong></p>
                                <p class="rpt-invest-box-copy">{html.escape(result.red_flag_headline)}</p>
                            </div>
                        </div>
                    </div>
                    <div class="rpt-card">
                        <p class="rpt-card-title">Risk analysis</p>
                        <p class="rpt-verdict-box-copy">{html.escape(result.red_flag_analysis)}</p>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_3(result: ProductEvaluationResponse, meta: dict | None, tier: PlanTier) -> None:
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
    platform_rows = compute_all_platform_economics(econ)

    if meta.get("used_sales_price_estimate"):
        st.caption("Selling price was estimated at 3× purchase cost — confirm your target price before scaling.")
    if meta.get("used_physical_baseline"):
        st.caption("Shipping uses lightweight package baseline — add real weight/dimensions for precise logistics.")

    summary_df = pd.DataFrame(
        [
            {"Metric": "Gross margin (per unit)", "Value": f"${fin.gross_margin_usd:.2f} ({fin.gross_margin_pct:.1f}%)"},
            {"Metric": "Net margin after shipping + Shopify fees", "Value": f"${fin.net_margin_usd:.2f} ({fin.net_margin_pct:.1f}%)"},
            {"Metric": "Platform fee (Shopify est.)", "Value": f"${fin.platform_fee_usd:.2f} ({fin.platform_fee_pct:.1f}%)"},
            {"Metric": "ROI on product cost", "Value": f"{fin.roi_pct:.1f}%"},
            {"Metric": "Break-even CPA (gross, after shipping)", "Value": f"${fin.break_even_cpa:.2f}"},
            {"Metric": "Break-even CPA (net, after fees)", "Value": f"${fin.break_even_cpa_net:.2f}"},
            {"Metric": "Est. shipping / unit", "Value": f"${fin.shipping_per_unit_usd:.2f}"},
        ]
    )
    st.markdown("#### Unit economics snapshot")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    platform_df = pd.DataFrame(
        [
            {
                "Platform": row.platform_label,
                "Fee %": f"{row.fee_rate_pct:.1f}%",
                "Net margin / unit": f"${row.net_margin_usd:.2f}",
                "Net margin %": f"{row.net_margin_pct:.1f}%",
                "Break-even CPA": f"${row.break_even_cpa:.2f}",
            }
            for row in platform_rows
        ]
    )
    st.markdown("#### Platform fee comparison")
    st.dataframe(platform_df, use_container_width=True, hide_index=True)

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

    if result.has_financial_verdict():
        verdict_class = {
            "GO": "go",
            "NO-GO": "nogo",
            "CONDITIONAL GO": "conditional",
        }.get(result.financial_verdict or "", "conditional")
        conditions_html = "".join(
            f"<li>{html.escape(item)}</li>" for item in (result.financial_conditions or [])
        )
        risks_html = "".join(
            f"<li>{html.escape(item)}</li>" for item in (result.financial_key_risks or [])
        )
        st.markdown(
            f"""
            <div class="verdict-banner verdict-banner--{verdict_class}">
                <p class="verdict-banner-emoji">{"✅" if result.financial_verdict == "GO" else "⚠️" if result.financial_verdict == "CONDITIONAL GO" else "🛑"}</p>
                <div class="verdict-banner-copy">
                    <p class="verdict-banner-label">CFO Verdict · {html.escape(result.financial_verdict or "")}</p>
                    <p class="verdict-banner-subtitle">{html.escape(result.financial_verdict_headline or "")}</p>
                </div>
            </div>
            <div class="insight-card"><p>{html.escape(result.cfo_summary or "")}</p></div>
            <p><strong>Conditions for launch</strong></p><ul>{conditions_html}</ul>
            <p><strong>Key financial risks</strong></p><ul>{risks_html}</ul>
            """,
            unsafe_allow_html=True,
        )
    else:
        verdict = verdict_status(result.overall_score)
        st.markdown(
            f"""
            <div class="verdict-banner verdict-banner--{verdict.css_class}">
                <p class="verdict-banner-emoji">{verdict.emoji}</p>
                <div class="verdict-banner-copy">
                    <p class="verdict-banner-label">{html.escape(verdict.label)}</p>
                    <p class="verdict-banner-subtitle">{html.escape(verdict.subtitle)}</p>
                </div>
                <p class="verdict-banner-score">{result.overall_score}<span>/100</span></p>
            </div>
            <p class="verdict-banner-context">Re-run on Premium for Claude Opus CFO verdict synthesis.</p>
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
        st.markdown("#### Strategic direction")
        st.markdown(
            f'<div class="insight-card insight-card--marketing"><p>{html.escape(result.marketing_teaser or "")}</p></div>',
            unsafe_allow_html=True,
        )

    if result.has_marketing_blueprint():
        if result.competitor_ad_angles:
            st.markdown("#### Competitor ad angles (Meta / TikTok patterns)")
            for angle in result.competitor_ad_angles:
                st.markdown(f"- {html.escape(angle)}")
        if result.marketing_angles:
            st.markdown("#### Fresh angles (differentiated)")
            for angle in result.marketing_angles:
                st.markdown(f"- {html.escape(angle)}")
        if result.ad_script_frameworks:
            st.markdown("#### Ad script frameworks")
            for script in result.ad_script_frameworks:
                st.markdown(
                    f"**{html.escape(script.platform)}** — "
                    f"*Hook:* {html.escape(script.hook)}  \n"
                    f"*Body:* {html.escape(script.body)}  \n"
                    f"*CTA:* {html.escape(script.cta)}"
                )
        if result.targeting_stack:
            st.markdown("#### Targeting stack")
            st.markdown(result.targeting_stack)
        if result.influencer_dm_templates:
            st.markdown("#### Influencer outreach DMs")
            for template in result.influencer_dm_templates:
                st.code(template, language=None)


def render_section_5(result: ProductEvaluationResponse, tier: PlanTier) -> None:
    render_section_header("web_intelligence")
    if not has_section_access("web_intelligence", tier) or not result.has_web_intelligence():
        render_locked_card(section_id="web_intelligence")
        return

    trend = result.demand_trend or "stable"
    trend_emoji = {"rising": "📈", "stable": "➡️", "declining": "📉"}.get(trend, "➡️")
    st.markdown(
        f'<div class="insight-card insight-card--hero">'
        f"<p>{html.escape(result.web_intelligence_summary or '')}</p></div>",
        unsafe_allow_html=True,
    )
    if result.competitor_price_range or result.demand_trend:
        st.markdown(
            f"**Competitor price range:** {html.escape(result.competitor_price_range or 'N/A')} · "
            f"**Demand trend:** {trend_emoji} {html.escape(trend.title())}"
        )
    if result.market_timing_assessment:
        st.markdown(f"**Market timing:** {html.escape(result.market_timing_assessment)}")

    if result.supplier_recommendations:
        st.markdown("#### Top supplier recommendations")
        for supplier in result.supplier_recommendations:
            st.markdown(
                f"**[{html.escape(supplier.name)}]({html.escape(supplier.url)})**  \n"
                f"Price: {html.escape(supplier.price_signal)} · "
                f"MOQ: {html.escape(supplier.moq_signal)} · "
                f"Rating: {html.escape(supplier.rating_signal)}"
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

    praised_html = "".join(
        f"<li>{html.escape(item)}</li>" for item in (result.praised_features or [])
    )
    unmet_html = "".join(
        f"<li>{html.escape(item)}</li>" for item in (result.unmet_needs or [])
    )
    category_score = result.category_sentiment_score

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
                {f'<p class="s6-category-score">Category sentiment score · <strong>{category_score}/100</strong></p>' if category_score is not None else ""}
            </div>

            {f'<div class="s6-card"><p class="s6-card-title">What customers value</p><ul>{praised_html}</ul></div>' if praised_html else ""}
            {f'<div class="s6-card"><p class="s6-card-title">Unmet needs in the category</p><ul>{unmet_html}</ul></div>' if unmet_html else ""}

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
        f'<div class="status-banner status-banner--success cm-ws-reveal">'
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

    render_section_1(result, meta)
    st.divider()
    render_section_2(result)
    if tier == PlanTier.FREE:
        st.divider()
        render_cliffhanger_banner()
    st.divider()
    render_section_3(result, meta, tier)
    st.divider()
    render_section_4(result, tier)
    st.divider()
    render_section_5(result, tier)
    st.divider()
    render_section_6(result, tier)

    with st.expander("Raw JSON"):
        st.json(result.model_dump())
