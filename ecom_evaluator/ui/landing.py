"""Marketing landing page."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS
from ecom_evaluator.ui.subscription import enter_tool_view


def render_landing_page() -> None:
    st.markdown(
        """
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Know if your product can win — before you spend a dollar</h1>
                <p class="landing-lead">
                    ProductScore delivers a 6-section evaluation. The free tier runs on Gemini 2.5 Flash using
                    your inputs and product image only — no web search, near-zero cost, ceiling-quality insights.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Free tier — sections 1–4")
    cols = st.columns(2)
    for idx, section in enumerate(REPORT_SECTIONS[:4]):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="landing-section-card">
                    <p class="landing-section-num">Section {section.number}</p>
                    <p class="landing-section-title">{section.title}</p>
                    <p class="landing-section-body">{section.subtitle}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    pro = PLAN_CONFIG[PlanTier.PRO]
    st.markdown("#### Upgrade path")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(
            f"""
            <div class="landing-plan landing-plan--premium">
                <p class="landing-plan-name">Premium · ${premium.price_usd_monthly}/mo</p>
                <p class="landing-plan-detail">Section 5 — Live web search &amp; sourcing links</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            f"""
            <div class="landing-plan landing-plan--pro">
                <p class="landing-plan-name">Pro · ${pro.price_usd_monthly}/mo</p>
                <p class="landing-plan-detail">Section 6 — Ultimate marketing blueprint (Gemini 2.5 Pro)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        if st.button("Run your free evaluation", type="primary", use_container_width=True, key="landing_start"):
            enter_tool_view()
            st.rerun()

    st.markdown(
        '<p class="landing-footnote">Free · 1 evaluation · No web search · Gemini 2.5 Flash</p>',
        unsafe_allow_html=True,
    )
