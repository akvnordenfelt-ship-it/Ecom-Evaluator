"""Hide Streamlit platform chrome, deploy button, and branding stamps."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

STREAMLIT_BRANDING_HIDE_CSS = """
/* Streamlit default chrome */
#MainMenu,
footer,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stAppDeployButton"],
[data-testid="stHeaderActionElements"],
[data-testid="stMainMenu"],
.stAppDeployButton,
.stDeployButton,
button[kind="header"],
.viewerBadge_container,
[class*="viewerBadge"],
[class*="StyledManageApp"],
a[href*="streamlit.io"][target="_blank"]:not([href*="docs"]) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    position: fixed !important;
    top: -10000px !important;
    left: -10000px !important;
}

/* Remove reserved top gap when the Streamlit header is hidden */
.stApp > header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
}
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
    """CSS in parent frame + sweep for late-injected Cloud badges."""
    components.html(
        f"""
        <script>
        (function () {{
            const win = window.parent;
            const doc = win.document;
            if (win.__psStreamlitChromeHidden) return;
            win.__psStreamlitChromeHidden = true;

            const css = {STREAMLIT_BRANDING_HIDE_CSS!r};

            function injectStyle(root) {{
                if (!root || root.getElementById("ps-hide-streamlit-chrome")) return;
                const style = root.createElement("style");
                style.id = "ps-hide-streamlit-chrome";
                style.textContent = css;
                (root.head || root.documentElement).appendChild(style);
            }}

            const SELECTORS = [
                '[data-testid="stToolbar"]',
                '[data-testid="stDecoration"]',
                '[data-testid="stStatusWidget"]',
                '[data-testid="stAppDeployButton"]',
                '[data-testid="stHeaderActionElements"]',
                '[data-testid="stMainMenu"]',
                '.stAppDeployButton',
                '.stDeployButton',
                'footer',
                '#MainMenu',
                'header[data-testid="stHeader"]',
                '.viewerBadge_container',
                '[class*="viewerBadge"]',
                '[class*="StyledManageApp"]',
            ];

            function hideBrandingIn(root) {{
                if (!root) return;
                SELECTORS.forEach(function (sel) {{
                    try {{
                        root.querySelectorAll(sel).forEach(function (el) {{
                            el.style.setProperty("display", "none", "important");
                            el.style.setProperty("visibility", "hidden", "important");
                        }});
                    }} catch (e) {{}}
                }});
                root.querySelectorAll("a, button, span").forEach(function (el) {{
                    const label = ((el.textContent || "") + " " + (el.getAttribute("title") || "")).trim();
                    if (/hosted with streamlit|made with streamlit|manage app|deploy/i.test(label)) {{
                        el.style.setProperty("display", "none", "important");
                        const wrap = el.closest("div");
                        if (wrap && wrap.childElementCount <= 2) {{
                            wrap.style.setProperty("display", "none", "important");
                        }}
                    }}
                }});
            }}

            function sweep() {{
                injectStyle(doc);
                injectStyle(document);
                hideBrandingIn(doc);
                hideBrandingIn(document);
            }}

            sweep();
            if (doc.body) {{
                new MutationObserver(sweep).observe(doc.body, {{ childList: true, subtree: true }});
            }}
            win.setInterval(sweep, 2000);
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
