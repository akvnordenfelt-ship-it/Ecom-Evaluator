"""Tests for cross-tab auth persistence helpers."""

import pytest

from urllib.parse import quote

from ecom_evaluator.auth.persistence import (
    _restore_dev_user,
    build_cookie_auth_payload,
    decode_auth_cookie,
    encode_auth_cookie,
    _decode_cookie_value,
)
from ecom_evaluator.exceptions import AnalysisError


def test_auth_cookie_round_trip():
    payload = {
        "v": 1,
        "provider": "supabase",
        "user_id": "uuid-123",
        "email": "founder@example.com",
        "refresh_token": "refresh-token",
    }
    encoded = encode_auth_cookie(payload)
    assert decode_auth_cookie(encoded) == payload
    assert _decode_cookie_value(encoded) == payload
    assert _decode_cookie_value(quote(encoded, safe="")) == payload


def test_cookie_payload_omits_access_token(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.persistence.build_browser_auth_payload",
        lambda: {
            "v": 1,
            "provider": "supabase",
            "user_id": "uuid-123",
            "email": "founder@example.com",
            "access_token": "access-token",
            "refresh_token": "refresh-token",
        },
    )
    cookie_payload = build_cookie_auth_payload()
    assert cookie_payload is not None
    assert cookie_payload.get("refresh_token") == "refresh-token"
    assert "access_token" not in cookie_payload


def test_restore_dev_user_from_payload(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.persistence.get_auth_settings",
        lambda: type(
            "Settings",
            (),
            {"provider": "dev"},
        )(),
    )
    user = _restore_dev_user(
        {
            "user_id": "abc123",
            "email": "founder@example.com",
            "display_name": "Founder",
        }
    )
    assert user.user_id == "abc123"
    assert user.email == "founder@example.com"
    assert user.display_name == "Founder"


def test_restore_dev_user_rejects_wrong_provider(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.persistence.get_auth_settings",
        lambda: type(
            "Settings",
            (),
            {"provider": "supabase"},
        )(),
    )
    with pytest.raises(AnalysisError):
        _restore_dev_user({"user_id": "abc", "email": "x@y.com"})


def test_restore_dev_user_requires_fields(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.persistence.get_auth_settings",
        lambda: type(
            "Settings",
            (),
            {"provider": "dev"},
        )(),
    )
    with pytest.raises(AnalysisError):
        _restore_dev_user({"user_id": "abc"})
