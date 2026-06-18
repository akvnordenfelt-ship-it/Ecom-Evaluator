"""Crow Metrics brand assets and HTML helpers."""

from __future__ import annotations

import base64
import html
from functools import lru_cache
from pathlib import Path

BRAND_NAME = "Crow Metrics"
BRAND_NAME_UPPER = "CROW METRICS"
BRAND_TAGLINE = "E-commerce evaluator & go-to-market planner"
BRAND_BLUE = "#2B59FF"
BRAND_BLUE_DEEP = "#1E3A8A"

STATIC_BRAND_DIR = Path(__file__).resolve().parent.parent / "static" / "brand"
LOGO_PATH = STATIC_BRAND_DIR / "crow-logo.png"
WORDMARK_PATH = STATIC_BRAND_DIR / "crow-wordmark.png"


def brand_page_title(suffix: str = "E-commerce Evaluator") -> str:
    return f"{BRAND_NAME} — {suffix}"


@lru_cache(maxsize=2)
def _file_data_uri(path: Path) -> str:
    if not path.is_file():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def logo_data_uri() -> str:
    return _file_data_uri(LOGO_PATH)


def wordmark_image_data_uri() -> str:
    return _file_data_uri(WORDMARK_PATH)


def logo_path() -> Path | None:
    return LOGO_PATH if LOGO_PATH.is_file() else None


def wordmark_html(*, size: str = "md", with_logo: bool = False) -> str:
    """HTML wordmark: bold CROW + light METRICS."""
    size_class = f"crow-wordmark--{size}"
    logo_html = ""
    if with_logo:
        uri = html.escape(logo_data_uri(), quote=True)
        if uri:
            logo_html = (
                f'<img class="crow-wordmark__logo" src="{uri}" alt="" aria-hidden="true" />'
            )
    return (
        f'<span class="crow-wordmark {size_class}">'
        f"{logo_html}"
        '<span class="crow-wordmark__text" aria-label="Crow Metrics">'
        '<span class="crow-wordmark__crow">CROW</span>'
        '<span class="crow-wordmark__metrics">METRICS</span>'
        "</span>"
        "</span>"
    )


def header_brand_html() -> str:
    """Navbar / compact brand lockup with icon + wordmark."""
    uri = html.escape(logo_data_uri(), quote=True)
    logo = (
        f'<img class="site-header__mark" src="{uri}" alt="" aria-hidden="true" />'
        if uri
        else ""
    )
    return logo + wordmark_html(size="sm")


def auth_brand_html() -> str:
    uri = html.escape(logo_data_uri(), quote=True)
    if uri:
        return f'<img class="auth-brand-mark__logo" src="{uri}" alt="Crow Metrics" />'
    return wordmark_html(size="lg", with_logo=False)
