"""Global site navigation bar — Jungle Scout-style SaaS header."""

from __future__ import annotations

import html

import streamlit as st

from ecom_evaluator.auth.session import get_current_user, is_authenticated, logout_user
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.ui.subscription import (
    APP_VIEW_AUTH,
    APP_VIEW_LANDING,
    APP_VIEW_TOOL,
    evaluations_status_label,
    user_can_run,
)

_CHEVRON_SVG = (
    '<svg class="site-header__chevron" width="11" height="11" viewBox="0 0 11 11" '
    'fill="none" aria-hidden="true">'
    '<path d="M2.5 4L5.5 7L8.5 4" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)


def handle_nav_query() -> None:
    """Apply landing anchors and nav actions from URL query params."""
    anchor = st.query_params.get("nav_anchor")
    action = st.query_params.get("nav_action")
    if not anchor and not action:
        return

    if anchor:
        st.session_state["app_view"] = APP_VIEW_LANDING
        st.session_state["landing_anchor"] = anchor
    elif action == "home":
        st.session_state["app_view"] = APP_VIEW_LANDING
    elif action == "login":
        st.session_state["app_view"] = APP_VIEW_AUTH
        st.session_state["auth_mode"] = "login"
    elif action == "signup":
        st.session_state["app_view"] = APP_VIEW_AUTH
        st.session_state["auth_mode"] = "signup"
    elif action == "tool":
        st.session_state["app_view"] = APP_VIEW_TOOL
    elif action == "logout":
        logout_user()
        st.session_state["app_view"] = APP_VIEW_LANDING

    try:
        if anchor:
            del st.query_params["nav_anchor"]
        if action:
            del st.query_params["nav_action"]
    except Exception:
        st.query_params.clear()
    st.rerun()


def handle_nav_anchor_query() -> None:
    """Backward-compatible alias for anchor-only handling."""
    handle_nav_query()


def _render_header_html(markup: str) -> None:
    """Render header markup (single compact block — blank lines break st.markdown HTML)."""
    st.markdown(markup, unsafe_allow_html=True)


def _mega_menu_html() -> str:
    return (
        '<div class="site-header__mega">'
        '<div class="site-header__mega-feature">'
        '<p class="site-header__mega-kicker">Free preview</p>'
        '<p class="site-header__mega-title">Know before you spend</p>'
        '<p class="site-header__mega-desc">Upload a product and get Sections 1–2 free in about 30 seconds. '
        f"{FREE_EVALUATIONS_PER_ACCOUNT} evaluations included — no credit card.</p>"
        '<a class="site-header__mega-link" href="?nav_action=signup">Start free evaluation →</a>'
        "</div>"
        '<div class="site-header__mega-grid">'
        '<div class="site-header__mega-col">'
        '<p class="site-header__mega-heading">Learn</p>'
        '<a class="site-header__mega-item" href="?nav_anchor=process">How it works</a>'
        '<span class="site-header__mega-rule"></span>'
        '<a class="site-header__mega-item" href="?nav_anchor=sample">Sample report</a>'
        "</div>"
        '<div class="site-header__mega-col">'
        '<p class="site-header__mega-heading">Support</p>'
        '<a class="site-header__mega-item" href="?nav_anchor=pricing">Plans &amp; pricing</a>'
        '<span class="site-header__mega-rule"></span>'
        '<a class="site-header__mega-item" href="?nav_anchor=resources">FAQ</a>'
        "</div>"
        "</div>"
        "</div>"
    )


def _resources_dropdown_html() -> str:
    return (
        '<div class="site-header__dropdown">'
        '<a class="site-header__link site-header__dropdown-trigger" href="?nav_anchor=resources">'
        "<span>Resources</span>"
        f"{_CHEVRON_SVG}"
        "</a>"
        f'<div class="site-header__dropdown-panel" role="menu">{_mega_menu_html()}</div>'
        "</div>"
    )


def _guest_actions_html() -> str:
    return (
        '<span class="site-header__divider" aria-hidden="true"></span>'
        '<a class="site-header__login" href="?nav_action=login">Log in</a>'
        '<a class="site-header__cta" href="?nav_action=signup">Get started</a>'
    )


def _authenticated_actions_html(*, email: str, status_label: str, status_class: str) -> str:
    return (
        f'<span class="site-header__user">{html.escape(email)}</span>'
        f'<span class="check-row check-row--{status_class} site-header__quota">'
        f'<span class="check-dot"></span>{html.escape(status_label)}</span>'
        '<span class="site-header__divider" aria-hidden="true"></span>'
        '<a class="site-header__cta site-header__cta--compact" href="?nav_action=tool">Run evaluation</a>'
        '<a class="site-header__login" href="?nav_action=logout">Log out</a>'
    )


def _build_site_header_html(*, actions_html: str) -> str:
    return (
        '<header class="site-header">'
        '<div class="site-header__bar">'
        '<div class="site-header__inner">'
        '<a class="site-header__brand" href="?nav_action=home">'
        '<span class="site-header__mark" aria-hidden="true">🦈</span>'
        '<span class="site-header__name">ProductScore</span>'
        "</a>"
        '<nav class="site-header__nav" aria-label="Primary">'
        '<a class="site-header__link" href="?nav_anchor=pricing">Pricing</a>'
        f"{_resources_dropdown_html()}"
        "</nav>"
        f'<div class="site-header__actions">{actions_html}</div>'
        "</div>"
        "</div>"
        "</header>"
        '<div class="site-header__spacer" aria-hidden="true"></div>'
    )


def render_site_navbar() -> None:
    """Render a fixed Jungle Scout-style top navigation bar."""
    logged_in = is_authenticated()
    user = get_current_user()

    actions = (
        _authenticated_actions_html(
            email=user.email,
            status_label=evaluations_status_label(),
            status_class="done" if user_can_run() else "pending",
        )
        if logged_in and user
        else _guest_actions_html()
    )

    _render_header_html(_build_site_header_html(actions_html=actions))
