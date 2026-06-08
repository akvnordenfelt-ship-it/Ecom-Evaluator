"""Session rate limits for shared-key (hosted) deployments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone

from ecom_evaluator.config import ANALYSIS_COOLDOWN_SECONDS, MAX_ANALYSES_PER_SESSION


@dataclass
class RateLimitConfig:
    max_per_session: int = MAX_ANALYSES_PER_SESSION
    cooldown_seconds: int = ANALYSIS_COOLDOWN_SECONDS


@dataclass
class RateLimitState:
    count: int = 0
    last_run_at: datetime | None = None


def load_rate_limit_config() -> RateLimitConfig:
    max_per = os.getenv("MAX_ANALYSES_PER_SESSION")
    cooldown = os.getenv("ANALYSIS_COOLDOWN_SECONDS")
    return RateLimitConfig(
        max_per_session=int(max_per) if max_per else MAX_ANALYSES_PER_SESSION,
        cooldown_seconds=int(cooldown) if cooldown else ANALYSIS_COOLDOWN_SECONDS,
    )


def rate_limit_enabled() -> bool:
    explicit = os.getenv("RATE_LIMIT_ENABLED", "").strip().lower()
    if explicit in {"0", "false", "no", "off"}:
        return False
    if explicit in {"1", "true", "yes", "on"}:
        return True
    return True


def check_rate_limit(
    state: RateLimitState,
    config: RateLimitConfig | None = None,
    *,
    now: datetime | None = None,
) -> str | None:
    """Return a user-facing error if blocked, otherwise None."""
    config = config or load_rate_limit_config()
    now = now or datetime.now(timezone.utc)

    if state.count >= config.max_per_session:
        return (
            f"You've used all {config.max_per_session} free evaluations for this browser session. "
            "Open the app in a new tab later, or come back tomorrow."
        )

    if state.last_run_at is not None:
        elapsed = (now - state.last_run_at).total_seconds()
        if elapsed < config.cooldown_seconds:
            wait = int(config.cooldown_seconds - elapsed) + 1
            return f"Please wait {wait} seconds before running another evaluation."

    return None


def record_analysis(state: RateLimitState, *, now: datetime | None = None) -> None:
    now = now or datetime.now(timezone.utc)
    state.count += 1
    state.last_run_at = now


def remaining_analyses(state: RateLimitState, config: RateLimitConfig | None = None) -> int:
    config = config or load_rate_limit_config()
    return max(0, config.max_per_session - state.count)


def rate_limit_status_message(state: RateLimitState, config: RateLimitConfig | None = None) -> str:
    config = config or load_rate_limit_config()
    remaining = remaining_analyses(state, config)
    if config.max_per_session <= 1:
        return "1 free evaluation left" if remaining >= 1 else "Free evaluation used this session"
    return f"{remaining} of {config.max_per_session} free evaluations left this session"
