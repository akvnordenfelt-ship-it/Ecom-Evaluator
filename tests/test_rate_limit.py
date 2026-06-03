"""Tests for session rate limiting (no Streamlit runtime)."""

from datetime import datetime, timezone

from ecom_evaluator.rate_limit import (
    RateLimitConfig,
    RateLimitState,
    check_rate_limit,
    record_analysis,
    remaining_analyses,
    rate_limit_status_message,
)


def test_check_rate_limit_allows_first_run():
    state = RateLimitState()
    assert check_rate_limit(state, RateLimitConfig(max_per_session=3, cooldown_seconds=45)) is None


def test_check_rate_limit_blocks_after_max():
    state = RateLimitState(count=3)
    err = check_rate_limit(state, RateLimitConfig(max_per_session=3, cooldown_seconds=45))
    assert err is not None
    assert "3" in err


def test_check_rate_limit_enforces_cooldown():
    now = datetime(2026, 6, 2, 12, 0, 0, tzinfo=timezone.utc)
    state = RateLimitState(count=1, last_run_at=now)
    err = check_rate_limit(
        state,
        RateLimitConfig(max_per_session=3, cooldown_seconds=45),
        now=now.replace(second=10),
    )
    assert err is not None
    assert "wait" in err.lower()


def test_record_analysis_increments_count():
    state = RateLimitState()
    now = datetime(2026, 6, 2, 12, 0, 0, tzinfo=timezone.utc)
    record_analysis(state, now=now)
    assert state.count == 1
    assert state.last_run_at == now


def test_remaining_analyses():
    state = RateLimitState(count=2)
    assert remaining_analyses(state, RateLimitConfig(max_per_session=3)) == 1


def test_rate_limit_status_message():
    state = RateLimitState(count=1)
    msg = rate_limit_status_message(state, RateLimitConfig(max_per_session=3))
    assert "2 of 3" in msg
