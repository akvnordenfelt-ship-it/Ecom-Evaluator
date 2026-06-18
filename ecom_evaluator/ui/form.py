"""Streamlit form and shell UI."""

from __future__ import annotations

import html

import streamlit as st

from ecom_evaluator.auth.session import account_quota_label, get_current_user, is_authenticated, logout_user
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.settings import has_shared_api_key, resolve_api_key
from ecom_evaluator.ui.paywall import render_paywall_card
from ecom_evaluator.rate_limit import load_rate_limit_config, remaining_analyses
from ecom_evaluator.ui.session import get_rate_limit_state, has_remaining_quota, shared_rate_limit_applies
from ecom_evaluator.ui.subscription import (
    APP_VIEW_LANDING,
    evaluations_status_label,
    show_paywall,
    user_can_run,
)
from ecom_evaluator.ui.branding import BRAND_TAGLINE, wordmark_html
from ecom_evaluator.ui.theme import form_section_header, tool_workspace_hero


def render_app_header(*, hide_api_status: bool = False) -> None:
    st.markdown('<div class="app-header-marker"></div>', unsafe_allow_html=True)
    top_left, top_right = st.columns([3, 1])
    with top_left:
        st.markdown(
            f"""
            <div class="app-topbar">
                <div class="brand-lockup">
                    {wordmark_html(size="md", with_logo=True)}
                    <p class="brand-tagline">{html.escape(BRAND_TAGLINE)}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        if not hide_api_status:
            with st.popover("Settings"):
                st.markdown("**Gemini API key**")
                st.caption("Required for local use. Save `GEMINI_API_KEY` in `.env` or paste below.")
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
            status_class = "done" if user_can_run() else "pending"
            user = get_current_user()
            if user:
                st.caption(html.escape(user.email))
            st.markdown(
                f'<div class="check-row check-row--{status_class}" style="justify-content:flex-end;margin-top:0.75rem;">'
                f'<span class="check-dot"></span>{html.escape(status_label)}</div>',
                unsafe_allow_html=True,
            )
            btn_home, btn_logout = st.columns(2)
            with btn_home:
                if st.button("Home", key="header_home", use_container_width=True):
                    st.session_state["app_view"] = APP_VIEW_LANDING
                    st.rerun()
            with btn_logout:
                if is_authenticated() and st.button("Log out", key="header_logout", use_container_width=True):
                    logout_user()
                    st.rerun()


def _evaluation_quota_label(data: dict) -> str:
    account_label = account_quota_label()
    if account_label:
        return account_label

    left = int(st.session_state.get("evaluations_left", 0))
    if shared_rate_limit_applies(data):
        remaining = remaining_analyses(get_rate_limit_state(), load_rate_limit_config())
        left = min(left, remaining)
    if left == 1:
        return f"1 of {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations left"
    if left > 1:
        return f"{left} of {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations left"
    return "No free evaluations remaining"


def render_readiness_panel(data: dict) -> None:
    api_ok = bool(resolve_api_key(data["api_key"]))
    checks = [
        (bool(data["product_name"].strip()), "Product name entered"),
        (data["purchase_price"] > 0, "Purchase price set"),
    ]
    if data.get("product_url", "").strip():
        checks.append((True, "Listing URL added for richer context"))
    if not has_shared_api_key():
        checks.insert(0, (api_ok, "API connected"))
    done = sum(1 for ok, _ in checks if ok)
    rows_html = "".join(
        f'<div class="check-row check-row--{"done" if ok else "pending"}">'
        f'<span class="check-dot"></span>{html.escape(label)}</div>'
        for ok, label in checks
    )
    quota_label = _evaluation_quota_label(data)
    st.markdown(
        f'<div class="readiness-card readiness-card--premium">'
        f'<div class="readiness-header">'
        f'<span class="readiness-label">Launch checklist</span>'
        f'<span class="readiness-score">{done}/{len(checks)}</span>'
        f"</div>{rows_html}"
        f'<div class="readiness-quota"><span class="readiness-quota-dot"></span>'
        f"{html.escape(quota_label)}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_evaluation_form(*, compact: bool = False) -> dict:
    """Main-area product form (replaces sidebar)."""
    api_key = st.session_state.get("settings_api_key", "")

    if compact:
        st.markdown(
            """
            <div class="tool-workspace-compact">
                <p class="tool-workspace-compact-title">Update your product inputs</p>
                <p class="tool-workspace-compact-copy">Change any field and run again to refresh your report.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            tool_workspace_hero(
                kicker="Your workspace",
                title="Evaluate your product in ~30 seconds",
                copy="Enter your product name and purchase cost to unlock the evaluation. "
                "Add advanced details anytime to sharpen accuracy.",
            ),
            unsafe_allow_html=True,
        )

    st.markdown('<div class="form-workspace-marker"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.55, 1], gap="large")

    with left:
        st.markdown(
            form_section_header(
                badge="Required",
                badge_class="form-section-badge--required",
                icon="✅",
                title="Minimum inputs",
                subtitle="Only product name and purchase price are needed to run your free evaluation.",
            ),
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            product_name = st.text_input(
                "Product name *",
                placeholder="e.g. Wireless earbud cleaning kit",
                key="form_product_name",
            )
            purchase_price = st.number_input(
                "Purchase price ($) *",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="form_purchase_price",
            )
            product_url = st.text_input(
                "Product listing URL (optional)",
                placeholder="https://www.aliexpress.com/item/…",
                key="form_product_url",
                help="Paste an AliExpress, Amazon, eBay, or similar listing link so the AI can use real product context.",
            )

        st.markdown(
            form_section_header(
                badge="Optional",
                badge_class="form-section-badge--optional",
                icon="⚙️",
                title="Advanced profile options",
                subtitle="Improves scoring accuracy for profile, risks, and margin math.",
            ),
            unsafe_allow_html=True,
        )
        with st.expander("Open advanced fields", expanded=False):
            description = st.text_area(
                "Description & target audience",
                height=120,
                placeholder="What it does, who buys it, your angle vs competitors…",
                key="form_description",
            )
            sales_price = st.number_input(
                "Target selling price ($)",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="form_sales_price",
                help="Leave at 0 to estimate at 3× purchase cost for margin math.",
            )
            if sales_price > 0 and purchase_price >= 0:
                margin = sales_price - purchase_price
                margin_pct = margin / sales_price * 100 if sales_price else 0
                st.markdown(
                    f'<div class="metric-hint">Estimated gross margin: <strong>${margin:.2f}</strong> '
                    f'({margin_pct:.1f}% of selling price)</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                '<p class="form-subsection-label">Shipping profile</p>',
                unsafe_allow_html=True,
            )
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
            st.markdown(
                '<p class="form-field-hint">Leave weight/dimensions at 0 to use a lightweight package baseline '
                "(0.15 kg, 15×10×5 cm).</p>",
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "Product image (PNG or JPG)",
                type=["png", "jpg", "jpeg"],
                key="form_image",
            )
            if uploaded_file is not None:
                st.image(uploaded_file, use_container_width=True)

    with right:
        st.markdown(
            """
            <div class="form-action-intro">
                <p class="form-action-kicker">Launch pad</p>
                <p class="form-action-title">Ready when you are</p>
                <p class="form-action-copy">Complete the checklist, then run your Shark Tank-grade evaluation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        form_snapshot = {
            "api_key": api_key,
            "product_name": product_name,
            "purchase_price": purchase_price,
            "product_url": product_url,
        }
        render_readiness_panel(form_snapshot)

        running = st.session_state.get("analysis_running", False)
        paywall_active = show_paywall()
        quota_blocked = shared_rate_limit_applies(form_snapshot) and not has_remaining_quota(form_snapshot)
        blocked = running or paywall_active or quota_blocked

        if paywall_active:
            render_paywall_card()
            run_analysis = False
        else:
            run_analysis = st.button(
                "Run evaluation →",
                type="primary",
                use_container_width=True,
                disabled=blocked,
                key="form_run_analysis",
            )
            st.markdown(
                """
                <p class="form-run-footnote">
                    Free preview · Sections 1–2 · Upgrade for verdict &amp; execution stack
                </p>
                """,
                unsafe_allow_html=True,
            )
            if quota_blocked:
                st.warning("Server quota reached. Try again later or upgrade to Premium.")
            if running:
                st.info("Evaluation in progress — building your report…")

    return {
        "api_key": api_key,
        "product_name": product_name,
        "purchase_price": purchase_price,
        "product_url": product_url,
        "sales_price": sales_price,
        "weight_kg": weight_kg,
        "length_cm": length_cm,
        "width_cm": width_cm,
        "height_cm": height_cm,
        "description": description,
        "uploaded_file": uploaded_file,
        "run_analysis": run_analysis,
    }
