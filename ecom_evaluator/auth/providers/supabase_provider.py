"""Supabase authentication provider."""

from __future__ import annotations

from typing import Any

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.auth.providers.base import resolve_auth_redirect_url
from ecom_evaluator.exceptions import AnalysisError, SignupPendingConfirmation


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


def _session_tokens(session: Any) -> tuple[str | None, str | None]:
    if session is None:
        return None, None
    access_token = getattr(session, "access_token", None)
    refresh_token = getattr(session, "refresh_token", None)
    return (
        str(access_token) if access_token else None,
        str(refresh_token) if refresh_token else None,
    )


def _user_is_confirmed(user: Any) -> bool:
    confirmed_at = getattr(user, "email_confirmed_at", None) or getattr(user, "confirmed_at", None)
    return bool(confirmed_at)


def _auth_error_code(exc: Exception) -> str:
    code = getattr(exc, "code", None)
    return str(code).strip().lower() if code else ""


def _login_error_message(exc: Exception) -> str:
    message = str(exc).lower()
    code = _auth_error_code(exc)
    if "email not confirmed" in message or code in ("email_not_confirmed", "email_not_verified"):
        return "Confirm your email address first, then sign in."
    if code == "invalid_credentials" or "invalid login credentials" in message:
        return (
            "Could not sign in. Double-check your email and password — if you haven't verified yet, "
            "enter the 6-digit code from your signup email, or use Resend verification code below."
        )
    return "Incorrect email or password."


def _signup_error_message(exc: Exception) -> str:
    message = str(exc).lower()
    if "already registered" in message:
        return "An account with this email already exists. Log in instead."
    if "invalid api key" in message or "invalid jwt" in message:
        return (
            "Supabase rejected the API key. In Streamlit secrets, set SUPABASE_ANON_KEY to the "
            "legacy anon public key from Supabase → Project Settings → API → Legacy API Keys "
            "(a long JWT starting with eyJ…). Do not use the secret/service_role key."
        )
    if "confirmation mail" in message or "sending confirmation" in message:
        return (
            "We couldn't send the confirmation email. In Supabase, open Authentication → "
            "SMTP Settings and configure custom SMTP (Resend, SendGrid, etc.), then try again."
        )
    return f"Sign up failed: {exc}"


class SupabaseAuthProvider:
    def __init__(self, *, url: str, anon_key: str) -> None:
        if not url or not anon_key:
            raise RuntimeError(
                "Supabase auth requires SUPABASE_URL and SUPABASE_ANON_KEY in Streamlit secrets."
            )
        key = anon_key.strip()
        if key.startswith("sb_secret_"):
            raise RuntimeError(
                "SUPABASE_ANON_KEY must be the public anon/publishable key, not the secret key."
            )
        self._url = url.strip()
        self._anon_key = key
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

    def resend_confirmation_email(self, *, email: str) -> None:
        client = self._get_client()
        redirect_url = resolve_auth_redirect_url()
        try:
            client.auth.resend(
                {
                    "type": "signup",
                    "email": email.strip().lower(),
                    "options": {"email_redirect_to": redirect_url},
                }
            )
        except Exception as exc:
            message = str(exc).lower()
            if "confirmation mail" in message or "sending confirmation" in message:
                raise AnalysisError(
                    "We couldn't send the confirmation email. Configure custom SMTP in Supabase, "
                    "then try again."
                ) from exc
            raise AnalysisError(f"Could not resend confirmation email: {exc}") from exc

    def verify_email_otp(self, *, email: str, token: str) -> AuthLoginResult:
        client = self._get_client()
        normalized_email = email.strip().lower()
        normalized_token = token.strip()
        if not normalized_token:
            raise AnalysisError("Enter the verification code from your email.")

        last_error: Exception | None = None
        for otp_type in ("signup", "email"):
            try:
                response = client.auth.verify_otp(
                    {
                        "email": normalized_email,
                        "token": normalized_token,
                        "type": otp_type,
                    }
                )
            except Exception as exc:
                last_error = exc
                continue

            access_token, refresh_token = _session_tokens(getattr(response, "session", None))
            user = getattr(response, "user", None)
            if user is None or not getattr(user, "id", None):
                raise AnalysisError("Verification succeeded but no user was returned. Try signing in.")
            return AuthLoginResult(
                user=user_from_supabase_record(user),
                access_token=access_token,
                refresh_token=refresh_token,
            )

        raise AnalysisError(
            "Invalid or expired verification code. Request a new code and try again."
        ) from last_error

    def complete_email_confirmation(self, *, token_hash: str, confirmation_type: str) -> AuthLoginResult:
        client = self._get_client()
        try:
            response = client.auth.verify_otp(
                {"token_hash": token_hash, "type": confirmation_type}
            )
        except Exception as exc:
            raise AnalysisError(
                "Email confirmation link is invalid or expired. Request a new verification code."
            ) from exc

        access_token, refresh_token = _session_tokens(getattr(response, "session", None))
        user = getattr(response, "user", None)
        if user is None or not getattr(user, "id", None):
            raise AnalysisError(
                "Email confirmation link is invalid or expired. Request a new verification code."
            )
        return AuthLoginResult(
            user=user_from_supabase_record(user),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def login(self, credentials: AuthCredentials) -> AuthLoginResult:
        client = self._get_client()
        try:
            response = client.auth.sign_in_with_password(
                {"email": credentials.email.strip().lower(), "password": credentials.password}
            )
        except Exception as exc:
            raise AnalysisError(_login_error_message(exc)) from exc

        access_token, refresh_token = _session_tokens(getattr(response, "session", None))
        return AuthLoginResult(
            user=user_from_supabase_record(response.user),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh_session(self, *, refresh_token: str) -> AuthLoginResult:
        client = self._get_client()
        try:
            response = client.auth.refresh_session(refresh_token)
        except Exception as exc:
            raise AnalysisError("Your session expired. Log in again.") from exc

        session = getattr(response, "session", None)
        user = getattr(response, "user", None)
        if user is None and session is not None:
            user = getattr(session, "user", None)
        access_token = getattr(session, "access_token", None) if session else None
        new_refresh = getattr(session, "refresh_token", None) if session else None
        return AuthLoginResult(
            user=user_from_supabase_record(user),
            access_token=str(access_token) if access_token else None,
            refresh_token=str(new_refresh or refresh_token),
        )

    def sign_up(self, request: SignUpRequest) -> AuthLoginResult:
        client = self._get_client()
        if len(request.password) < 8:
            raise AnalysisError("Password must be at least 8 characters.")
        metadata = {}
        if request.display_name:
            metadata["display_name"] = request.display_name.strip()
        redirect_url = resolve_auth_redirect_url()
        options: dict[str, object] = {"email_redirect_to": redirect_url}
        if metadata:
            options["data"] = metadata
        try:
            response = client.auth.sign_up(
                {
                    "email": request.email.strip().lower(),
                    "password": request.password,
                    "options": options,
                }
            )
        except Exception as exc:
            raise AnalysisError(_signup_error_message(exc)) from exc

        user = response.user
        if user is None or not user.id:
            raise AnalysisError(
                "Account created — check your email to confirm, then log in."
            )

        identities = getattr(user, "identities", None)
        if identities is not None and len(identities) == 0:
            raise AnalysisError("An account with this email already exists. Log in instead.")

        if not _user_is_confirmed(user):
            raise SignupPendingConfirmation(request.email.strip().lower())

        access_token, refresh_token = _session_tokens(getattr(response, "session", None))
        return AuthLoginResult(
            user=user_from_supabase_record(user),
            access_token=access_token,
            refresh_token=refresh_token,
        )
