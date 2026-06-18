"""Global site navigation bar — fixed top header with drawer navigation."""

from __future__ import annotations

import html

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.auth.session import get_current_user, is_authenticated, logout_user
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.ui.branding import header_brand_html
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


_NavAction = str | None
_NavAnchor = str | None

NAV_ACTIONS = ("home", "login", "signup", "tool", "logout")
NAV_ANCHORS = ("process", "sample", "pricing", "resources")


def _nav_action_link(*, action: str, class_name: str, text: str) -> str:
    """In-app nav link that never triggers a full page reload by itself."""
    safe_action = html.escape(action, quote=True)
    return (
        f'<a class="{class_name}" href="#" data-ps-nav-action="{safe_action}" '
        f'target="_self">{text}</a>'
    )


def _nav_anchor_link(*, anchor: str, class_name: str, text: str) -> str:
    safe_anchor = html.escape(anchor, quote=True)
    return (
        f'<a class="{class_name}" href="#" data-ps-nav-anchor="{safe_anchor}" '
        f'target="_self">{text}</a>'
    )


def apply_nav_state(*, action: _NavAction = None, anchor: _NavAnchor = None) -> bool:
    """Update session view state for in-app navigation without a full page reload."""
    if anchor:
        st.session_state["app_view"] = APP_VIEW_LANDING
        st.session_state["landing_anchor"] = anchor
        return True
    if not action:
        return False
    if action == "home":
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
    else:
        return False
    return True


def handle_nav_query() -> None:
    """Apply landing anchors and nav actions from URL query params (cold loads only)."""
    anchor = st.query_params.get("nav_anchor")
    action = st.query_params.get("nav_action")
    if not anchor and not action:
        return

    apply_nav_state(action=action, anchor=anchor)

    try:
        if anchor:
            del st.query_params["nav_anchor"]
        if action:
            del st.query_params["nav_action"]
    except Exception:
        pass
    st.rerun()


def handle_nav_anchor_query() -> None:
    """Backward-compatible alias for anchor-only handling."""
    handle_nav_query()


def render_hidden_nav_buttons() -> None:
    """Hidden Streamlit buttons triggered by the in-app nav JavaScript bridge."""
    for action in NAV_ACTIONS:
        if st.button(f"__PSNAV_{action}__", key=f"ps_nav_{action}"):
            if apply_nav_state(action=action):
                st.rerun()
    for anchor in NAV_ANCHORS:
        if st.button(f"__PSNAV_anchor_{anchor}__", key=f"ps_nav_anchor_{anchor}"):
            if apply_nav_state(anchor=anchor):
                st.rerun()


def install_in_app_nav_bridge() -> None:
    """
    Intercept header/landing nav links and click hidden Streamlit buttons.

    Raw ``href="?nav_..."`` links cause a full HTTP reload, which tears down the
    Streamlit websocket and clears ``st.session_state`` (including auth). Links
    use ``href="#"`` + ``data-ps-nav-*`` so a failed bridge cannot log users out.
    """
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__psInAppNavInstalled) return;
            win.__psInAppNavInstalled = true;

            function readNavTarget(link) {
                const action = link.getAttribute("data-ps-nav-action");
                const anchor = link.getAttribute("data-ps-nav-anchor");
                if (action || anchor) {
                    return { action, anchor };
                }
                const href = link.getAttribute("href") || "";
                if (!href.startsWith("?nav_")) return null;
                const params = new URLSearchParams(href.substring(1));
                return {
                    action: params.get("nav_action"),
                    anchor: params.get("nav_anchor"),
                };
            }

            function clickNavKey(keySuffix, attempt) {
                const tries = attempt || 0;
                const selector = '[class*="st-key-ps_nav_' + keySuffix + '"]';
                const host = doc.querySelector(selector);
                if (!host) {
                    if (tries < 8) {
                        win.setTimeout(function () {
                            clickNavKey(keySuffix, tries + 1);
                        }, 40);
                    }
                    return false;
                }
                const button = host.querySelector("button");
                if (!button) {
                    if (tries < 8) {
                        win.setTimeout(function () {
                            clickNavKey(keySuffix, tries + 1);
                        }, 40);
                    }
                    return false;
                }
                button.click();
                return true;
            }

            doc.addEventListener(
                "click",
                function (event) {
                    const link = event.target.closest(
                        'a[data-ps-nav-action], a[data-ps-nav-anchor], a[href^="?nav_"]'
                    );
                    if (!link) return;

                    const target = readNavTarget(link);
                    if (!target) return;

                    event.preventDefault();
                    event.stopImmediatePropagation();

                    if (target.action) {
                        clickNavKey(target.action, 0);
                    } else if (target.anchor) {
                        clickNavKey("anchor_" + target.anchor, 0);
                    }
                },
                true
            );

            function setMobileNavOpen(open) {
                const header = doc.querySelector(".site-header");
                const btn = doc.querySelector(".site-header__menu-btn");
                const drawer = doc.querySelector(".site-header__mobile-drawer");
                const backdrop = doc.querySelector(".site-header__mobile-backdrop");
                if (!header || !btn) return;
                header.classList.toggle("is-mobile-open", open);
                btn.setAttribute("aria-expanded", open ? "true" : "false");
                if (drawer) drawer.setAttribute("aria-hidden", open ? "false" : "true");
                if (backdrop) backdrop.setAttribute("aria-hidden", open ? "false" : "true");
                doc.documentElement.classList.toggle("ps-nav-open", open);
            }

            doc.addEventListener(
                "click",
                function (event) {
                    const menuBtn = event.target.closest(".site-header__menu-btn");
                    if (menuBtn) {
                        event.preventDefault();
                        const header = doc.querySelector(".site-header");
                        setMobileNavOpen(header && !header.classList.contains("is-mobile-open"));
                        return;
                    }
                    if (event.target.closest(".site-header__mobile-backdrop")) {
                        setMobileNavOpen(false);
                        return;
                    }
                    if (
                        event.target.closest(
                            ".site-header__mobile-drawer a[data-ps-nav-action], .site-header__mobile-drawer a[data-ps-nav-anchor]"
                        )
                    ) {
                        setMobileNavOpen(false);
                    }
                },
                true
            );
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def install_same_window_nav_bridge() -> None:
    """Backward-compatible alias — navigation is handled by install_in_app_nav_bridge."""
    install_in_app_nav_bridge()


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
        + _nav_action_link(
            action="signup",
            class_name="site-header__mega-link",
            text="Start free evaluation →",
        )
        + "</div>"
        '<div class="site-header__mega-grid">'
        '<div class="site-header__mega-col">'
        '<p class="site-header__mega-heading">Learn</p>'
        + _nav_anchor_link(anchor="process", class_name="site-header__mega-item", text="How it works")
        + _nav_anchor_link(anchor="sample", class_name="site-header__mega-item", text="Sample report")
        + "</div>"
        '<div class="site-header__mega-col">'
        '<p class="site-header__mega-heading">Support</p>'
        + _nav_anchor_link(anchor="pricing", class_name="site-header__mega-item", text="Plans &amp; pricing")
        + _nav_anchor_link(anchor="resources", class_name="site-header__mega-item", text="FAQ")
        + "</div>"
        "</div>"
        "</div>"
    )


def _resources_dropdown_html() -> str:
    return (
        '<div class="site-header__dropdown">'
        + _nav_anchor_link(
            anchor="resources",
            class_name="site-header__link site-header__dropdown-trigger",
            text=f"<span>Resources</span>{_CHEVRON_SVG}",
        )
        + f'<div class="site-header__dropdown-panel" role="menu">{_mega_menu_html()}</div>'
        "</div>"
    )


def _guest_primary_cta_html() -> str:
    return _nav_action_link(action="signup", class_name="site-header__cta", text="Start Free")


def _auth_primary_cta_html() -> str:
    return _nav_action_link(
        action="tool",
        class_name="site-header__cta site-header__cta--compact",
        text="Run evaluation",
    )


def _guest_drawer_actions_html() -> str:
    return (
        _nav_action_link(action="login", class_name="site-header__login", text="Log in")
        + _nav_action_link(action="signup", class_name="site-header__cta", text="Start Free")
    )


def _authenticated_drawer_actions_html(*, email: str, status_label: str, status_class: str) -> str:
    return (
        f'<div class="site-header__mobile-meta">'
        f'<span class="site-header__user">{html.escape(email)}</span>'
        f'<span class="check-row check-row--{status_class} site-header__quota">'
        f'<span class="check-dot"></span>{html.escape(status_label)}</span>'
        f"</div>"
        + _auth_primary_cta_html()
        + _nav_action_link(action="logout", class_name="site-header__text-action", text="Log out")
    )


def _mobile_nav_links_html() -> str:
    return (
        '<p class="site-header__mobile-kicker">Explore</p>'
        + _nav_anchor_link(anchor="pricing", class_name="site-header__mobile-link", text="Pricing")
        + _nav_anchor_link(anchor="process", class_name="site-header__mobile-link", text="How it works")
        + _nav_anchor_link(anchor="sample", class_name="site-header__mobile-link", text="Sample report")
        + _nav_anchor_link(anchor="resources", class_name="site-header__mobile-link", text="FAQ")
        + _nav_action_link(action="tool", class_name="site-header__mobile-link", text="Run evaluation")
    )


def _menu_button_html() -> str:
    return (
        '<button type="button" class="site-header__menu-btn" aria-label="Open menu" aria-expanded="false">'
        '<span class="site-header__menu-bar" aria-hidden="true"></span>'
        '<span class="site-header__menu-bar" aria-hidden="true"></span>'
        '<span class="site-header__menu-bar" aria-hidden="true"></span>'
        "</button>"
    )


def _mobile_drawer_shell_html(*, drawer_actions_html: str) -> str:
    return (
        '<div class="site-header__mobile-drawer" aria-hidden="true">'
        f'<nav class="site-header__mobile-nav" aria-label="Site">{_mobile_nav_links_html()}</nav>'
        f'<div class="site-header__mobile-actions">{drawer_actions_html}</div>'
        "</div>"
        '<div class="site-header__mobile-backdrop" aria-hidden="true"></div>'
    )


def _header_controls_html(*, logged_in: bool) -> str:
    primary = _auth_primary_cta_html() if logged_in else _guest_primary_cta_html()
    return f'<div class="site-header__controls">{primary}{_menu_button_html()}</div>'


def _build_site_header_html(*, drawer_actions_html: str, logged_in: bool) -> str:
    return (
        '<header class="site-header">'
        '<div class="site-header__bar">'
        '<div class="site-header__inner">'
        + _nav_action_link(
            action="home",
            class_name="site-header__brand",
            text=header_brand_html(),
        )
        + _header_controls_html(logged_in=logged_in)
        + _mobile_drawer_shell_html(drawer_actions_html=drawer_actions_html)
        + "</div>"
        "</div>"
        "</header>"
        '<div class="site-header__spacer" aria-hidden="true"></div>'
    )


def render_site_navbar() -> None:
    """Render the fixed top navigation bar."""
    logged_in = is_authenticated()
    user = get_current_user()

    drawer_actions = (
        _authenticated_drawer_actions_html(
            email=user.email,
            status_label=evaluations_status_label(),
            status_class="done" if user_can_run() else "pending",
        )
        if logged_in and user
        else _guest_drawer_actions_html()
    )

    _render_header_html(
        _build_site_header_html(drawer_actions_html=drawer_actions, logged_in=logged_in and user is not None)
    )
