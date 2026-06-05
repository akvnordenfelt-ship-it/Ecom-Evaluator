"""Streamlit form and shell UI."""

from __future__ import annotations

import html

import streamlit as st

from ecom_evaluator.settings import has_shared_api_key, resolve_api_key
from ecom_evaluator.ui.paywall import render_paywall_card
from ecom_evaluator.ui.session import has_remaining_quota, rate_limit_banner_text, shared_rate_limit_applies
from ecom_evaluator.ui.subscription import (
    APP_VIEW_LANDING,
    evaluations_status_label,
    show_paywall,
    user_can_run,
)
from ecom_evaluator.ui.theme import form_step_header


def render_app_header(*, hide_api_status: bool = False) -> None:
    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.markdown(
            """
            <div class="app-topbar">
                <div class="brand-lockup">
                    <p class="brand-name">ProductScore</p>
                    <p class="brand-tagline">E-commerce evaluator & go-to-market planner</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        if not hide_api_status:
            with st.popover("Settings"):
                st.markdown("**Google AI Studio API key**")
                st.caption("Required for local use. Save `GOOGLE_AI_API_KEY` in `.env` or paste below.")
                st.text_input(
                    "API key",
                    type="password",
                    placeholder="Paste key",
                    key="settings_api_key",
                    label_visibility="collapsed",
                )
                st.link_button("Get an API key", "https://aistudio.google.com/apikey", use_container_width=True)
        else:
            status_label = evaluations_status_label()
            status_class = "done" if user_can_run() or st.session_state.get("is_premium") else "pending"
            st.markdown(
                f'<div class="check-row check-row--{status_class}" style="justify-content:flex-end;margin-top:2.2rem;">'
                f'<span class="check-dot"></span>{html.escape(status_label)}</div>',
                unsafe_allow_html=True,
            )
            if st.button("Home", key="header_home", use_container_width=True):
                st.session_state["app_view"] = APP_VIEW_LANDING
                st.rerun()


def render_hero(*, compact: bool = False) -> None:
    if compact:
        st.markdown(
            """
            <div class="hero-block" style="padding:1.1rem 1.4rem;">
                <p class="hero-kicker">Adjust & re-run</p>
                <p class="hero-title" style="font-size:1.2rem;">Update your product inputs</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        """
        <div class="hero-block">
            <p class="hero-kicker">Shark Tank-grade analysis</p>
            <p class="hero-title">Evaluate any product in minutes</p>
            <p class="hero-copy">
                Enter your product details once. We scan Amazon, AliExpress, and the open web,
                then produce scores, competitor intel, a marketing playbook, and a go-to-market plan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_readiness_panel(data: dict) -> None:
    api_ok = bool(resolve_api_key(data["api_key"]))
    saas_ok = user_can_run()
    checks = [
        (saas_ok, evaluations_status_label()),
        (bool(data["product_name"].strip()), "Product name"),
        (data["sales_price"] > 0, "Selling price"),
        (bool(data["description"].strip()), "Description"),
        (data["uploaded_file"] is not None, "Product image"),
    ]
    if not has_shared_api_key():
        checks.insert(0, (api_ok, "API connected"))
    if shared_rate_limit_applies(data):
        quota_ok = has_remaining_quota(data)
        checks.append((quota_ok, "Server quota"))
    done = sum(1 for ok, _ in checks if ok)
    rows_html = "".join(
        f'<div class="check-row check-row--{"done" if ok else "pending"}">'
        f'<span class="check-dot"></span>{html.escape(label)}</div>'
        for ok, label in checks
    )
    st.markdown(
        f'<div class="readiness-card">'
        f'<div class="readiness-header">'
        f'<span class="readiness-label">Readiness</span>'
        f'<span class="readiness-score">{done}/{len(checks)}</span>'
        f"</div>{rows_html}</div>",
        unsafe_allow_html=True,
    )


def render_evaluation_form(*, compact: bool = False) -> dict:
    """Main-area product form (replaces sidebar)."""
    api_key = st.session_state.get("settings_api_key", "")

    if compact:
        st.caption("Change any field and run a new evaluation to refresh the report.")
    else:
        st.markdown(
            """
            <div class="tool-intro">
                <p class="tool-intro-kicker">Your workspace</p>
                <p class="tool-intro-title">Complete the steps below</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left, right = st.columns([1.45, 1], gap="large")

    with left:
        with st.container(border=True):
            st.markdown(form_step_header("Step 1", "🏷️", "Product identity"), unsafe_allow_html=True)
            product_name = st.text_input(
                "Product name",
                placeholder="e.g. Wireless earbud cleaning kit",
                key="form_product_name",
            )
            description = st.text_area(
                "Description & target audience",
                height=130,
                placeholder="What it does, who buys it, your angle vs competitors, channels you are considering…",
                key="form_description",
            )

        with st.container(border=True):
            st.markdown(form_step_header("Step 2", "💰", "Unit economics"), unsafe_allow_html=True)
            econ_left, econ_right = st.columns(2)
            with econ_left:
                purchase_price = st.number_input(
                    "Purchase price ($)",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f",
                    key="form_purchase_price",
                )
            with econ_right:
                sales_price = st.number_input(
                    "Target selling price ($)",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f",
                    key="form_sales_price",
                )
            if sales_price > 0:
                margin = sales_price - purchase_price
                margin_pct = margin / sales_price * 100
                st.markdown(
                    f'<div class="metric-hint">Estimated gross margin: <strong>${margin:.2f}</strong> '
                    f'({margin_pct:.1f}% of selling price)</div>',
                    unsafe_allow_html=True,
                )

        with st.container(border=True):
            st.markdown(form_step_header("Step 3", "📦", "Shipping profile"), unsafe_allow_html=True)
            weight_kg = st.number_input(
                "Weight (kg)", min_value=0.0, step=0.01, format="%.3f", key="form_weight_kg"
            )
            dim_cols = st.columns(3)
            with dim_cols[0]:
                length_cm = st.number_input("Length (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_length")
            with dim_cols[1]:
                width_cm = st.number_input("Width (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_width")
            with dim_cols[2]:
                height_cm = st.number_input("Height (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_height")

    with right:
        with st.container(border=True):
            st.markdown(form_step_header("Visual", "🖼️", "Product image"), unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload PNG or JPG",
                type=["png", "jpg", "jpeg"],
                key="form_image",
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                st.image(uploaded_file, use_container_width=True)
            else:
                st.markdown(
                    '<div class="metric-hint">Optional but recommended — improves packaging, '
                    "creative, and positioning scores.</div>",
                    unsafe_allow_html=True,
                )

        form_snapshot = {
            "api_key": api_key,
            "product_name": product_name,
            "sales_price": sales_price,
            "description": description,
            "uploaded_file": uploaded_file,
        }
        render_readiness_panel(form_snapshot)

        if shared_rate_limit_applies(form_snapshot):
            banner = rate_limit_banner_text(form_snapshot)
            if banner:
                st.caption(banner)

        running = st.session_state.get("analysis_running", False)
        paywall_active = show_paywall()
        quota_blocked = shared_rate_limit_applies(form_snapshot) and not has_remaining_quota(form_snapshot)
        blocked = running or paywall_active or quota_blocked

        if paywall_active:
            render_paywall_card()
            run_analysis = False
        else:
            run_analysis = st.button(
                "Run evaluation",
                type="primary",
                use_container_width=True,
                disabled=blocked,
                key="form_run_analysis",
            )
            if quota_blocked:
                st.warning("Server quota reached. Try again later or upgrade to Premium.")
            if running:
                st.info("Evaluation in progress — web search, then AI analysis.")

    return {
        "api_key": api_key,
        "product_name": product_name,
        "purchase_price": purchase_price,
        "sales_price": sales_price,
        "weight_kg": weight_kg,
        "length_cm": length_cm,
        "width_cm": width_cm,
        "height_cm": height_cm,
        "description": description,
        "uploaded_file": uploaded_file,
        "run_analysis": run_analysis,
    }
