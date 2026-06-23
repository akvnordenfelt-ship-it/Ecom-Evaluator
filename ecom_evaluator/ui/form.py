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
from ecom_evaluator.ui.workspace_theme import get_workspace_theme, render_workspace_theme_switcher


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


def _session_float(key: str) -> float:
    value = st.session_state.get(key, 0.0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _session_str(key: str) -> str:
    return str(st.session_state.get(key, "") or "").strip()


def _has_uploaded_image() -> bool:
    uploaded = st.session_state.get("form_image")
    return uploaded is not None


def _build_launch_checklist(data: dict) -> list[tuple[bool, str]]:
    has_identity = bool(data.get("product_name", "").strip()) or bool(data.get("product_url", "").strip())
    has_price = float(data.get("purchase_price", 0) or 0) > 0
    has_sell = float(data.get("sales_price", 0) or 0) > 0
    has_usp = bool(data.get("description", "").strip())
    has_specs = any(
        float(data.get(field, 0) or 0) > 0
        for field in ("weight_kg", "length_cm", "width_cm", "height_cm")
    )
    has_image = bool(data.get("has_image"))
    ready = has_identity and has_price
    checks = [
        (has_identity, "Product link or details added"),
        (has_price, "Purchase price set"),
        (has_sell, "Selling price added"),
        (has_usp, "Unique selling point added"),
        (has_specs, "Weight / package specs added"),
        (has_image, "Product image uploaded"),
        (ready, "Ready to run evaluation"),
    ]
    if not has_shared_api_key():
        api_ok = bool(resolve_api_key(data.get("api_key", "")))
        checks.insert(0, (api_ok, "API connected"))
    return checks


def _checklist_snapshot(api_key: str) -> dict:
    return {
        "api_key": api_key,
        "product_name": _session_str("form_product_name"),
        "product_url": _session_str("form_product_url"),
        "purchase_price": _session_float("form_purchase_price"),
        "sales_price": _session_float("form_sales_price"),
        "description": _session_str("form_description"),
        "weight_kg": _session_float("form_weight_kg"),
        "length_cm": _session_float("form_length"),
        "width_cm": _session_float("form_width"),
        "height_cm": _session_float("form_height"),
        "has_image": _has_uploaded_image(),
    }


def _tool_fields_label(text: str) -> None:
    st.markdown(f'<p class="cm-tool-fields-label">{html.escape(text)}</p>', unsafe_allow_html=True)


def _render_tool_sidebar(*, api_key: str) -> None:
    snapshot = _checklist_snapshot(api_key)
    checks = _build_launch_checklist(snapshot)
    done = sum(1 for ok, _ in checks if ok)
    rows_html = "".join(
        f'<div class="cm-tool-check-row{" is-done" if ok else ""}">'
        f'<span class="cm-tool-check-dot" aria-hidden="true"></span>'
        f"<span>{html.escape(label)}</span></div>"
        for ok, label in checks
    )
    quota_label = _evaluation_quota_label(snapshot)
    st.markdown(
        '<aside class="cm-tool-sidebar">'
        '<div class="cm-tool-side-promo cm-ws-reveal">'
        '<p class="cm-tool-side-promo-kicker">Your workspace</p>'
        '<p class="cm-tool-side-promo-title">We don\u2019t sugarcoat. We score.</p>'
        '<p class="cm-tool-side-promo-copy">Product intelligence in ~30 seconds.</p>'
        '<div class="cm-tool-side-badges">'
        '<span class="cm-tool-side-badge">2 sections free</span>'
        '<span class="cm-tool-side-badge">~30 sec preview</span>'
        '<span class="cm-tool-side-badge">Premium unlocks all 6</span>'
        "</div></div>"
        '<div class="cm-tool-checklist cm-ws-reveal cm-ws-reveal-delay-1">'
        '<div class="cm-tool-checklist-head">'
        '<span class="cm-tool-checklist-label">Launch checklist</span>'
        f'<span class="cm-tool-checklist-score">{done}/{len(checks)}</span>'
        f"</div>{rows_html}"
        f'<div class="cm-tool-check-quota"><span class="cm-tool-check-quota-dot" aria-hidden="true"></span>'
        f"{html.escape(quota_label)}</div>"
        "</div>"
        '<div class="cm-tool-score-guide cm-ws-reveal cm-ws-reveal-delay-2">'
        '<p class="cm-tool-score-guide-title">Score guide</p>'
        '<div class="cm-tool-score-row cm-ws-score-row" title="90+ = strong opportunity">'
        '<span class="cm-tool-score-swatch" style="background:#34D399"></span>90–100 · Strong Go</div>'
        '<div class="cm-tool-score-row cm-ws-score-row" title="Solid fundamentals">'
        '<span class="cm-tool-score-swatch" style="background:#60A5FA"></span>70–89 · Promising</div>'
        '<div class="cm-tool-score-row cm-ws-score-row" title="Validate before scaling">'
        '<span class="cm-tool-score-swatch" style="background:#FBBF24"></span>50–69 · Caution</div>'
        '<div class="cm-tool-score-row cm-ws-score-row" title="High risk profile">'
        '<span class="cm-tool-score-swatch" style="background:#F87171"></span>0–49 · Walk away</div>'
        "</div>"
        '<div class="cm-tool-privacy cm-ws-reveal cm-ws-reveal-delay-3">'
        "<span>Encrypted in transit. Never shared.</span>"
        "</div>"
        "</aside>",
        unsafe_allow_html=True,
    )


def _render_tool_main_header(*, compact: bool) -> None:
    if compact:
        st.markdown(
            '<div class="cm-tool-compact-banner">'
            "<strong>Update your product inputs</strong>"
            "<span>Change any field and run again to refresh your report.</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        '<header class="cm-tool-main-head">'
        '<h1 class="cm-tool-main-title">Evaluate your product</h1>'
        '<p class="cm-tool-main-lead">Name and cost are enough to start.</p>'
        "</header>",
        unsafe_allow_html=True,
    )


def _render_tool_cta(
    *,
    blocked: bool,
    paywall_active: bool,
    quota_blocked: bool,
    running: bool,
) -> bool:
    st.markdown('<div class="cm-tool-cta-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    if paywall_active:
        render_paywall_card()
        return False

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
        st.info("Evaluation in progress…")
    st.markdown(
        '<p class="cm-tool-cta-footnote">Sections 1–2 free · ~30 seconds</p>',
        unsafe_allow_html=True,
    )
    return run_analysis


def render_evaluation_form(*, compact: bool = False) -> dict:
    """Main-area product form — premium dark workspace layout."""
    api_key = st.session_state.get("settings_api_key", "")

    mode = get_workspace_theme()
    st.markdown(
        f'<div class="form-workspace-marker cm-tool-form cm-workspace cm-workspace-mode-{html.escape(mode)}" '
        f'data-workspace-theme="{html.escape(mode)}" aria-hidden="true"></div>'
        '<div class="cm-tool-form-layout-marker" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    sidebar, main = st.columns([0.92, 2.08], gap="large")

    with sidebar:
        _render_tool_sidebar(api_key=api_key)

    with main:
        if not compact:
            render_workspace_theme_switcher()
        _render_tool_main_header(compact=compact)

        sales_price = _session_float("form_sales_price")
        weight_kg = _session_float("form_weight_kg")
        length_cm = _session_float("form_length")
        width_cm = _session_float("form_width")
        height_cm = _session_float("form_height")
        description = _session_str("form_description")
        uploaded_file = st.session_state.get("form_image")

        st.markdown('<div class="cm-tool-required-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
        _tool_fields_label("Required")
        with st.container(border=True, key="form_required_card"):
            product_url = st.text_input(
                "Product link",
                placeholder="https://www.aliexpress.com/item/…",
                key="form_product_url",
            )
            name_col, price_col = st.columns(2)
            with name_col:
                product_name = st.text_input(
                    "Product name",
                    placeholder="Wireless earbud cleaning kit",
                    key="form_product_name",
                )
            with price_col:
                purchase_price = st.number_input(
                    "Purchase price",
                    min_value=0.0,
                    step=0.01,
                    format="%.2f",
                    key="form_purchase_price",
                )

        st.markdown('<div class="cm-tool-optional-marker cm-ws-reveal cm-ws-reveal-delay-1" aria-hidden="true"></div>', unsafe_allow_html=True)
        _tool_fields_label("Optional")

        with st.expander("Pricing", expanded=False):
            sales_price = st.number_input(
                "Target selling price",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="form_sales_price",
            )
            if sales_price > 0 and purchase_price >= 0:
                margin = sales_price - purchase_price
                margin_pct = margin / sales_price * 100 if sales_price else 0
                st.markdown(
                    f'<div class="metric-hint">Margin: <strong>${margin:.2f}</strong> ({margin_pct:.1f}%)</div>',
                    unsafe_allow_html=True,
                )
            description = st.text_area(
                "Unique selling point",
                height=88,
                placeholder="Who buys this and why?",
                key="form_description",
            )

        with st.expander("Shipping", expanded=False):
            weight_kg = st.number_input(
                "Weight (kg)", min_value=0.0, step=0.01, format="%.3f", key="form_weight_kg"
            )
            length_cm = st.number_input(
                "Length (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_length"
            )
            width_cm = st.number_input(
                "Width (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_width"
            )
            height_cm = st.number_input(
                "Height (cm)", min_value=0.0, step=0.1, format="%.1f", key="form_height"
            )

        with st.expander("Image", expanded=False):
            uploaded_file = st.file_uploader(
                "Product image",
                type=["png", "jpg", "jpeg"],
                key="form_image",
            )
            if uploaded_file is not None:
                st.image(uploaded_file, use_container_width=True)

        running = st.session_state.get("analysis_running", False)
        paywall_active = show_paywall()
        form_snapshot = {
            "api_key": api_key,
            "product_name": product_name,
            "purchase_price": purchase_price,
            "product_url": product_url,
        }
        quota_blocked = shared_rate_limit_applies(form_snapshot) and not has_remaining_quota(form_snapshot)
        blocked = running or paywall_active or quota_blocked

        run_analysis = _render_tool_cta(
            blocked=blocked,
            paywall_active=paywall_active,
            quota_blocked=quota_blocked,
            running=running,
        )

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
