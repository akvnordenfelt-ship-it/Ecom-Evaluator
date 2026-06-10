"""Streamlit-Authenticator provider adapter."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.auth.providers.base import _secret


class StreamlitAuthenticatorProvider:
    """
    Wraps `streamlit-authenticator` credentials from secrets.

    Expected secrets structure:
    [authenticator]
    cookie_name = "productscore_auth"
    cookie_key = "replace-with-random-key"
    cookie_expiry_days = 30

    [authenticator.credentials.usernames.alice]
    email = "alice@example.com"
    name = "Alice"
    password = "$2b$12$..."  # bcrypt hash
    """

    def provider_label(self) -> str:
        return "Streamlit Authenticator"

    def _authenticator(self):
        try:
            import streamlit_authenticator as stauth
        except ImportError as exc:
            raise RuntimeError(
                "Install Streamlit Authenticator with: pip install streamlit-authenticator"
            ) from exc

        config = st.secrets.get("authenticator")
        if not config:
            raise RuntimeError(
                "Missing [authenticator] block in Streamlit secrets for streamlit_authenticator provider."
            )
        credentials = config.get("credentials")
        if not credentials:
            raise RuntimeError("Missing [authenticator.credentials] in Streamlit secrets.")

        return stauth.Authenticate(
            credentials,
            config.get("cookie_name", "productscore_auth"),
            config.get("cookie_key", "change-me"),
            cookie_expiry_days=int(config.get("cookie_expiry_days", 30)),
        )

    def login(self, credentials: AuthCredentials) -> AuthLoginResult:
        raise AnalysisError(
            "Streamlit Authenticator handles login in the UI layer. "
            "Use render_authenticator_widget() from the auth screen."
        )

    def sign_up(self, request: SignUpRequest) -> AuthUser:
        raise AnalysisError("Self-serve sign up is not enabled for Streamlit Authenticator.")

    def render_login_widget(self) -> AuthUser | None:
        authenticator = self._authenticator()
        authenticator.login(location="main", key="productscore_authenticator_login")
        name = st.session_state.get("name")
        username = st.session_state.get("username")
        auth_status = st.session_state.get("authentication_status")
        if auth_status and username:
            credentials = st.secrets["authenticator"]["credentials"]["usernames"][username]
            email = credentials.get("email", username)
            return AuthUser(user_id=str(username), email=str(email), display_name=str(name or username))
        return None
