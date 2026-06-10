"""Streamlit session integration for authenticated users."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.auth.models import AuthCredentials, AuthLoginResult, AuthUser, SignUpRequest
from ecom_evaluator.auth.providers.base import get_auth_provider, get_auth_settings
from ecom_evaluator.auth.quota import evaluations_remaining, get_quota_store
from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.plans import get_plan_config, plan_has_unlimited_evaluations


def init_auth_state() -> None:
    defaults = {
        "auth_user": None,
        "auth_error": None,
        "auth_access_token": None,
        "auth_refresh_token": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def auth_is_required() -> bool:
    return get_auth_settings().auth_required


def is_authenticated() -> bool:
    if not auth_is_required():
        return True
    return st.session_state.get("auth_user") is not None


def get_current_user() -> AuthUser | None:
    user = st.session_state.get("auth_user")
    return user if isinstance(user, AuthUser) else None


def require_authenticated_user() -> AuthUser:
    user = get_current_user()
    if user is None:
        raise AnalysisError("You must be logged in to continue.")
    return user


def set_auth_user(
    user: AuthUser,
    *,
    access_token: str | None = None,
    refresh_token: str | None = None,
) -> None:
    st.session_state["auth_user"] = user
    st.session_state["auth_error"] = None
    st.session_state["auth_access_token"] = access_token
    st.session_state["auth_refresh_token"] = refresh_token
    sync_user_evaluation_quota()


def clear_auth_error() -> None:
    st.session_state["auth_error"] = None


def set_auth_error(message: str) -> None:
    st.session_state["auth_error"] = message


def render_auth_error() -> None:
    message = st.session_state.get("auth_error")
    if message:
        st.error(message)


def login_with_credentials(*, email: str, password: str) -> None:
    provider = get_auth_provider()
    result = provider.login(AuthCredentials(email=email, password=password))
    set_auth_user(
        result.user,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
    )


def sign_up_account(*, email: str, password: str, display_name: str | None = None) -> None:
    provider = get_auth_provider()
    user = provider.sign_up(SignUpRequest(email=email, password=password, display_name=display_name))
    set_auth_user(user)


def logout_user() -> None:
    st.session_state["auth_user"] = None
    st.session_state["auth_error"] = None
    st.session_state["auth_access_token"] = None
    st.session_state["auth_refresh_token"] = None
    st.session_state["auth_browser_clear"] = True
    st.session_state["analysis_result"] = None
    st.session_state["analysis_meta"] = None
    st.session_state["app_view"] = "landing"


def sync_user_evaluation_quota() -> None:
    """Load per-account free evaluation balance into session state."""
    from ecom_evaluator.ui.subscription import get_subscription_tier

    tier = get_subscription_tier()
    plan = get_plan_config(tier)
    if plan_has_unlimited_evaluations(tier):
        st.session_state["evaluations_left"] = plan.monthly_evaluations
        return

    user = get_current_user()
    if user is None:
        st.session_state["evaluations_left"] = FREE_EVALUATIONS_PER_ACCOUNT
        return

    used = get_quota_store().get_used_count(user.user_id)
    st.session_state["evaluations_left"] = evaluations_remaining(user_id=user.user_id, used_count=used)


def persist_evaluation_consumed() -> None:
    """Increment durable quota for the logged-in account."""
    from ecom_evaluator.ui.subscription import get_subscription_tier

    tier = get_subscription_tier()
    if plan_has_unlimited_evaluations(tier):
        return

    user = get_current_user()
    if user is None:
        left = int(st.session_state.get("evaluations_left", 0))
        st.session_state["evaluations_left"] = max(0, left - 1)
        return

    used = get_quota_store().increment_used(user.user_id)
    st.session_state["evaluations_left"] = evaluations_remaining(user_id=user.user_id, used_count=used)


def account_quota_label() -> str | None:
    user = get_current_user()
    if user is None:
        return None
    from ecom_evaluator.ui.subscription import get_subscription_tier

    tier = get_subscription_tier()
    if plan_has_unlimited_evaluations(tier):
        return "Premium · Unlimited evaluations"
    remaining = int(st.session_state.get("evaluations_left", 0))
    if remaining == 1:
        return f"1 of {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations left"
    if remaining > 1:
        return f"{remaining} of {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations left"
    return "Free evaluations used on this account"
