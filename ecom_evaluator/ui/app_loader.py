"""Branded first-paint shell — hides bridge buttons and shows a loading screen."""

from __future__ import annotations

import html
import json

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.ui.branding import BRAND_TAGLINE, logo_data_uri

HIDDEN_BRIDGE_HOST_CSS = """
div[class*="st-key-ps_nav_"],
div[class*="st-key-ps_sample_"] {
    position: fixed !important;
    left: -10000px !important;
    top: 0 !important;
    width: 1px !important;
    height: 1px !important;
    overflow: hidden !important;
    opacity: 0 !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
"""

APP_LOADER_CSS = """
html:not(.cm-app-ready),
html:not(.cm-app-ready) body {
    background: #0A1128 !important;
}
.cm-app-loader {
    position: fixed;
    inset: 0;
    z-index: 2147483000;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(ellipse 70% 45% at 10% -5%, rgba(43, 89, 255, 0.22) 0%, transparent 55%),
        radial-gradient(ellipse 55% 40% at 95% 0%, rgba(30, 58, 138, 0.18) 0%, transparent 50%),
        linear-gradient(180deg, #060B18 0%, #0A1128 42%, #0F172A 100%);
    transition: opacity 0.4s ease, visibility 0.4s ease;
}
html.cm-app-ready .cm-app-loader {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}
.cm-app-loader__inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.1rem;
    text-align: center;
    padding: 2rem;
    animation: cm-loader-rise 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes cm-loader-rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: none; }
}
.cm-app-loader__logo {
    width: 52px;
    height: 52px;
    object-fit: contain;
    filter: drop-shadow(0 8px 24px rgba(43, 89, 255, 0.35));
}
.cm-app-loader__wordmark {
    display: inline-flex;
    align-items: baseline;
    gap: 0.35rem;
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.14em;
    line-height: 1;
}
.cm-app-loader__crow {
    font-size: 1.05rem;
    font-weight: 800;
    color: #F5F5F7;
}
.cm-app-loader__metrics {
    font-size: 1.05rem;
    font-weight: 300;
    color: #94A3B8;
}
.cm-app-loader__tagline {
    margin: 0;
    max-width: 18rem;
    font-size: 0.82rem;
    line-height: 1.45;
    color: #86868B;
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.cm-app-loader__spinner {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid rgba(147, 197, 253, 0.18);
    border-top-color: #2B59FF;
    animation: cm-loader-spin 0.85s linear infinite;
}
@keyframes cm-loader-spin {
    to { transform: rotate(360deg); }
}
@media (prefers-reduced-motion: reduce) {
    .cm-app-loader__inner { animation: none; }
    .cm-app-loader__spinner { animation: none; opacity: 0.65; }
}
"""

_READY_SELECTORS = (
    ".site-header",
    ".cm-hero-screen",
    ".cm-auth-page",
    ".cm-workspace",
    ".cm-live-catalog",
)

_LOADER_JS = r"""
(function () {
    const win = window.parent;
    const doc = win.document;
    if (!doc || win.__cmAppLoaderInstalled) return;
    win.__cmAppLoaderInstalled = true;

    const STYLE_ID = "cm-app-loader-style";
    const LOADER_ID = "cm-app-loader";
    const READY_SELECTORS = __READY_SELECTORS__;
    const logoSrc = __LOGO_SRC__;

    function injectStyle(css) {
        if (doc.getElementById(STYLE_ID)) return;
        const style = doc.createElement("style");
        style.id = STYLE_ID;
        style.textContent = css;
        (doc.head || doc.documentElement).appendChild(style);
    }

    function loaderMarkup() {
        const logo = logoSrc
            ? '<img class="cm-app-loader__logo" src="' + logoSrc + '" alt="" aria-hidden="true" />'
            : "";
        return (
            '<div class="cm-app-loader__inner" role="status" aria-live="polite" aria-busy="true">' +
            logo +
            '<div class="cm-app-loader__wordmark" aria-label="Crow Metrics">' +
            '<span class="cm-app-loader__crow">CROW</span>' +
            '<span class="cm-app-loader__metrics">METRICS</span>' +
            "</div>" +
            '<p class="cm-app-loader__tagline">__TAGLINE__</p>' +
            '<div class="cm-app-loader__spinner" aria-hidden="true"></div>' +
            "</div>"
        );
    }

    function ensureLoader() {
        injectStyle(__LOADER_CSS__);
        let loader = doc.getElementById(LOADER_ID);
        if (!loader) {
            loader = doc.createElement("div");
            loader.id = LOADER_ID;
            loader.className = "cm-app-loader";
            loader.innerHTML = loaderMarkup();
            doc.body.appendChild(loader);
        }
    }

    function isReady() {
        for (let i = 0; i < READY_SELECTORS.length; i += 1) {
            if (doc.querySelector(READY_SELECTORS[i])) return true;
        }
        return false;
    }

    function markReady() {
        doc.documentElement.classList.add("cm-app-ready");
        const loader = doc.getElementById(LOADER_ID);
        if (!loader) return;
        win.setTimeout(function () {
            loader.remove();
        }, 450);
    }

    function pollReady(attempt) {
        if (isReady()) {
            markReady();
            return;
        }
        if (attempt >= 80) {
            markReady();
            return;
        }
        win.setTimeout(function () {
            pollReady(attempt + 1);
        }, 50);
    }

    ensureLoader();
    if (!doc.documentElement.classList.contains("cm-app-ready")) {
        pollReady(0);
    }
})();
"""


def inject_early_app_shell() -> None:
    """Inject before hidden bridge buttons so they never flash on screen."""
    st.markdown(
        f"<style>{HIDDEN_BRIDGE_HOST_CSS}{APP_LOADER_CSS}</style>",
        unsafe_allow_html=True,
    )


def install_app_loader() -> None:
    """Mount branded loader in the parent document and dismiss when the app is ready."""
    logo_src = html.escape(logo_data_uri(), quote=True)
    tagline = html.escape(BRAND_TAGLINE)
    loader_css = json.dumps(APP_LOADER_CSS)
    ready_selectors = json.dumps(list(_READY_SELECTORS))
    logo_json = json.dumps(logo_src)

    script = (
        _LOADER_JS.replace("__LOADER_CSS__", loader_css)
        .replace("__READY_SELECTORS__", ready_selectors)
        .replace("__LOGO_SRC__", logo_json)
        .replace("__TAGLINE__", tagline)
    )
    components.html(f"<script>{script}</script>", height=0, width=0)
