"""Tests for Streamlit branding hide helpers."""

from ecom_evaluator.ui.streamlit_chrome import STREAMLIT_BRANDING_HIDE_CSS


def test_branding_hide_css_targets_streamlit_chrome():
    css = STREAMLIT_BRANDING_HIDE_CSS
    assert "stAppDeployButton" in css
    assert "stToolbar" in css
    assert "footer" in css
    assert "viewerBadge_container__67w8K" in css
    assert '[class*="viewerBadge"]' in css
    assert "site-header" in css


def test_branding_css_does_not_hide_app_navbar():
    css = STREAMLIT_BRANDING_HIDE_CSS
    assert "header.site-header" in css
    assert 'header {visibility: hidden' not in css.replace(" ", "")
