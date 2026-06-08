"""Public landing page with login and sign-up gate."""

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
from ecom_evaluator.ui.landing import (
    render_landing_at_a_glance,
    render_landing_body,
    render_landing_final_cta,
    render_landing_footnote,
    render_landing_hero,
)
from ecom_evaluator.ui.subscription import enter_tool_view


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


def _render_auth_panel(*, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="auth-card">
            <p class="auth-card-kicker">Your account</p>
            <p class="auth-card-title">{title}</p>
            <p class="auth-card-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_google_sign_in() -> bool:
    """Render Google button. Returns True when the button is shown."""
    settings = get_auth_settings()
    if not settings.google_oauth_enabled or settings.provider != "supabase":
        return False

    try:
        oauth_url = get_google_oauth_url()
    except AnalysisError:
        return False
    except RuntimeError:
        return False

    st.link_button(
        "Continue with Google",
        oauth_url,
        use_container_width=True,
        type="primary",
    )
    st.caption("Creates an account automatically on first Google sign-in.")
    st.markdown('<p class="auth-divider"><span>or use email</span></p>', unsafe_allow_html=True)
    return True


def _render_dev_auth_forms() -> None:
    _render_auth_panel(
        title="Log in or create an account to start",
        copy=f"Free accounts include {FREE_EVALUATIONS_PER_ACCOUNT} evaluations. Premium unlocks unlimited runs.",
    )
    _render_email_password_auth()


def _render_supabase_auth_forms() -> None:
    install_oauth_callback_bridge()
    _render_auth_panel(
        title="Continue with Google or email",
        copy=f"New and returning users get {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations per account.",
    )

    google_available = _render_google_sign_in()
    if not google_available:
        with st.expander("Google sign-in unavailable"):
            st.markdown(
                "Google sign-in needs the Supabase Python package on the server. "
                "If you deploy on Streamlit Cloud, push the latest `requirements.txt` and reboot the app."
            )
            st.code("pip install supabase", language="bash")
            st.caption(f"OAuth redirect URL: `{resolve_oauth_redirect_url()}`")

    _render_email_password_auth()


def _render_streamlit_authenticator() -> None:
    provider = StreamlitAuthenticatorProvider()
    user = provider.render_login_widget()
    if user is not None:
        set_auth_user(user)
        enter_tool_view()
        st.rerun()


def _render_auth_forms() -> None:
    settings = get_auth_settings()
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


def render_auth_gate() -> None:
    """Full marketing landing page with sign-in panel after the hero."""
    render_landing_hero()
    render_auth_error()
    _render_auth_forms()
    render_landing_at_a_glance()
    render_landing_body()
    render_landing_final_cta(show_buttons=False)
    render_landing_footnote()
