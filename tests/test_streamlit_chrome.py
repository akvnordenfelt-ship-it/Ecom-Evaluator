"""Tests for Streamlit branding hide helpers."""

from ecom_evaluator.ui.streamlit_chrome import STREAMLIT_BRANDING_HIDE_CSS


def test_branding_hide_css_targets_streamlit_chrome():
    css = STREAMLIT_BRANDING_HIDE_CSS
    assert "stAppDeployButton" in css
    assert "stToolbar" in css
    assert "footer" in css
    assert "Hosted" not in css  # text matching is in JS, not CSS
