"""Sign-in / sign-up screen (shown on demand, not on the landing page)."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.auth.oauth import (
    get_google_oauth_url,
    install_oauth_callback_bridge,
    resolve_oauth_redirect_url,
)
from ecom_evaluator.auth.providers.base import get_auth_settings
from ecom_evaluator.auth.providers.streamlit_authenticator_provider import StreamlitAuthenticatorProvider
from ecom_evaluator.auth.session import (
    clear_auth_error,
    login_with_credentials,
    render_auth_error,
    set_auth_user,
    sign_up_account,
)
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.ui.subscription import complete_post_auth_navigation, go_to_landing, open_auth_screen


def _finish_auth() -> None:
    complete_post_auth_navigation()
    st.rerun()


def _auth_headline() -> tuple[str, str]:
    intent = st.session_state.get("auth_intent")
    mode = st.session_state.get("auth_mode", "login")
    if intent == "evaluate":
        return (
            "Sign in to run your free evaluation",
            f"Log in or create an account — {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations included.",
        )
    if mode == "signup":
        return (
            "Create your free account",
            f"Get {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations and preview Sections 1–2.",
        )
    return (
        "Welcome back",
        "Log in to access your evaluations and saved quota.",
    )


def _render_login_form() -> None:
    with st.form("auth_login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@company.com", key="auth_login_email")
        password = st.text_input("Password", type="password", key="auth_login_password")
        submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)
    if submitted:
        clear_auth_error()
        try:
            login_with_credentials(email=email, password=password)
            _finish_auth()
        except AnalysisError as exc:
            st.error(str(exc))


def _render_signup_form() -> None:
    with st.form("auth_signup_form", clear_on_submit=False):
        name = st.text_input("Display name (optional)", key="auth_signup_name")
        email = st.text_input("Email", placeholder="you@company.com", key="auth_signup_email")
        password = st.text_input("Password", type="password", help="Minimum 8 characters", key="auth_signup_password")
        confirm = st.text_input("Confirm password", type="password", key="auth_signup_confirm")
        submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)
    if submitted:
        clear_auth_error()
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            try:
                sign_up_account(email=email, password=password, display_name=name or None)
                _finish_auth()
            except AnalysisError as exc:
                st.error(str(exc))


def _render_email_password_auth() -> None:
    mode = st.session_state.get("auth_mode", "login")
    if mode == "signup":
        _render_signup_form()
        if st.button("Already have an account? Log in", key="auth_switch_login"):
            open_auth_screen(mode="login", intent=st.session_state.get("auth_intent"))
    else:
        _render_login_form()
        if st.button("New here? Create a free account", key="auth_switch_signup"):
            open_auth_screen(mode="signup", intent=st.session_state.get("auth_intent"))


def _render_auth_panel() -> None:
    title, copy = _auth_headline()
    st.markdown(
        f"""
        <div class="auth-card auth-card--standalone">
            <p class="auth-card-kicker">Your account</p>
            <p class="auth-card-title">{title}</p>
            <p class="auth-card-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_google_sign_in() -> bool:
    settings = get_auth_settings()
    if not settings.google_oauth_enabled or settings.provider != "supabase":
        return False

    try:
        oauth_url = get_google_oauth_url()
    except (AnalysisError, RuntimeError):
        return False

    st.link_button(
        "Continue with Google",
        oauth_url,
        use_container_width=True,
        type="primary",
    )
    st.caption("Works for new and returning accounts.")
    st.markdown('<p class="auth-divider"><span>or use email</span></p>', unsafe_allow_html=True)
    return True


def _render_supabase_auth() -> None:
    install_oauth_callback_bridge()
    if not _render_google_sign_in():
        with st.expander("Google sign-in unavailable"):
            st.caption(f"Redirect URL: `{resolve_oauth_redirect_url()}`")
    _render_email_password_auth()


def _render_dev_auth() -> None:
    _render_email_password_auth()
    if get_auth_settings().provider == "dev":
        st.caption("Development auth — use Supabase in production.")


def _render_streamlit_authenticator() -> None:
    provider = StreamlitAuthenticatorProvider()
    user = provider.render_login_widget()
    if user is not None:
        set_auth_user(user)
        _finish_auth()


def render_auth_screen() -> None:
    """Compact auth screen — only shown when user clicks Log in, Get started, or Run evaluation."""
    _, center, _ = st.columns([0.15, 1.7, 0.15])
    with center:
        render_auth_error()
        _render_auth_panel()

        settings = get_auth_settings()
        if settings.provider == "streamlit_authenticator":
            _render_streamlit_authenticator()
        elif settings.provider == "supabase":
            _render_supabase_auth()
        else:
            _render_dev_auth()

        if st.button("← Back to home", key="auth_back_home"):
            go_to_landing()
