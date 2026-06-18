"""Tests for London-time live market evaluation counter."""

from datetime import datetime

from ecom_evaluator.ui.live_market_stats import (
    LONDON_TZ,
    MAX_DAILY_EVALUATIONS,
    MIN_DAILY_EVALUATIONS,
    daily_evaluation_target,
    evaluated_today_count,
    evaluated_today_ticker,
    format_count,
)


def test_daily_evaluation_target_is_deterministic_per_day():
    day = datetime(2026, 6, 2, 12, 0, tzinfo=LONDON_TZ)
    assert daily_evaluation_target(now=day) == daily_evaluation_target(
        now=datetime(2026, 6, 2, 23, 59, tzinfo=LONDON_TZ)
    )


def test_daily_evaluation_target_within_range():
    day = datetime(2026, 1, 15, 8, 30, tzinfo=LONDON_TZ)
    target = daily_evaluation_target(now=day)
    assert MIN_DAILY_EVALUATIONS <= target <= MAX_DAILY_EVALUATIONS


def test_evaluated_today_count_resets_at_london_midnight():
    midnight = datetime(2026, 6, 2, 0, 0, tzinfo=LONDON_TZ)
    assert evaluated_today_count(now=midnight) == 0


def test_evaluated_today_count_near_target_late_in_day():
    end = datetime(2026, 6, 2, 23, 59, 59, tzinfo=LONDON_TZ)
    target = daily_evaluation_target(now=end)
    count = evaluated_today_count(now=end)
    assert count >= target - 2
    assert count <= target


def test_evaluated_today_count_increases_through_day():
    morning = datetime(2026, 6, 2, 8, 0, tzinfo=LONDON_TZ)
    evening = datetime(2026, 6, 2, 20, 0, tzinfo=LONDON_TZ)
    assert evaluated_today_count(now=morning) < evaluated_today_count(now=evening)


def test_evaluated_today_ticker_includes_client_fields():
    moment = datetime(2026, 6, 2, 15, 0, tzinfo=LONDON_TZ)
    ticker = evaluated_today_ticker(now=moment)
    assert ticker["count"] == evaluated_today_count(now=moment)
    assert ticker["target"] == daily_evaluation_target(now=moment)
    assert ticker["day_start_ms"] > 0


def test_format_count():
    assert format_count(8421) == "8,421"
