"""Global site navigation bar — pure HTML/CSS SaaS header."""

from __future__ import annotations

import html

import streamlit as st

from ecom_evaluator.auth.session import get_current_user, is_authenticated, logout_user
from ecom_evaluator.ui.subscription import (
    APP_VIEW_AUTH,
    APP_VIEW_LANDING,
    APP_VIEW_TOOL,
    evaluations_status_label,
    user_can_run,
)

_CHEVRON_SVG = (
    '<svg class="site-header__chevron" width="10" height="10" viewBox="0 0 10 10" '
    'fill="none" aria-hidden="true">'
    '<path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)

_DROPDOWN_ITEMS = (
    ("How it works", "process"),
    ("Sample report", "sample"),
    ("Plans & pricing", "pricing"),
    ("FAQ", "resources"),
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


def _dropdown_html() -> str:
    items = "\n".join(
        f'    <a class="site-header__menu-item" href="?nav_anchor={anchor}">{label}</a>'
        for label, anchor in _DROPDOWN_ITEMS
    )
    return f"""
    <div class="site-header__dropdown">
      <a class="site-header__link site-header__dropdown-trigger" href="?nav_anchor=resources">
        <span>Resources</span>
        {_CHEVRON_SVG}
      </a>
      <div class="site-header__dropdown-menu" role="menu">
{items}
      </div>
    </div>
    """


def _guest_actions_html() -> str:
    return """
    <a class="site-header__ghost" href="?nav_action=login">Log in</a>
    <a class="site-header__cta" href="?nav_action=signup">Get started</a>
    """


def _authenticated_actions_html(*, email: str, status_label: str, status_class: str) -> str:
    return f"""
    <span class="site-header__user">{html.escape(email)}</span>
    <span class="check-row check-row--{status_class} site-header__quota">
      <span class="check-dot"></span>{html.escape(status_label)}
    </span>
    <a class="site-header__cta site-header__cta--compact" href="?nav_action=tool">Run evaluation</a>
    <a class="site-header__ghost" href="?nav_action=logout">Log out</a>
    """


def render_site_navbar() -> None:
    """Render a full-width premium SaaS header (Stripe / Linear style)."""
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

    st.markdown(
        f"""
<header class="site-header">
  <div class="site-header__bar">
    <div class="site-header__inner">
      <div class="site-header__left">
        <a class="site-header__brand" href="?nav_action=home">
          <span class="site-header__mark" aria-hidden="true">🦈</span>
          <span class="site-header__name">ProductScore</span>
        </a>
        <nav class="site-header__nav" aria-label="Primary">
          <a class="site-header__link" href="?nav_anchor=pricing">Pricing</a>
          {_dropdown_html()}
        </nav>
      </div>
      <div class="site-header__actions">
        {actions}
      </div>
    </div>
  </div>
</header>
        """,
        unsafe_allow_html=True,
    )
