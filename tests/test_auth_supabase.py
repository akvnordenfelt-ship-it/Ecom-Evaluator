"""Tests for Supabase user mapping helpers."""

from types import SimpleNamespace

import pytest

from ecom_evaluator.auth.providers.supabase_provider import user_from_supabase_record
from ecom_evaluator.exceptions import AnalysisError


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
