"""Marketing landing page before the evaluation tool."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.report_sections import REPORT_SECTIONS
from ecom_evaluator.ui.subscription import enter_tool_view


def render_landing_page() -> None:
    free_sections = [section for section in REPORT_SECTIONS if section.free_tier]

    st.markdown(
        """
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Should you sell this product?</h1>
                <p class="landing-lead">
                    ProductScore scans Amazon, AliExpress, and the open web, then delivers an investment
                    verdict, live competitor intel, unit economics, and a clear action plan — in one free evaluation.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### What you get — free")
    section_cols = st.columns(2)
    for idx, section in enumerate(free_sections):
        with section_cols[idx % 2]:
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

    st.markdown(
        """
        <div class="landing-value-strip">
            <span>✓ Live web research</span>
            <span>✓ Margin & shipping analysis</span>
            <span>✓ Top risks & next steps</span>
            <span>✓ JSON + Markdown export</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='landing-cta-spacer'></div>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        if st.button(
            "Run your free evaluation",
            type="primary",
            use_container_width=True,
            key="landing_start_cta",
        ):
            enter_tool_view()
            st.rerun()

    st.markdown(
        """
        <p class="landing-footnote">
            No credit card · 1 free evaluation per session · Takes about 30 seconds
        </p>
        """,
        unsafe_allow_html=True,
    )
