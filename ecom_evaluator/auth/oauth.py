"""Supabase OAuth helpers for Streamlit (Google sign-in / sign-up)."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.auth.providers.base import get_auth_settings, resolve_auth_redirect_url
from ecom_evaluator.auth.session import set_auth_error, set_auth_user
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.ui.subscription import complete_post_auth_navigation

_OAUTH_QUERY_KEYS = (
    "code",
    "access_token",
    "refresh_token",
    "expires_in",
    "expires_at",
    "token_type",
    "provider_token",
    "provider_refresh_token",
    "type",
    "token_hash",
    "error",
    "error_description",
)


def resolve_oauth_redirect_url() -> str:
    """Public URL where Supabase redirects after Google auth (must be allowlisted)."""
    return resolve_auth_redirect_url()


def install_oauth_callback_bridge() -> None:
    """
    Supabase returns tokens in the URL hash (#access_token=...).
    Streamlit cannot read the hash server-side, so this script copies hash params
    into query params on the parent page, then reloads once.
    """
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const hash = win.location.hash;
            if (!hash || hash.length < 2) return;
            if (win.location.search.includes("access_token=")) return;
            if (win.location.search.includes("code=")) return;

            const params = new URLSearchParams(hash.substring(1));
            if (!params.get("access_token") && !params.get("error") && !params.get("token_hash")) return;

            const next = win.location.pathname + "?" + params.toString();
            win.location.replace(next);
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _clear_oauth_query_params() -> None:
    for key in _OAUTH_QUERY_KEYS:
        if key in st.query_params:
            del st.query_params[key]


def _get_supabase_provider():
    from ecom_evaluator.auth.providers.supabase_provider import SupabaseAuthProvider

    settings = get_auth_settings()
    return SupabaseAuthProvider(url=settings.supabase_url, anon_key=settings.supabase_anon_key)


def get_google_oauth_url() -> str:
    provider = _get_supabase_provider()
    return provider.get_google_oauth_url(redirect_to=resolve_oauth_redirect_url())


def handle_oauth_callback() -> bool:
    """
    Complete a Supabase auth redirect if query params are present.
    Handles Google OAuth, email confirmation links, and magic-link tokens.
    Returns True when the user was authenticated (caller should rerun).
    """
    settings = get_auth_settings()
    if settings.provider != "supabase":
        return False

    error = st.query_params.get("error")
    if error:
        description = st.query_params.get("error_description") or error
        set_auth_error(f"Sign-in failed: {description}")
        _clear_oauth_query_params()
        return False

    token_hash = st.query_params.get("token_hash")
    confirm_type = st.query_params.get("type")
    if token_hash and confirm_type in ("signup", "email", "magiclink", "recovery"):
        try:
            provider = _get_supabase_provider()
            result = provider.complete_email_confirmation(
                token_hash=str(token_hash),
                confirmation_type=str(confirm_type),
            )
            set_auth_user(
                result.user,
                access_token=result.access_token,
                refresh_token=result.refresh_token,
            )
            _clear_oauth_query_params()
            complete_post_auth_navigation()
            return True
        except AnalysisError as exc:
            set_auth_error(str(exc))
            _clear_oauth_query_params()
            return False

    access_token = st.query_params.get("access_token")
    refresh_token = st.query_params.get("refresh_token")
    if access_token and refresh_token:
        try:
            provider = _get_supabase_provider()
            user = provider.complete_session_tokens(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            set_auth_user(
                user,
                access_token=str(access_token),
                refresh_token=str(refresh_token),
            )
            _clear_oauth_query_params()
            complete_post_auth_navigation()
            return True
        except AnalysisError as exc:
            set_auth_error(str(exc))
            _clear_oauth_query_params()
            return False

    code = st.query_params.get("code")
    if code:
        try:
            provider = _get_supabase_provider()
            result = provider.complete_oauth_code(code=code)
            set_auth_user(
                result.user,
                access_token=result.access_token,
                refresh_token=result.refresh_token,
            )
            _clear_oauth_query_params()
            complete_post_auth_navigation()
            return True
        except AnalysisError as exc:
            set_auth_error(str(exc))
            _clear_oauth_query_params()
            return False

    return False
