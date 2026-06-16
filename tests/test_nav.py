"""Tests for in-app navigation state handling."""

import streamlit as st

from ecom_evaluator.ui.navbar import _nav_action_link, _nav_anchor_link, apply_nav_state
from ecom_evaluator.ui.subscription import APP_VIEW_AUTH, APP_VIEW_LANDING, APP_VIEW_TOOL


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


def test_apply_nav_state_unknown_action(monkeypatch):
    state = {"app_view": APP_VIEW_LANDING}
    monkeypatch.setattr(st, "session_state", state, raising=False)
    assert apply_nav_state(action="unknown") is False
