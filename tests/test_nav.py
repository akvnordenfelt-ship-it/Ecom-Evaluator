"""Tests for in-app navigation state handling."""

import streamlit as st

from ecom_evaluator.ui.navbar import _nav_action_link, _nav_anchor_link, apply_nav_state
from ecom_evaluator.ui.subscription import APP_VIEW_AUTH, APP_VIEW_LANDING, APP_VIEW_LIVE_CATALOG, APP_VIEW_TOOL


def test_nav_action_link_avoids_query_href():
    link = _nav_action_link(action="tool", class_name="site-header__cta", text="Run evaluation")
    assert 'href="#"' in link
    assert 'data-ps-nav-action="tool"' in link
    assert "?nav_action=" not in link


def test_nav_anchor_link_avoids_query_href():
    link = _nav_anchor_link(anchor="pricing", class_name="site-header__link", text="Pricing")
    assert 'href="#"' in link
    assert 'data-ps-nav-anchor="pricing"' in link
    assert "?nav_anchor=" not in link


def test_apply_nav_state_tool(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(action="tool") is True
    assert state["app_view"] == APP_VIEW_TOOL
    assert state.get("tool_focus_inputs") is True


def test_apply_nav_state_evaluate_guest(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    monkeypatch.setattr(
        "ecom_evaluator.ui.navbar.auth_is_required",
        lambda: True,
    )
    monkeypatch.setattr(
        "ecom_evaluator.ui.navbar.is_authenticated",
        lambda: False,
    )
    assert apply_nav_state(action="evaluate") is True
    assert state["app_view"] == APP_VIEW_AUTH
    assert state["auth_mode"] == "signup"
    assert state["auth_intent"] == "evaluate"


def test_apply_nav_state_login(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(action="login") is True
    assert state["app_view"] == APP_VIEW_AUTH
    assert state["auth_mode"] == "login"


def test_apply_nav_state_anchor(monkeypatch):
    state = {"app_view": APP_VIEW_TOOL}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(anchor="pricing") is True
    assert state["app_view"] == APP_VIEW_LANDING
    assert state["landing_anchor"] == "pricing"


def test_build_site_header_includes_mobile_menu():
    from ecom_evaluator.ui.navbar import _build_site_header_html, _guest_actions_html

    html_out = _build_site_header_html(actions_html=_guest_actions_html(), logged_in=False)
    assert "site-header__nav--desktop" in html_out
    assert "How it works" in html_out
    assert "Report preview" in html_out
    assert "Reviews" in html_out
    assert "Start Free Evaluation" in html_out
    assert "site-header__menu-btn" in html_out


def test_apply_nav_state_live_catalog(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(action="live_catalog") is True
    assert state["app_view"] == APP_VIEW_LIVE_CATALOG


def test_apply_nav_state_unknown_action(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(action="unknown") is False
