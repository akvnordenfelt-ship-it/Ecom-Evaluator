"""SaaS subscription state (simulated until Stripe is wired)."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.auth.session import init_auth_state, persist_evaluation_consumed, sync_user_evaluation_quota
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT, PAID_TIERS_ENABLED, STRIPE_PREMIUM_CHECKOUT_URL
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier, coerce_plan_tier, get_plan_config, plan_has_unlimited_evaluations

APP_VIEW_LANDING = "landing"
APP_VIEW_AUTH = "auth"
APP_VIEW_TOOL = "tool"
APP_VIEW_LIVE_CATALOG = "live_catalog"


def get_subscription_tier() -> PlanTier:
    if not PAID_TIERS_ENABLED:
        return PlanTier.FREE
    raw = st.session_state.get("subscription_tier", PlanTier.FREE.value)
    try:
        return coerce_plan_tier(raw)
    except ValueError:
        return PlanTier.FREE


def can_run_evaluation(*, evaluations_left: int, tier: PlanTier | None = None) -> bool:
    tier = tier or PlanTier.FREE
    if plan_has_unlimited_evaluations(tier):
        return True
    return evaluations_left > 0


def consume_evaluation(*, evaluations_left: int, tier: PlanTier | None = None) -> int:
    tier = tier or PlanTier.FREE
    if plan_has_unlimited_evaluations(tier):
        return evaluations_left
    return max(0, evaluations_left - 1)


def init_subscription_state() -> None:
    defaults = {
        "app_view": APP_VIEW_LANDING,
        "subscription_tier": PlanTier.FREE.value,
        "evaluations_left": FREE_EVALUATIONS_PER_ACCOUNT,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("subscription_tier") == "pro":
        st.session_state["subscription_tier"] = PlanTier.PREMIUM.value

    if st.session_state.get("is_premium"):
        st.session_state["subscription_tier"] = PlanTier.PREMIUM.value
        st.session_state["evaluations_left"] = PLAN_CONFIG[PlanTier.PREMIUM].monthly_evaluations
        del st.session_state["is_premium"]

    if st.session_state.get("analysis_result") is not None:
        st.session_state["app_view"] = APP_VIEW_TOOL

    sync_user_evaluation_quota()


def enter_tool_view(*, focus_inputs: bool = False) -> None:
    st.session_state["app_view"] = APP_VIEW_TOOL
    if focus_inputs:
        st.session_state["tool_focus_inputs"] = True


def go_to_landing(*, anchor: str | None = None) -> None:
    st.session_state["app_view"] = APP_VIEW_LANDING
    if anchor:
        st.session_state["landing_anchor"] = anchor
    st.rerun()


def open_auth_screen(*, mode: str = "login", intent: str | None = None) -> None:
    st.session_state["app_view"] = APP_VIEW_AUTH
    st.session_state["auth_mode"] = mode
    if intent:
        st.session_state["auth_intent"] = intent
    st.rerun()


def request_free_evaluation() -> None:
    from ecom_evaluator.auth.session import auth_is_required, is_authenticated

    if auth_is_required() and not is_authenticated():
        open_auth_screen(mode="login", intent="evaluate")
        return
    enter_tool_view(focus_inputs=True)
    st.rerun()


def complete_post_auth_navigation() -> None:
    intent = st.session_state.pop("auth_intent", None)
    if intent == "evaluate":
        enter_tool_view(focus_inputs=True)
    else:
        st.session_state["app_view"] = APP_VIEW_LANDING


def is_tool_view() -> bool:
    return st.session_state.get("app_view") == APP_VIEW_TOOL


def user_can_run() -> bool:
    tier = get_subscription_tier()
    return can_run_evaluation(
        evaluations_left=int(st.session_state.get("evaluations_left", 0)),
        tier=tier,
    )


def show_paywall() -> bool:
    return not user_can_run()


def mark_evaluation_consumed() -> None:
    persist_evaluation_consumed()


def activate_plan(tier: PlanTier | str) -> None:
    tier = coerce_plan_tier(tier)
    plan = get_plan_config(tier)
    st.session_state["subscription_tier"] = tier.value
    st.session_state["evaluations_left"] = plan.monthly_evaluations


def evaluations_status_label() -> str:
    from ecom_evaluator.auth.session import account_quota_label, get_current_user

    tier = get_subscription_tier()
    plan = get_plan_config(tier)
    left = int(st.session_state.get("evaluations_left", 0))

    if tier == PlanTier.FREE:
        account_label = account_quota_label()
        if get_current_user() and account_label:
            return account_label
        if left == 1:
            return f"Free · 1 of {FREE_EVALUATIONS_PER_ACCOUNT} evaluations left"
        if left > 1:
            return f"Free · {left} of {FREE_EVALUATIONS_PER_ACCOUNT} evaluations left"
        return "Free evaluations used"

    if plan_has_unlimited_evaluations(tier):
        return f"{plan.label} · Unlimited evaluations"

    return f"{plan.label} · {left} evaluations left"


def stripe_checkout_url(tier: PlanTier = PlanTier.PREMIUM) -> str:
    return STRIPE_PREMIUM_CHECKOUT_URL or "https://stripe.com"
