"""Tests for Supabase user mapping helpers."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ecom_evaluator.auth.models import SignUpRequest
from ecom_evaluator.auth.providers.supabase_provider import (
    SupabaseAuthProvider,
    _login_error_message,
    _signup_error_message,
    user_from_supabase_record,
)
from ecom_evaluator.exceptions import AnalysisError, SignupPendingConfirmation


def test_user_from_google_metadata():
    user = SimpleNamespace(
        id="uuid-123",
        email="founder@gmail.com",
        user_metadata={"full_name": "Alex Founder", "avatar_url": "https://example.com/a.png"},
    )
    auth_user = user_from_supabase_record(user)
    assert auth_user.user_id == "uuid-123"
    assert auth_user.email == "founder@gmail.com"
    assert auth_user.display_name == "Alex Founder"


def test_user_from_supabase_record_requires_id():
    with pytest.raises(AnalysisError):
        user_from_supabase_record(SimpleNamespace(id=None, email="x@y.com", user_metadata={}))


def test_login_error_message_email_not_confirmed():
    assert "Confirm your email" in _login_error_message(Exception("Email not confirmed"))


def test_login_error_message_invalid_credentials():
    exc = Exception("Invalid login credentials")
    exc.code = "invalid_credentials"  # type: ignore[attr-defined]
    assert "verification code" in _login_error_message(exc).lower()


def test_signup_error_message_smtp_failure():
    assert "SMTP" in _signup_error_message(Exception("Error sending confirmation mail"))


def test_signup_error_message_invalid_api_key():
    message = _signup_error_message(Exception("Invalid API key"))
    assert "legacy anon" in message.lower()


def test_sign_up_requires_email_confirmation_before_login(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.providers.supabase_provider.resolve_auth_redirect_url",
        lambda: "http://localhost:8501",
    )
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            identities=[SimpleNamespace(id="identity-1")],
            email_confirmed_at=None,
            confirmed_at=None,
        ),
        session=None,
    )
    provider._client = mock_client

    with pytest.raises(SignupPendingConfirmation) as exc_info:
        provider.sign_up(SignUpRequest(email="founder@example.com", password="password123"))

    assert exc_info.value.email == "founder@example.com"
    sign_up_call = mock_client.auth.sign_up.call_args[0][0]
    assert sign_up_call["options"]["email_redirect_to"] == "http://localhost:8501"
    mock_client.auth.resend.assert_not_called()


def test_sign_up_blocks_auto_login_when_unconfirmed_even_with_session(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.providers.supabase_provider.resolve_auth_redirect_url",
        lambda: "http://localhost:8501",
    )
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            identities=[SimpleNamespace(id="identity-1")],
            email_confirmed_at=None,
            confirmed_at=None,
        ),
        session=SimpleNamespace(access_token="access", refresh_token="refresh"),
    )
    provider._client = mock_client

    with pytest.raises(SignupPendingConfirmation):
        provider.sign_up(SignUpRequest(email="founder@example.com", password="password123"))


def test_verify_email_otp():
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.verify_otp.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            email_confirmed_at="2026-01-01T00:00:00Z",
        ),
        session=SimpleNamespace(access_token="access", refresh_token="refresh"),
    )
    provider._client = mock_client

    result = provider.verify_email_otp(email="founder@example.com", token="123456")
    assert result.user.email == "founder@example.com"
    assert result.access_token == "access"
    mock_client.auth.verify_otp.assert_called_once_with(
        {"email": "founder@example.com", "token": "123456", "type": "signup"}
    )


def test_sign_up_passes_auth_redirect_url(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.providers.supabase_provider.resolve_auth_redirect_url",
        lambda: "https://app.example.com",
    )
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            identities=[SimpleNamespace(id="identity-1")],
            email_confirmed_at=None,
            confirmed_at=None,
        ),
        session=None,
    )
    provider._client = mock_client

    with pytest.raises(SignupPendingConfirmation):
        provider.sign_up(SignUpRequest(email="founder@example.com", password="password123"))

    sign_up_call = mock_client.auth.sign_up.call_args[0][0]
    assert sign_up_call["options"]["email_redirect_to"] == "https://app.example.com"


def test_resend_confirmation_email(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.providers.supabase_provider.resolve_auth_redirect_url",
        lambda: "http://localhost:8501",
    )
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    provider._client = mock_client

    provider.resend_confirmation_email(email="Founder@Example.com")

    mock_client.auth.resend.assert_called_once_with(
        {
            "type": "signup",
            "email": "founder@example.com",
            "options": {"email_redirect_to": "http://localhost:8501"},
        }
    )


def test_sign_up_returns_session_when_email_auto_confirmed():
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            identities=[SimpleNamespace(id="identity-1")],
            email_confirmed_at="2026-01-01T00:00:00Z",
            confirmed_at=None,
        ),
        session=SimpleNamespace(access_token="access", refresh_token="refresh"),
    )
    provider._client = mock_client

    result = provider.sign_up(SignUpRequest(email="founder@example.com", password="password123"))
    assert result.user.email == "founder@example.com"
    assert result.access_token == "access"
    assert result.refresh_token == "refresh"


def test_sign_up_rejects_duplicate_email_without_identities():
    provider = SupabaseAuthProvider(url="https://example.supabase.co", anon_key="anon-key")
    mock_client = MagicMock()
    mock_client.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(
            id="uuid-1",
            email="founder@example.com",
            user_metadata={},
            identities=[],
            email_confirmed_at="2026-01-01T00:00:00Z",
            confirmed_at=None,
        ),
        session=None,
    )
    provider._client = mock_client

    with pytest.raises(AnalysisError, match="already exists"):
        provider.sign_up(SignUpRequest(email="founder@example.com", password="password123"))
