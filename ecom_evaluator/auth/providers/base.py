"""Auth provider protocol and factory."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol

import streamlit as st

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.config import AUTH_PROVIDER, PROJECT_ROOT, QUOTA_STORE_PATH


@dataclass(frozen=True)
class AuthSettings:
    provider: str
    auth_required: bool
    supabase_url: str
    supabase_anon_key: str
    quota_backend: str
    dev_users_path: str
    oauth_redirect_url: str
    google_oauth_enabled: bool


class AuthProvider(Protocol):
    def login(self, credentials: AuthCredentials) -> AuthLoginResult: ...

    def sign_up(self, request: SignUpRequest) -> AuthLoginResult: ...

    def provider_label(self) -> str: ...


def _secret(key: str, default: str = "") -> str:
    try:
        value = st.secrets.get(key, default)
    except Exception:
        value = default
    if value:
        return str(value).strip()
    return os.getenv(key, default).strip()


def _nested_secret(section: str, key: str) -> str:
    try:
        block = st.secrets.get(section)
        if isinstance(block, dict):
            value = block.get(key)
            if value:
                return str(value).strip()
    except Exception:
        pass
    return ""


def resolve_supabase_url() -> str:
    return _secret("SUPABASE_URL") or _nested_secret("supabase", "url")


def resolve_supabase_anon_key() -> str:
    return _secret("SUPABASE_ANON_KEY") or _nested_secret("supabase", "anon_key")


def resolve_auth_redirect_url() -> str:
    """Public app URL for Supabase OAuth and email confirmation redirects."""
    settings = get_auth_settings()
    if settings.oauth_redirect_url:
        return settings.oauth_redirect_url.rstrip("/")
    return "http://localhost:8501"


def get_auth_settings() -> AuthSettings:
    provider = _secret("AUTH_PROVIDER", AUTH_PROVIDER).lower() or "dev"
    auth_required_raw = _secret("AUTH_REQUIRED", os.getenv("AUTH_REQUIRED", "true"))
    auth_required = auth_required_raw.lower() in ("1", "true", "yes", "on")
    quota_backend = _secret("QUOTA_BACKEND", "file" if provider == "dev" else "supabase").lower()
    google_oauth_raw = _secret("GOOGLE_OAUTH_ENABLED", "true" if provider == "supabase" else "false")
    google_oauth_enabled = google_oauth_raw.lower() in ("1", "true", "yes", "on")
    return AuthSettings(
        provider=provider,
        auth_required=auth_required,
        supabase_url=resolve_supabase_url(),
        supabase_anon_key=resolve_supabase_anon_key(),
        quota_backend=quota_backend,
        dev_users_path=_secret("DEV_USERS_PATH", str(PROJECT_ROOT / ".data" / "dev_users.json")),
        oauth_redirect_url=_secret("AUTH_REDIRECT_URL"),
        google_oauth_enabled=google_oauth_enabled,
    )


def get_auth_provider() -> AuthProvider:
    settings = get_auth_settings()
    if settings.provider == "supabase":
        from ecom_evaluator.auth.providers.supabase_provider import SupabaseAuthProvider

        return SupabaseAuthProvider(
            url=settings.supabase_url,
            anon_key=settings.supabase_anon_key,
        )
    if settings.provider == "streamlit_authenticator":
        from ecom_evaluator.auth.providers.streamlit_authenticator_provider import (
            StreamlitAuthenticatorProvider,
        )

        return StreamlitAuthenticatorProvider()
    from ecom_evaluator.auth.providers.dev_provider import DevAuthProvider

    return DevAuthProvider(users_path=settings.dev_users_path)
