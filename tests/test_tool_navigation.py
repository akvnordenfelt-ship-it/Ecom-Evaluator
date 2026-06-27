"""Tests for evaluation tool navigation focus."""

import streamlit as st

from ecom_evaluator.ui.subscription import (
    APP_VIEW_AUTH,
    APP_VIEW_TOOL,
    complete_post_auth_navigation,
    enter_tool_view,
    request_free_evaluation,
)


def test_enter_tool_view_focus_inputs(monkeypatch):
    state: dict = {}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    enter_tool_view(focus_inputs=True)
    assert state["app_view"] == APP_VIEW_TOOL
    assert state["tool_focus_inputs"] is True


def test_complete_post_auth_navigation_evaluate_intent(monkeypatch):
    state = {"auth_intent": "evaluate", "app_view": APP_VIEW_AUTH}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    complete_post_auth_navigation()
    assert state["app_view"] == APP_VIEW_TOOL
    assert state.get("tool_focus_inputs") is True
    assert "auth_intent" not in state


def test_request_free_evaluation_opens_auth_for_guest(monkeypatch):
    state: dict = {}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    monkeypatch.setattr(
        "ecom_evaluator.auth.session.auth_is_required",
        lambda: True,
    )
    monkeypatch.setattr(
        "ecom_evaluator.auth.session.is_authenticated",
        lambda: False,
    )
    reruns: list[None] = []

    def _rerun() -> None:
        reruns.append(None)

    monkeypatch.setattr(st, "rerun", _rerun)
    request_free_evaluation()
    assert state["app_view"] == APP_VIEW_AUTH
    assert state["auth_intent"] == "evaluate"
    assert len(reruns) == 1
