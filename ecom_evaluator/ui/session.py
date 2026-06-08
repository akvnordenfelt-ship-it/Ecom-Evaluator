"""Streamlit session state and input validation."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from ecom_evaluator.rate_limit import (
    RateLimitState,
    check_rate_limit,
    load_rate_limit_config,
    rate_limit_enabled,
    rate_limit_status_message,
    record_analysis,
    remaining_analyses,
)
from ecom_evaluator.settings import has_shared_api_key, resolve_api_key, uses_shared_api_key
from ecom_evaluator.ui.subscription import init_subscription_state, show_paywall


def init_session_state() -> None:
    defaults = {
        "analysis_result": None,
        "analysis_meta": None,
        "analysis_running": False,
        "analysis_error": None,
        "market_research": None,
        "rate_limit_count": 0,
        "rate_limit_last_at": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    init_subscription_state()


def get_rate_limit_state() -> RateLimitState:
    last_raw = st.session_state.get("rate_limit_last_at")
    last_run_at = None
    if last_raw:
        last_run_at = datetime.fromisoformat(last_raw)
        if last_run_at.tzinfo is None:
            last_run_at = last_run_at.replace(tzinfo=timezone.utc)
    return RateLimitState(
        count=int(st.session_state.get("rate_limit_count", 0)),
        last_run_at=last_run_at,
    )


def save_rate_limit_state(state: RateLimitState) -> None:
    st.session_state["rate_limit_count"] = state.count
    st.session_state["rate_limit_last_at"] = (
        state.last_run_at.isoformat() if state.last_run_at else None
    )


def shared_rate_limit_applies(data: dict) -> bool:
    return rate_limit_enabled() and uses_shared_api_key(data["api_key"])


def validate_rate_limit(data: dict) -> str | None:
    if not shared_rate_limit_applies(data):
        return None
    return check_rate_limit(get_rate_limit_state(), load_rate_limit_config())


def mark_analysis_for_rate_limit(data: dict) -> None:
    if not shared_rate_limit_applies(data):
        return
    state = get_rate_limit_state()
    record_analysis(state)
    save_rate_limit_state(state)


def rate_limit_banner_text(data: dict) -> str | None:
    if not shared_rate_limit_applies(data):
        return None
    config = load_rate_limit_config()
    state = get_rate_limit_state()
    return rate_limit_status_message(state, config)


def has_remaining_quota(data: dict) -> bool:
    if not shared_rate_limit_applies(data):
        return True
    state = get_rate_limit_state()
    return remaining_analyses(state, load_rate_limit_config()) > 0


def validate_inputs(data: dict) -> list[str]:
    errors: list[str] = []
    if not resolve_api_key(data["api_key"]):
        errors.append(
            "No API key is configured on the server. Ask the site owner to set "
            "`GEMINI_API_KEY` (or `GOOGLE_AI_API_KEY`), or paste your own key in Settings (top right)."
        )
    if not data["product_name"].strip():
        errors.append("Enter a product name.")
    if data["purchase_price"] <= 0:
        errors.append("Purchase price must be greater than 0.")

    limit_error = validate_rate_limit(data)
    if limit_error:
        errors.append(limit_error)

    if show_paywall():
        errors.append(
            "Your free evaluation has been used. Upgrade to Premium for unlimited scans."
        )

    return errors


def set_analysis_error(message: str) -> None:
    st.session_state["analysis_error"] = message


def clear_analysis_error() -> None:
    st.session_state["analysis_error"] = None


def render_analysis_error() -> None:
    message = st.session_state.get("analysis_error")
    if not message:
        return
    st.error(message)
    if st.button("Dismiss error", key="dismiss_analysis_error"):
        clear_analysis_error()
        st.rerun()


def friendly_analysis_error(message: str) -> str:
    lower = message.lower()
    if "api key" in lower or "401" in message or "403" in message:
        return (
            f"{message}\n\n"
            "**Tip:** The hosted API key may be missing or invalid. "
            "Contact the site owner or add your own key in Settings."
        )
    if "incomplete report" in lower or "did not generate enough detail" in lower:
        return (
            f"{message}\n\n"
            "**Tip:** The AI returned a partial response. Click **Run analysis** again — "
            "the app auto-retries up to 3 times. Uploading a product image often improves results."
        )
    if "503" in message or "high demand" in lower or "overloaded" in lower:
        return (
            f"{message}\n\n"
            "**Tip:** The AI provider may be overloaded. Wait a minute and try again — "
            "the app will auto-retry up to 3 times."
        )
    if "429" in message or "quota" in lower or "rate limit" in lower:
        return (
            f"{message}\n\n"
            "**Tip:** The free API quota may be exhausted for now. "
            "Try again later or use your own key in Settings."
        )
    if "schema" in lower or "empty response" in lower or "invalid json" in lower:
        return f"{message}\n\n**Tip:** Run the analysis again — occasional model glitches happen."
    return message


def api_ready_label() -> tuple[str, str]:
    """Return (status label, css class suffix) for the header badge."""
    if has_shared_api_key():
        return "Hosted API ready", "done"
    return "Add API key", "pending"
