"""Tests for per-account evaluation quotas."""

import pytest

from ecom_evaluator.auth.quota import FileQuotaStore, evaluations_remaining
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT


@pytest.fixture
def quota_store(tmp_path):
    return FileQuotaStore(path=tmp_path / "quota.json")


def test_new_user_has_full_quota(quota_store):
    assert quota_store.get_used_count("user-1") == 0
    assert evaluations_remaining(user_id="user-1", used_count=0) == FREE_EVALUATIONS_PER_ACCOUNT


def test_increment_tracks_used_evaluations(quota_store):
    assert quota_store.increment_used("user-1") == 1
    assert quota_store.increment_used("user-1") == 2
    assert evaluations_remaining(user_id="user-1", used_count=2) == 0


def test_quota_isolated_per_user(quota_store):
    quota_store.increment_used("user-a")
    assert quota_store.get_used_count("user-a") == 1
    assert quota_store.get_used_count("user-b") == 0
