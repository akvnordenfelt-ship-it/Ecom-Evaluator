"""SaaS subscription state (simulated until Stripe is wired)."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.config import DEFAULT_FREE_EVALUATIONS, PAID_TIERS_ENABLED, STRIPE_PREMIUM_CHECKOUT_URL, STRIPE_PRO_CHECKOUT_URL
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier, get_plan_config

APP_VIEW_LANDING = "landing"
APP_VIEW_TOOL = "tool"


def get_subscription_tier() -> PlanTier:
    if not PAID_TIERS_ENABLED:
        return PlanTier.FREE
    raw = st.session_state.get("subscription_tier", PlanTier.FREE.value)
    try:
        return PlanTier(raw)
    except ValueError:
        return PlanTier.FREE


def can_run_evaluation(*, evaluations_left: int, tier: PlanTier | None = None) -> bool:
    return evaluations_left > 0


def consume_evaluation(*, evaluations_left: int, tier: PlanTier | None = None) -> int:
    return max(0, evaluations_left - 1)


def init_subscription_state() -> None:
    defaults = {
        "app_view": APP_VIEW_LANDING,
        "subscription_tier": PlanTier.FREE.value,
        "evaluations_left": DEFAULT_FREE_EVALUATIONS,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("is_premium"):
        st.session_state["subscription_tier"] = PlanTier.PREMIUM.value
        st.session_state["evaluations_left"] = PLAN_CONFIG[PlanTier.PREMIUM].monthly_evaluations
        del st.session_state["is_premium"]

    if st.session_state.get("analysis_result") is not None:
        st.session_state["app_view"] = APP_VIEW_TOOL


def enter_tool_view() -> None:
    st.session_state["app_view"] = APP_VIEW_TOOL


def is_tool_view() -> bool:
    return st.session_state.get("app_view") == APP_VIEW_TOOL


def user_can_run() -> bool:
    return can_run_evaluation(
        evaluations_left=int(st.session_state.get("evaluations_left", 0)),
        tier=get_subscription_tier(),
    )


def show_paywall() -> bool:
    return not user_can_run()


def mark_evaluation_consumed() -> None:
    st.session_state["evaluations_left"] = consume_evaluation(
        evaluations_left=int(st.session_state.get("evaluations_left", 0)),
        tier=get_subscription_tier(),
    )


def activate_plan(tier: PlanTier) -> None:
    plan = get_plan_config(tier)
    st.session_state["subscription_tier"] = tier.value
    st.session_state["evaluations_left"] = plan.monthly_evaluations


def evaluations_status_label() -> str:
    tier = get_subscription_tier()
    plan = get_plan_config(tier)
    left = int(st.session_state.get("evaluations_left", 0))

    if tier == PlanTier.FREE:
        if left == 1:
            return "Free · 1 evaluation left"
        if left > 1:
            return f"Free · {left} evaluations left"
        return "Free trial used"

    return f"{plan.label} · {left}/{plan.monthly_evaluations} evaluations left"


def stripe_checkout_url(tier: PlanTier = PlanTier.PREMIUM) -> str:
    if tier == PlanTier.PRO and STRIPE_PRO_CHECKOUT_URL:
        return STRIPE_PRO_CHECKOUT_URL
    return STRIPE_PREMIUM_CHECKOUT_URL or "https://stripe.com"
