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


def render_site_navbar() -> None:
    """Sticky top bar — brand left, links right."""
    logged_in = is_authenticated()
    user = get_current_user()

    st.markdown('<div class="site-nav-shell">', unsafe_allow_html=True)

    nav_left, nav_right = st.columns([1.15, 2.85], vertical_alignment="center")
    with nav_left:
        if st.button("🦈  ProductScore", key="nav_brand_home", type="tertiary"):
            go_to_landing()

    with nav_right:
        c1, c2, c3, c4, c5 = st.columns([0.85, 0.95, 0.75, 1.05, 0.85])
        with c1:
            if st.button("Pricing", key="nav_pricing", use_container_width=True):
                go_to_landing(anchor="pricing")
        with c2:
            if st.button("Resources", key="nav_resources", use_container_width=True):
                go_to_landing(anchor="resources")
        with c3:
            if not logged_in:
                if st.button("Log in", key="nav_login", use_container_width=True):
                    open_auth_screen(mode="login")
        with c4:
            if logged_in:
                if st.button("Run evaluation", key="nav_run_eval", type="primary", use_container_width=True):
                    enter_tool_view()
                    st.rerun()
            else:
                if st.button("Get started", key="nav_signup", type="primary", use_container_width=True):
                    open_auth_screen(mode="signup")
        with c5:
            if logged_in:
                if st.button("Log out", key="nav_logout", use_container_width=True):
                    logout_user()
                    st.session_state["app_view"] = APP_VIEW_LANDING
                    st.rerun()

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

    st.markdown("</div>", unsafe_allow_html=True)
