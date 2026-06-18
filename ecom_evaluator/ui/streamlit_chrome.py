"""Hide Streamlit platform chrome, deploy button, and branding stamps."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

# Do NOT use bare `header { }` — it would hide our `.site-header` navbar markup.
STREAMLIT_BRANDING_HIDE_CSS = """
#MainMenu {
    visibility: hidden !important;
    display: none !important;
}
footer {
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
div[data-testid="stDecoration"],
[data-testid="stDecoration"] {
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
#GithubIcon,
.viewerBadge_container__67w8K,
.viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK,
[class*="viewerBadge_container"],
[class*="viewerBadge_link"],
[class*="viewerBadge_text"],
[class*="styles_viewerBadge"],
[class*="viewerBadge"],
[class*="StyledManageApp"],
[class*="MadeWithStreamlit"],
a[href*="streamlit.io/cloud"],
a[href*="share.streamlit.io"],
a[href*="streamlit.io"][target="_blank"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    max-height: 0 !important;
    width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
    position: fixed !important;
    top: -10000px !important;
    left: -10000px !important;
}

/* Keep Crow Metrics navbar visible */
header.site-header,
.site-header,
.site-header * {
    visibility: visible !important;
    display: revert !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: revert !important;
    top: auto !important;
    left: auto !important;
    width: auto !important;
    max-width: none !important;
    height: auto !important;
    max-height: none !important;
}
.site-header {
    display: block !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
}
.site-header__inner,
.site-header__bar,
.site-header__brand,
.site-header__nav,
.site-header__actions,
.site-header__mobile-drawer,
.site-header__menu-btn {
    display: flex !important;
}
.site-header__brand {
    display: inline-flex !important;
}
.site-header__mobile-drawer {
    display: block !important;
}
.site-header.is-mobile-open .site-header__mobile-drawer {
    display: block !important;
}
"""

_BRANDING_JS = r"""
(function () {
    const STYLE_ID = "ps-hide-streamlit-chrome";
    const SELECTORS = [
        "#MainMenu",
        "footer",
        'header[data-testid="stHeader"]',
        '[data-testid="stDecoration"]',
        'div[data-testid="stDecoration"]',
        '[data-testid="stStatusWidget"]',
        '[data-testid="stToolbar"]',
        '[data-testid="stAppDeployButton"]',
        '[data-testid="stDeployButton"]',
        '[data-testid="stHeaderActionElements"]',
        '[data-testid="stMainMenu"]',
        ".stAppDeployButton",
        ".stDeployButton",
        "#GithubIcon",
        ".viewerBadge_container__67w8K",
        ".viewerBadge_container__1QSob",
        ".styles_viewerBadge__1yB5_",
        ".viewerBadge_link__1S137",
        ".viewerBadge_text__1JaDK",
        '[class*="viewerBadge_container"]',
        '[class*="viewerBadge_link"]',
        '[class*="viewerBadge_text"]',
        '[class*="styles_viewerBadge"]',
        '[class*="viewerBadge"]',
        '[class*="StyledManageApp"]',
        '[class*="MadeWithStreamlit"]',
        'a[href*="streamlit.io/cloud"]',
        'a[href*="share.streamlit.io"]',
    ];

    function collectWindows(start) {
        const wins = [];
        const seen = new Set();
        function walk(win) {
            if (!win || seen.has(win)) return;
            seen.add(win);
            wins.push(win);
            try {
                for (let i = 0; i < win.frames.length; i += 1) {
                    walk(win.frames[i]);
                }
            } catch (e) {}
            try {
                if (win.parent && win.parent !== win) walk(win.parent);
            } catch (e) {}
        }
        walk(start || window);
        try {
            if (window.top) walk(window.top);
        } catch (e) {}
        return wins;
    }

    function injectStyle(doc, css) {
        if (!doc || doc.getElementById(STYLE_ID)) return;
        const style = doc.createElement("style");
        style.id = STYLE_ID;
        style.textContent = css;
        (doc.head || doc.documentElement).appendChild(style);
    }

    function hideNode(el) {
        if (!el || el.closest(".site-header")) return;
        el.style.setProperty("display", "none", "important");
        el.style.setProperty("visibility", "hidden", "important");
        el.style.setProperty("opacity", "0", "important");
        el.style.setProperty("pointer-events", "none", "important");
        el.setAttribute("aria-hidden", "true");
    }

    function hideBrandingIn(doc) {
        if (!doc) return;
        SELECTORS.forEach(function (sel) {
            try {
                doc.querySelectorAll(sel).forEach(hideNode);
            } catch (e) {}
        });

        doc.querySelectorAll("a, button, span, div, img").forEach(function (el) {
            if (el.closest(".site-header")) return;
            const label = (
                (el.textContent || "") +
                " " +
                (el.getAttribute("title") || "") +
                " " +
                (el.getAttribute("aria-label") || "") +
                " " +
                (el.getAttribute("href") || "") +
                " " +
                (el.className || "")
            ).toLowerCase();
            if (
                /hosted with streamlit|made with streamlit|manage app|viewerbadge|deploy/.test(
                    label
                ) ||
                /streamlit\.io\/(cloud|share)/.test(label)
            ) {
                hideNode(el);
                const wrap = el.closest('[class*="viewerBadge"], [class*="StyledManageApp"]');
                if (wrap) hideNode(wrap);
            }
        });

        /* Bottom-right fixed overlays (Cloud profile / red badge) */
        doc.querySelectorAll("div, a, button").forEach(function (el) {
            if (el.closest(".site-header")) return;
            let style;
            try {
                style = doc.defaultView.getComputedStyle(el);
            } catch (e) {
                return;
            }
            if (style.position !== "fixed" && style.position !== "absolute") return;
            const rect = el.getBoundingClientRect();
            const vw = doc.documentElement.clientWidth || 0;
            const vh = doc.documentElement.clientHeight || 0;
            if (rect.bottom < vh - 140 || rect.right < vw - 180) return;
            const blob = (
                (el.className || "") +
                " " +
                (el.textContent || "") +
                " " +
                (el.innerHTML || "")
            ).toLowerCase();
            if (
                /viewerbadge|streamlit|hosted with|manage app|profile/.test(blob) ||
                el.querySelector('[class*="viewerBadge"], img[alt*="streamlit"], img[src*="streamlit"]')
            ) {
                hideNode(el);
            }
        });
    }

    function sweep(css) {
        collectWindows(window).forEach(function (win) {
            try {
                injectStyle(win.document, css);
                hideBrandingIn(win.document);
            } catch (e) {}
        });
    }

    window.__psStreamlitChromeSweep = sweep;
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
    """Inject CSS/JS into app + parent frames (Streamlit Cloud shell)."""
    css_json = repr(STREAMLIT_BRANDING_HIDE_CSS)
    components.html(
        f"""
        <script>
        {_BRANDING_JS}
        (function () {{
            const css = {css_json};
            function run() {{
                if (window.__psStreamlitChromeSweep) window.__psStreamlitChromeSweep(css);
            }}
            run();
            let ticks = 0;
            const fast = setInterval(function () {{
                run();
                ticks += 1;
                if (ticks >= 24) clearInterval(fast);
            }}, 250);
            setInterval(run, 2000);
            try {{
                const win = window.parent;
                const doc = win.document;
                if (doc.body) {{
                    new MutationObserver(run).observe(doc.body, {{
                        childList: true,
                        subtree: true,
                    }});
                }}
            }} catch (e) {{}}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )
