"""Hide Streamlit platform chrome, deploy button, and branding stamps."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

# In-app Streamlit chrome only. Do NOT use bare `header { }` — hides `.site-header` navbar.
APP_STREAMLIT_HIDE_CSS = """
#MainMenu {
    visibility: hidden !important;
    display: none !important;
}
.stApp > footer,
footer[data-testid="stFooter"] {
    visibility: hidden !important;
    display: none !important;
}
header[data-testid="stHeader"] {
    visibility: hidden !important;
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
}
[data-testid="stDecoration"],
div[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}
[data-testid="stToolbar"],
[data-testid="stAppDeployButton"],
[data-testid="stDeployButton"],
[data-testid="stHeaderActionElements"],
[data-testid="stMainMenu"],
.stAppDeployButton,
.stDeployButton,
button[kind="header"],
#GithubIcon {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
"""

# Streamlit Cloud shell (parent frame) — badge/profile only, never app layout rules.
CLOUD_BADGE_HIDE_CSS = """
[class*="viewerBadge_container"],
[class*="viewerBadge_link"],
[class*="viewerBadge_text"],
[class*="styles_viewerBadge"],
[class*="viewerBadge"],
[class*="StyledManageApp"],
[class*="MadeWithStreamlit"],
.viewerBadge_container__67w8K,
.viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
"""

STREAMLIT_BRANDING_HIDE_CSS = APP_STREAMLIT_HIDE_CSS + CLOUD_BADGE_HIDE_CSS

_BADGE_SELECTORS = [
    '[class*="viewerBadge_container"]',
    '[class*="viewerBadge_link"]',
    '[class*="viewerBadge_text"]',
    '[class*="styles_viewerBadge"]',
    '[class*="viewerBadge"]',
    '[class*="StyledManageApp"]',
    '[class*="MadeWithStreamlit"]',
]

_BRANDING_JS = r"""
(function () {
    const APP_STYLE_ID = "ps-hide-streamlit-app-chrome";
    const CLOUD_STYLE_ID = "ps-hide-streamlit-cloud-badge";

    function injectStyle(doc, css, id) {
        if (!doc || doc.getElementById(id)) return;
        const style = doc.createElement("style");
        style.id = id;
        style.textContent = css;
        (doc.head || doc.documentElement).appendChild(style);
    }

    function hideMatches(doc, selectors) {
        if (!doc) return;
        selectors.forEach(function (sel) {
            try {
                doc.querySelectorAll(sel).forEach(function (el) {
                    el.style.setProperty("display", "none", "important");
                    el.style.setProperty("visibility", "hidden", "important");
                    el.style.setProperty("pointer-events", "none", "important");
                });
            } catch (e) {}
        });
    }

    function parentDocuments() {
        const docs = [];
        let win = window;
        for (let i = 0; i < 6; i += 1) {
            try {
                if (win.document && !docs.includes(win.document)) docs.push(win.document);
                if (!win.parent || win.parent === win) break;
                win = win.parent;
            } catch (e) {
                break;
            }
        }
        return docs;
    }

    window.__psStreamlitChromeSweep = function (appCss, cloudCss, badgeSelectors) {
        injectStyle(document, appCss, APP_STYLE_ID);
        hideMatches(document, badgeSelectors);

        parentDocuments().forEach(function (doc) {
            if (doc === document) return;
            injectStyle(doc, cloudCss, CLOUD_STYLE_ID);
            hideMatches(doc, badgeSelectors);
        });
    };
})();
"""


def configure_streamlit_chrome() -> None:
    """Apply scriptable Streamlit options before the page renders."""
    try:
        st.set_option("client.toolbarMode", "minimal")
    except Exception:
        pass


def inject_streamlit_branding_hide_css() -> None:
    st.markdown(f"<style>{STREAMLIT_BRANDING_HIDE_CSS}</style>", unsafe_allow_html=True)


def install_streamlit_branding_hide_bridge() -> None:
    """Hide in-app chrome + Cloud badge in parent frame without touching app layout."""
    components.html(
        f"""
        <script>
        {_BRANDING_JS}
        (function () {{
            const appCss = {APP_STREAMLIT_HIDE_CSS!r};
            const cloudCss = {CLOUD_BADGE_HIDE_CSS!r};
            const badgeSelectors = {list(_BADGE_SELECTORS)!r};
            function run() {{
                if (window.__psStreamlitChromeSweep) {{
                    window.__psStreamlitChromeSweep(appCss, cloudCss, badgeSelectors);
                }}
            }}
            run();
            let ticks = 0;
            const fast = setInterval(function () {{
                run();
                ticks += 1;
                if (ticks >= 12) clearInterval(fast);
            }}, 500);
            setInterval(run, 3000);
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
