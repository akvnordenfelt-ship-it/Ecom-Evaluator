"""Tests for cross-tab auth persistence helpers."""

import base64
import json

import pytest

from ecom_evaluator.auth.persistence import _restore_dev_user
from ecom_evaluator.exceptions import AnalysisError


def test_restore_dev_user_decodes_payload(monkeypatch):
    monkeypatch.setattr(
        "ecom_evaluator.auth.persistence.get_auth_settings",
        lambda: type(
            "Settings",
            (),
            {"provider": "dev"},
        )(),
    )
    payload = {
        "user_id": "abc123",
        "email": "founder@example.com",
        "display_name": "Founder",
    }
    encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
    user = _restore_dev_user(encoded)
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
    encoded = base64.b64encode(b'{"user_id":"abc","email":"x@y.com"}').decode("ascii")
    with pytest.raises(AnalysisError):
        _restore_dev_user(encoded)
