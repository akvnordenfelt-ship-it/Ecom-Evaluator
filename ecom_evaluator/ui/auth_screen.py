"""Public landing page with login and sign-up gate."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.auth.oauth import (
    get_google_oauth_url,
    install_oauth_callback_bridge,
    resolve_oauth_redirect_url,
)
from ecom_evaluator.auth.providers.base import get_auth_provider, get_auth_settings
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
from ecom_evaluator.ui.subscription import enter_tool_view


def _render_marketing_hero() -> None:
    st.markdown(
        f"""
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Know if your product can win — before you spend a dollar</h1>
                <p class="landing-lead">
                    Create a free account to preview Sections 1–2: your product profile score and
                    brutal red-flag analysis. Premium unlocks the financial verdict and full execution stack.
                </p>
                <div class="lp-hero-badges">
                    <span class="lp-hero-badge">{FREE_EVALUATIONS_PER_ACCOUNT} free evaluations / account</span>
                    <span class="lp-hero-badge">Sections 1–2 preview</span>
                    <span class="lp-hero-badge">Premium · $29/mo</span>
                    <span class="lp-hero-badge">Secure login</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_value_strip() -> None:
    st.markdown(
        f"""
        <div class="lp-value-grid">
            <div class="lp-value-tile">
                <span class="lp-value-icon">🔐</span>
                <p class="lp-value-title">Account required</p>
                <p class="lp-value-desc">Log in to protect your quota and save your evaluation history</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">🎯</span>
                <p class="lp-value-title">{FREE_EVALUATIONS_PER_ACCOUNT} free runs</p>
                <p class="lp-value-desc">Each account gets {FREE_EVALUATIONS_PER_ACCOUNT} full free-tier evaluations</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">📋</span>
                <p class="lp-value-title">Sections 1–2 free</p>
                <p class="lp-value-desc">Profile metrics and Shark Tank red flags before you upgrade</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">🚀</span>
                <p class="lp-value-title">Premium unlocks all 6</p>
                <p class="lp-value-desc">Verdict, marketing blueprint, live intel, and video scripts</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_email_password_auth(*, signup_enabled: bool = True) -> None:
    tab_login, tab_signup = st.tabs(["Log in", "Create account"])

    with tab_login:
        with st.form("auth_login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@company.com", key="auth_login_email")
            password = st.text_input("Password", type="password", key="auth_login_password")
            submitted = st.form_submit_button("Log in", type="primary", use_container_width=True)
        if submitted:
            clear_auth_error()
            try:
                login_with_credentials(email=email, password=password)
                enter_tool_view()
                st.rerun()
            except AnalysisError as exc:
                st.error(str(exc))

    with tab_signup:
        if not signup_enabled:
            st.info("Sign up with Google above, or ask an admin to invite you.")
            return
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
                    enter_tool_view()
                    st.rerun()
                except AnalysisError as exc:
                    st.error(str(exc))


def _render_dev_auth_forms() -> None:
    st.markdown(
        f"""
        <div class="auth-card">
            <p class="auth-card-kicker">Your account</p>
            <p class="auth-card-title">Log in or create an account to start</p>
            <p class="auth-card-copy">Free accounts include {FREE_EVALUATIONS_PER_ACCOUNT} evaluations. Premium unlocks unlimited runs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_email_password_auth()


def _render_supabase_auth_forms() -> None:
    settings = get_auth_settings()
    install_oauth_callback_bridge()

    st.markdown(
        f"""
        <div class="auth-card">
            <p class="auth-card-kicker">Your account</p>
            <p class="auth-card-title">Continue with Google or email</p>
            <p class="auth-card-copy">New and returning users get {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations per account.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if settings.google_oauth_enabled:
        try:
            oauth_url = get_google_oauth_url()
            st.link_button(
                "Continue with Google",
                oauth_url,
                use_container_width=True,
                type="primary",
            )
            st.caption("Creates an account automatically on first Google sign-in.")
        except AnalysisError as exc:
            st.warning(str(exc))
        except RuntimeError as exc:
            st.warning(str(exc))

        st.markdown('<p class="auth-divider"><span>or use email</span></p>', unsafe_allow_html=True)

    _render_email_password_auth()

    with st.expander("Google sign-in troubleshooting"):
        st.code(resolve_oauth_redirect_url(), language=None)
        st.caption("Add this exact URL under Supabase → Authentication → URL Configuration → Redirect URLs.")


def _render_streamlit_authenticator() -> None:
    provider = StreamlitAuthenticatorProvider()
    user = provider.render_login_widget()
    if user is not None:
        set_auth_user(user)
        enter_tool_view()
        st.rerun()


def render_auth_gate() -> None:
    """Marketing landing + authentication wall."""
    settings = get_auth_settings()
    _render_marketing_hero()
    _render_value_strip()
    render_auth_error()

    if settings.provider == "streamlit_authenticator":
        _render_streamlit_authenticator()
    elif settings.provider == "supabase":
        _render_supabase_auth_forms()
    else:
        _render_dev_auth_forms()
        if settings.provider == "dev":
            st.caption(
                "Development auth is active. Google sign-in requires `AUTH_PROVIDER = \"supabase\"`."
            )

    st.markdown(
        '<p class="landing-footnote">ProductScore · Built for e-commerce operators</p>',
        unsafe_allow_html=True,
    )
