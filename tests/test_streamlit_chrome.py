"""Tests for Streamlit branding hide helpers."""

from ecom_evaluator.ui.streamlit_chrome import (
    APP_STREAMLIT_HIDE_CSS,
    CLOUD_BADGE_HIDE_CSS,
    STREAMLIT_BRANDING_HIDE_CSS,
)


def test_app_hide_css_targets_in_app_chrome():
    css = APP_STREAMLIT_HIDE_CSS
    assert "stAppDeployButton" in css
    assert "stToolbar" in css
    assert "stDecoration" in css
    assert "viewerBadge" not in css


def test_cloud_badge_css_is_narrow():
    css = CLOUD_BADGE_HIDE_CSS
    assert "viewerBadge" in css
    assert "footer" not in css
    assert "stHeader" not in css


def test_combined_css_available():
    assert APP_STREAMLIT_HIDE_CSS in STREAMLIT_BRANDING_HIDE_CSS
    assert CLOUD_BADGE_HIDE_CSS in STREAMLIT_BRANDING_HIDE_CSS


def test_app_css_does_not_hide_app_navbar():
    css = APP_STREAMLIT_HIDE_CSS
    assert 'header[data-testid="stHeader"]' in css
    assert "header.site-header" not in css
    assert "header {" not in css.replace('header[data-testid="stHeader"]', "")
