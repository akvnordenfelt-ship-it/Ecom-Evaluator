"""Global site navigation bar."""

from __future__ import annotations

import html

import streamlit as st

from ecom_evaluator.auth.session import get_current_user, is_authenticated, logout_user
from ecom_evaluator.ui.subscription import (
    APP_VIEW_LANDING,
    enter_tool_view,
    evaluations_status_label,
    go_to_landing,
    open_auth_screen,
    user_can_run,
)

_RESOURCES_DROPDOWN_HTML = """
<div class="nav-dropdown">
  <a class="nav-text-link nav-dropdown-trigger" href="?nav_anchor=resources">
    <span>Resources</span>
    <span class="nav-caret" aria-hidden="true">▾</span>
  </a>
  <div class="nav-dropdown-panel" role="menu">
    <a class="nav-dropdown-item" href="?nav_anchor=process">How it works</a>
    <a class="nav-dropdown-item" href="?nav_anchor=sample">Sample report</a>
    <a class="nav-dropdown-item" href="?nav_anchor=pricing">Plans &amp; pricing</a>
    <a class="nav-dropdown-item" href="?nav_anchor=resources">FAQ</a>
  </div>
</div>
"""


def handle_nav_anchor_query() -> None:
    """Navigate to a landing section when ?nav_anchor= is present in the URL."""
    anchor = st.query_params.get("nav_anchor")
    if not anchor:
        return
    st.session_state["app_view"] = APP_VIEW_LANDING
    st.session_state["landing_anchor"] = anchor
    try:
        del st.query_params["nav_anchor"]
    except Exception:
        st.query_params.clear()
    st.rerun()


def render_site_navbar() -> None:
    """Sticky top bar — brand left, links center-right, actions far right."""
    logged_in = is_authenticated()
    user = get_current_user()

    st.markdown('<div class="site-nav-outer"><div class="site-nav-inner">', unsafe_allow_html=True)

    brand_col, links_col, actions_col = st.columns([1.15, 1.55, 1.3], vertical_alignment="center")

    with brand_col:
        if st.button("🦈  ProductScore", key="nav_brand_home", type="tertiary"):
            go_to_landing()

    with links_col:
        if logged_in:
            pricing_col, resources_col = st.columns([0.55, 1.45], vertical_alignment="center")
        else:
            pricing_col, resources_col, login_col = st.columns([0.55, 1.25, 0.65], vertical_alignment="center")

        with pricing_col:
            if st.button("Pricing", key="nav_pricing", use_container_width=True):
                go_to_landing(anchor="pricing")

        with resources_col:
            st.markdown(_RESOURCES_DROPDOWN_HTML, unsafe_allow_html=True)

        if not logged_in:
            with login_col:
                if st.button("Log in", key="nav_login", use_container_width=True):
                    open_auth_screen(mode="login")

    with actions_col:
        if logged_in:
            run_col, logout_col = st.columns([1.15, 0.85], vertical_alignment="center")
            with run_col:
                if st.button("Run evaluation", key="nav_run_eval", type="primary", use_container_width=True):
                    enter_tool_view()
                    st.rerun()
            with logout_col:
                if st.button("Log out", key="nav_logout", use_container_width=True):
                    logout_user()
                    st.session_state["app_view"] = APP_VIEW_LANDING
                    st.rerun()
        else:
            _, cta_col, _ = st.columns([0.15, 1, 0.15], vertical_alignment="center")
            with cta_col:
                if st.button("Get started", key="nav_signup", type="primary", use_container_width=True):
                    open_auth_screen(mode="signup")

    if logged_in and user:
        status_label = evaluations_status_label()
        status_class = "done" if user_can_run() else "pending"
        st.markdown(
            f'<div class="site-nav-meta">'
            f'<span class="site-nav-user">{html.escape(user.email)}</span>'
            f'<span class="check-row check-row--{status_class} site-nav-quota">'
            f'<span class="check-dot"></span>{html.escape(status_label)}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div></div>", unsafe_allow_html=True)
