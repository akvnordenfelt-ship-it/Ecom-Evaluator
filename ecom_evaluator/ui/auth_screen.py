"""Sign-in / sign-up screen (shown on demand, not on the landing page)."""

from __future__ import annotations

import html

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
    clear_pending_signup,
    login_with_credentials,
    render_auth_error,
    resend_signup_confirmation,
    set_auth_user,
    sign_up_account,
    verify_signup_code,
)
from ecom_evaluator.exceptions import AnalysisError, SignupPendingConfirmation
from ecom_evaluator.ui.subscription import complete_post_auth_navigation, open_auth_screen

_GOOGLE_ICON_SVG = (
    '<svg class="auth-oauth-icon" width="18" height="18" viewBox="0 0 48 48" aria-hidden="true">'
    '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
    '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
    '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
    '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>'
    "</svg>"
)


def _finish_auth() -> None:
    complete_post_auth_navigation()
    st.rerun()


def _auth_title() -> str:
    if st.session_state.get("auth_pending_email"):
        return "Verify your email"
    mode = st.session_state.get("auth_mode", "login")
    if mode == "signup":
        return "Create your account"
    return "Sign in"


def _auth_subtitle() -> str:
    pending = st.session_state.get("auth_pending_email")
    if pending:
        return f"Enter the verification code we sent to {pending}."
    mode = st.session_state.get("auth_mode", "login")
    if mode == "signup":
        return "Start with a free preview — no credit card required."
    return "Access your evaluations, scores, and saved reports."


def _google_oauth_button_html(oauth_url: str) -> str:
    safe_url = html.escape(oauth_url, quote=True)
    return (
        f'<a class="auth-oauth-btn" href="{safe_url}" target="_self">'
        f"{_GOOGLE_ICON_SVG}"
        "<span>Continue with Google</span>"
        "</a>"
    )


def _render_auth_header() -> None:
    title = html.escape(_auth_title())
    subtitle = html.escape(_auth_subtitle())
    st.markdown(
        '<div class="auth-form-header">'
        '<a class="auth-form-back" href="#" data-ps-nav-action="home" target="_self">← Back to home</a>'
        '<div class="auth-wordmark"><span class="auth-wordmark__mark" aria-hidden="true">🦈</span>'
        '<span class="auth-wordmark__name">ProductScore</span></div>'
        f'<h1 class="auth-form-title">{title}</h1>'
        f'<p class="auth-form-lead">{subtitle}</p>'
        "</div>",
        unsafe_allow_html=True,
    )


def _render_auth_divider() -> None:
    st.markdown(
        '<div class="auth-form-divider" role="separator">'
        '<span>or continue with email</span></div>',
        unsafe_allow_html=True,
    )


def _render_auth_footer() -> None:
    st.markdown(
        '<div class="auth-form-legal">'
        "<p>By continuing, you agree to our Terms of Service and Privacy Policy.</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def _render_login_form() -> None:
    with st.form("auth_login_form", clear_on_submit=False):
        st.markdown('<p class="auth-field-label">Email</p>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@company.com", key="auth_login_email", label_visibility="collapsed")
        st.markdown('<p class="auth-field-label">Password</p>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", key="auth_login_password", label_visibility="collapsed")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)
    if submitted:
        clear_auth_error()
        try:
            login_with_credentials(email=email, password=password)
            _finish_auth()
        except AnalysisError as exc:
            st.error(str(exc))

    if get_auth_settings().provider == "supabase":
        if st.button("Resend verification code", key="auth_resend_confirmation", use_container_width=True):
            email_value = str(st.session_state.get("auth_login_email", "")).strip()
            if not email_value:
                st.error("Enter your email above first.")
            else:
                try:
                    resend_signup_confirmation(email=email_value)
                    st.success("Verification code sent. Check your inbox and spam folder.")
                except AnalysisError as exc:
                    st.error(str(exc))


def _render_verify_email_form() -> None:
    pending_email = str(st.session_state.get("auth_pending_email", "")).strip()
    if not pending_email:
        clear_pending_signup()
        st.rerun()
        return

    with st.form("auth_verify_form", clear_on_submit=False):
        st.markdown('<p class="auth-field-label">Verification code</p>', unsafe_allow_html=True)
        code = st.text_input(
            "Verification code",
            placeholder="12345678",
            key="auth_verify_code",
            label_visibility="collapsed",
            max_chars=8,
        )
        submitted = st.form_submit_button("Verify and continue", type="primary", use_container_width=True)

    if submitted:
        clear_auth_error()
        try:
            verify_signup_code(email=pending_email, code=code)
            _finish_auth()
        except AnalysisError as exc:
            st.error(str(exc))

    if st.button("Resend code", key="auth_resend_verify_code", use_container_width=True):
        try:
            resend_signup_confirmation(email=pending_email)
            st.success("New verification code sent.")
        except AnalysisError as exc:
            st.error(str(exc))

    if st.button("Back to sign in", key="auth_verify_back_login"):
        clear_pending_signup()
        open_auth_screen(mode="login", intent=st.session_state.get("auth_intent"))


def _render_signup_form() -> None:
    with st.form("auth_signup_form", clear_on_submit=False):
        st.markdown('<p class="auth-field-label">Email</p>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@company.com", key="auth_signup_email", label_visibility="collapsed")
        st.markdown(
            '<p class="auth-field-label">Display name <span class="auth-field-optional">(optional)</span></p>',
            unsafe_allow_html=True,
        )
        name = st.text_input("Display name", placeholder="Alex", key="auth_signup_name", label_visibility="collapsed")
        st.markdown('<p class="auth-field-label">Password</p>', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", key="auth_signup_password", label_visibility="collapsed")
        st.markdown('<p class="auth-field-label">Confirm password</p>', unsafe_allow_html=True)
        confirm = st.text_input("Confirm password", type="password", key="auth_signup_confirm", label_visibility="collapsed")
        submitted = st.form_submit_button("Create account", type="primary", use_container_width=True)
    if submitted:
        clear_auth_error()
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            try:
                sign_up_account(email=email, password=password, display_name=name or None)
                _finish_auth()
            except SignupPendingConfirmation as pending:
                st.session_state["auth_pending_email"] = pending.email
                st.rerun()
            except AnalysisError as exc:
                st.error(str(exc))


def _render_email_password_auth() -> None:
    mode = st.session_state.get("auth_mode", "login")
    if mode == "signup":
        _render_signup_form()
        if st.button("Already have an account? Sign in", key="auth_switch_login"):
            open_auth_screen(mode="login", intent=st.session_state.get("auth_intent"))
    else:
        _render_login_form()
        if st.button("New here? Create a free account", key="auth_switch_signup"):
            open_auth_screen(mode="signup", intent=st.session_state.get("auth_intent"))


def _render_google_sign_in() -> bool:
    settings = get_auth_settings()
    if not settings.google_oauth_enabled or settings.provider != "supabase":
        return False

    try:
        oauth_url = get_google_oauth_url()
    except (AnalysisError, RuntimeError):
        return False

    st.markdown(_google_oauth_button_html(oauth_url), unsafe_allow_html=True)
    _render_auth_divider()
    return True


def _render_supabase_auth() -> None:
    install_oauth_callback_bridge()
    if st.session_state.get("auth_pending_email"):
        _render_verify_email_form()
        return
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
    """Centered auth form — login and signup."""
    st.markdown('<div class="auth-page-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    _, center, _ = st.columns([1, 1.05, 1])
    with center:
        _render_auth_header()
        render_auth_error()

        settings = get_auth_settings()
        if settings.provider == "streamlit_authenticator":
            _render_streamlit_authenticator()
        elif settings.provider == "supabase":
            _render_supabase_auth()
        else:
            _render_dev_auth()

        _render_auth_footer()
