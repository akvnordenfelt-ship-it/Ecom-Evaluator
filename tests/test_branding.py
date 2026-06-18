"""Tests for Crow Metrics branding assets."""

from ecom_evaluator.ui.branding import (
    BRAND_NAME,
    header_brand_html,
    logo_data_uri,
    logo_path,
    wordmark_html,
)


def test_brand_assets_exist():
    assert logo_path() is not None
    assert logo_path().is_file()
    uri = logo_data_uri()
    assert uri.startswith("data:image/png;base64,")


def test_wordmark_html_structure():
    html = wordmark_html(size="md", with_logo=True)
    assert "crow-wordmark__crow" in html
    assert "CROW" in html
    assert "crow-wordmark__metrics" in html
    assert "METRICS" in html


def test_header_brand_html_includes_logo_and_wordmark():
    html = header_brand_html()
    assert "site-header__mark" in html
    assert "crow-wordmark" in html
    assert "CROW" in html
    assert "METRICS" in html
