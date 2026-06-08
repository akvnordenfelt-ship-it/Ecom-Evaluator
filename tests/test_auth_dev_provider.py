"""Tests for development auth provider."""

import pytest

from ecom_evaluator.auth.providers.dev_provider import DevAuthProvider
from ecom_evaluator.exceptions import AnalysisError


def test_dev_sign_up_and_login(tmp_path):
    provider = DevAuthProvider(users_path=tmp_path / "users.json")
    user = provider.sign_up(
        type("Req", (), {"email": "founder@example.com", "password": "password123", "display_name": "Founder"})()
    )
    assert user.user_id
    assert user.email == "founder@example.com"

    logged_in = provider.login(
        type("Creds", (), {"email": "founder@example.com", "password": "password123"})()
    )
    assert logged_in.user_id == user.user_id


def test_dev_login_rejects_bad_password(tmp_path):
    provider = DevAuthProvider(users_path=tmp_path / "users.json")
    provider.sign_up(
        type("Req", (), {"email": "founder@example.com", "password": "password123", "display_name": None})()
    )
    with pytest.raises(AnalysisError):
        provider.login(
            type("Creds", (), {"email": "founder@example.com", "password": "wrong-password"})()
        )
