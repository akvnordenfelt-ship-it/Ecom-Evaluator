"""Marketing landing page before the evaluation tool."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.ui.subscription import enter_tool_view


def render_landing_page() -> None:
    st.markdown(
        """
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Evaluate any product in minutes</h1>
                <p class="landing-lead">
                    ProductScore scans Amazon, AliExpress, and the open web, then delivers
                    investment scores, competitor intel, a full marketing playbook, and a go-to-market plan —
                    powered by AI.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    features = [
        ("📊", "Investment score", "Four dimension gauges plus a final Shark Tank-style verdict."),
        ("🔍", "Live market research", "Real competitor signals from Amazon, AliExpress, and indie stores."),
        ("🚀", "Go-to-market plan", "Marketing playbook, shipping insights, and channel strategy."),
    ]
    for col, (icon, title, body) in zip((c1, c2, c3), features):
        with col:
            st.markdown(
                f"""
                <div class="landing-feature">
                    <span class="landing-feature-icon">{icon}</span>
                    <p class="landing-feature-title">{title}</p>
                    <p class="landing-feature-body">{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='landing-cta-spacer'></div>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        if st.button(
            "Start your free evaluation",
            type="primary",
            use_container_width=True,
            key="landing_start_cta",
        ):
            enter_tool_view()
            st.rerun()

    st.markdown(
        """
        <p class="landing-footnote">
            No credit card required · 1 free evaluation · Upgrade anytime for unlimited scans
        </p>
        """,
        unsafe_allow_html=True,
    )
