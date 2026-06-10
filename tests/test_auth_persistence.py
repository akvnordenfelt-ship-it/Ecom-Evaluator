"""Tests for cross-tab auth persistence helpers."""

import pytest

from ecom_evaluator.auth.persistence import (
    _restore_dev_user,
    decode_auth_cookie,
    encode_auth_cookie,
)
from ecom_evaluator.exceptions import AnalysisError


def test_auth_cookie_round_trip():
    payload = {
        "v": 1,
        "provider": "supabase",
        "user_id": "uuid-123",
        "email": "founder@example.com",
        "display_name": "Founder",
        "refresh_token": "refresh-token",
    }
    encoded = encode_auth_cookie(payload)
    assert decode_auth_cookie(encoded) == payload


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
