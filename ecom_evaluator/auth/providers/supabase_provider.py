"""Supabase authentication provider."""

from __future__ import annotations

from typing import Any

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.exceptions import AnalysisError


def user_from_supabase_record(user: Any) -> AuthUser:
    if user is None or not getattr(user, "id", None):
        raise AnalysisError("Supabase login failed. No user returned.")

    metadata = user.user_metadata or {}
    if not isinstance(metadata, dict):
        metadata = {}

    email = (
        getattr(user, "email", None)
        or metadata.get("email")
        or metadata.get("preferred_username")
        or ""
    )
    display_name = (
        metadata.get("full_name")
        or metadata.get("name")
        or metadata.get("display_name")
        or (str(email).split("@")[0] if email else None)
    )
    return AuthUser(user_id=str(user.id), email=str(email), display_name=display_name)


class SupabaseAuthProvider:
    def __init__(self, *, url: str, anon_key: str) -> None:
        if not url or not anon_key:
            raise RuntimeError(
                "Supabase auth requires SUPABASE_URL and SUPABASE_ANON_KEY in Streamlit secrets."
            )
        self._url = url
        self._anon_key = anon_key
        self._client = None

    def provider_label(self) -> str:
        return "Supabase"

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError(
                "Install Supabase support with: pip install supabase"
            ) from exc
        self._client = create_client(self._url, self._anon_key)
        return self._client

    def get_google_oauth_url(self, *, redirect_to: str) -> str:
        client = self._get_client()
        try:
            response = client.auth.sign_in_with_oauth(
                {
                    "provider": "google",
                    "options": {"redirect_to": redirect_to},
                }
            )
        except Exception as exc:
            raise AnalysisError(f"Could not start Google sign-in: {exc}") from exc

        oauth_url = getattr(response, "url", None)
        if not oauth_url:
            raise AnalysisError("Supabase did not return a Google sign-in URL.")
        return str(oauth_url)

    def complete_session_tokens(self, *, access_token: str, refresh_token: str) -> AuthUser:
        client = self._get_client()
        try:
            response = client.auth.set_session(access_token, refresh_token)
            user = getattr(response, "user", None)
            if user is None:
                user_response = client.auth.get_user()
                user = getattr(user_response, "user", user_response)
        except Exception as exc:
            raise AnalysisError(
                "Google sign-in could not be completed. Try again or use email/password."
            ) from exc

        return user_from_supabase_record(user)

    def complete_oauth_code(self, *, code: str) -> AuthLoginResult:
        client = self._get_client()
        try:
            response = client.auth.exchange_code_for_session({"auth_code": code})
        except TypeError:
            response = client.auth.exchange_code_for_session(code)
        except Exception as exc:
            raise AnalysisError(
                "Google sign-in could not be completed. Try again or use email/password."
            ) from exc

        user = getattr(response, "user", None)
        if user is None and isinstance(response, dict):
            user = response.get("user")
        session = getattr(response, "session", None)
        if session is None and isinstance(response, dict):
            session = response.get("session")
        access_token = getattr(session, "access_token", None) if session else None
        refresh_token = getattr(session, "refresh_token", None) if session else None
        return AuthLoginResult(
            user=user_from_supabase_record(user),
            access_token=str(access_token) if access_token else None,
            refresh_token=str(refresh_token) if refresh_token else None,
        )

    def login(self, credentials: AuthCredentials) -> AuthLoginResult:
        client = self._get_client()
        try:
            response = client.auth.sign_in_with_password(
                {"email": credentials.email.strip().lower(), "password": credentials.password}
            )
        except Exception as exc:
            raise AnalysisError("Incorrect email or password.") from exc

        session = getattr(response, "session", None)
        access_token = getattr(session, "access_token", None) if session else None
        refresh_token = getattr(session, "refresh_token", None) if session else None
        return AuthLoginResult(
            user=user_from_supabase_record(response.user),
            access_token=str(access_token) if access_token else None,
            refresh_token=str(refresh_token) if refresh_token else None,
        )

    def sign_up(self, request: SignUpRequest) -> AuthUser:
        client = self._get_client()
        if len(request.password) < 8:
            raise AnalysisError("Password must be at least 8 characters.")
        metadata = {}
        if request.display_name:
            metadata["display_name"] = request.display_name.strip()
        try:
            response = client.auth.sign_up(
                {
                    "email": request.email.strip().lower(),
                    "password": request.password,
                    "options": {"data": metadata} if metadata else {},
                }
            )
        except Exception as exc:
            message = str(exc)
            if "already registered" in message.lower():
                raise AnalysisError("An account with this email already exists. Log in instead.") from exc
            raise AnalysisError(f"Sign up failed: {message}") from exc

        user = response.user
        if user is None or not user.id:
            raise AnalysisError(
                "Account created — check your email to confirm, then log in."
            )
        return user_from_supabase_record(user)
