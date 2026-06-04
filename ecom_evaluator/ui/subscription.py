"""SaaS subscription state (simulated until Stripe is wired)."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.config import DEFAULT_FREE_EVALUATIONS, STRIPE_CHECKOUT_URL

APP_VIEW_LANDING = "landing"
APP_VIEW_TOOL = "tool"


def can_run_evaluation(*, evaluations_left: int, is_premium: bool) -> bool:
    return is_premium or evaluations_left > 0


def consume_evaluation(*, evaluations_left: int, is_premium: bool) -> int:
    if is_premium:
        return evaluations_left
    return max(0, evaluations_left - 1)


def init_subscription_state() -> None:
    defaults = {
        "app_view": APP_VIEW_LANDING,
        "evaluations_left": DEFAULT_FREE_EVALUATIONS,
        "is_premium": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("analysis_result") is not None:
        st.session_state["app_view"] = APP_VIEW_TOOL


def enter_tool_view() -> None:
    st.session_state["app_view"] = APP_VIEW_TOOL


def is_tool_view() -> bool:
    return st.session_state.get("app_view") == APP_VIEW_TOOL


def user_can_run() -> bool:
    return can_run_evaluation(
        evaluations_left=int(st.session_state.get("evaluations_left", 0)),
        is_premium=bool(st.session_state.get("is_premium", False)),
    )


def show_paywall() -> bool:
    return not user_can_run()


def mark_evaluation_consumed() -> None:
    st.session_state["evaluations_left"] = consume_evaluation(
        evaluations_left=int(st.session_state.get("evaluations_left", 0)),
        is_premium=bool(st.session_state.get("is_premium", False)),
    )


def evaluations_status_label() -> str:
    if st.session_state.get("is_premium"):
        return "Premium — unlimited"
    left = int(st.session_state.get("evaluations_left", 0))
    if left == 1:
        return "1 free evaluation left"
    if left > 1:
        return f"{left} free evaluations left"
    return "Free trial used"


def stripe_checkout_url() -> str:
    return STRIPE_CHECKOUT_URL or "https://stripe.com"
