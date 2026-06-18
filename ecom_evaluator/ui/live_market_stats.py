"""Live market headline stats (London-time daily evaluation counter)."""

from __future__ import annotations

import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

LONDON_TZ = ZoneInfo("Europe/London")
MIN_DAILY_EVALUATIONS = 5_000
MAX_DAILY_EVALUATIONS = 15_000


def daily_evaluation_target(*, now: datetime | None = None) -> int:
    """Deterministic daily cap between 5,000 and 15,000 (inclusive)."""
    moment = now or datetime.now(LONDON_TZ)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=LONDON_TZ)
    else:
        moment = moment.astimezone(LONDON_TZ)

    seed = int(hashlib.md5(moment.strftime("%Y-%m-%d").encode()).hexdigest()[:8], 16)
    span = MAX_DAILY_EVALUATIONS - MIN_DAILY_EVALUATIONS + 1
    return MIN_DAILY_EVALUATIONS + (seed % span)


def evaluated_today_count(*, now: datetime | None = None) -> int:
    """Count that resets at 00:00 London and rises smoothly through the day."""
    moment = now or datetime.now(LONDON_TZ)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=LONDON_TZ)
    else:
        moment = moment.astimezone(LONDON_TZ)

    day_start = moment.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_into_day = (moment - day_start).total_seconds()
    fraction = min(1.0, max(0.0, seconds_into_day / 86_400.0))
    target = daily_evaluation_target(now=moment)
    progress = fraction**0.88
    return int(target * progress)


def format_count(value: int) -> str:
    return f"{value:,}"


def evaluated_today_ticker(*, now: datetime | None = None) -> dict[str, int]:
    """Server-rendered count plus client ticker inputs (London midnight epoch ms)."""
    moment = now or datetime.now(LONDON_TZ)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=LONDON_TZ)
    else:
        moment = moment.astimezone(LONDON_TZ)

    day_start = moment.replace(hour=0, minute=0, second=0, microsecond=0)
    return {
        "count": evaluated_today_count(now=moment),
        "target": daily_evaluation_target(now=moment),
        "day_start_ms": int(day_start.timestamp() * 1000),
    }
