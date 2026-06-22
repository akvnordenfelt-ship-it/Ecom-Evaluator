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

# Streamlit Cloud shell (parent frame) — badges + creator profile chip only.
CLOUD_BADGE_HIDE_CSS = """
[class*="viewerBadge_container"],
[class*="viewerBadge_link"],
[class*="viewerBadge_text"],
[class*="styles_viewerBadge"],
[class*="viewerBadge"],
[class*="StyledManageApp"],
[class*="MadeWithStreamlit"],
[class*="creatorBadge"],
[class*="CreatorBadge"],
[class*="profileBadge"],
[class*="ProfileBadge"],
[class*="userBadge"],
[class*="UserBadge"],
[class*="userAvatar"],
[class*="UserAvatar"],
[class*="creatorChip"],
[class*="CreatorChip"],
[data-testid*="creator"],
[data-testid*="Creator"],
[data-testid*="profileBadge"],
a[href*="discuss.streamlit.io/u/"],
a[href*="share.streamlit.io/"],
a[href*="streamlit.io/community/profile"],
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
    '[class*="creatorBadge"]',
    '[class*="CreatorBadge"]',
    '[class*="profileBadge"]',
    '[class*="ProfileBadge"]',
    '[class*="userBadge"]',
    '[class*="UserBadge"]',
    '[class*="userAvatar"]',
    '[class*="UserAvatar"]',
    '[class*="creatorChip"]',
    '[class*="CreatorChip"]',
    '[data-testid*="creator"]',
    '[data-testid*="Creator"]',
    '[data-testid*="profileBadge"]',
    'a[href*="discuss.streamlit.io/u/"]',
    'a[href*="share.streamlit.io/"]',
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

    function hideNode(el) {
        if (!el) return;
        el.style.setProperty("display", "none", "important");
        el.style.setProperty("visibility", "hidden", "important");
        el.style.setProperty("opacity", "0", "important");
        el.style.setProperty("pointer-events", "none", "important");
    }

    function hideMatches(doc, selectors) {
        if (!doc) return;
        selectors.forEach(function (sel) {
            try {
                doc.querySelectorAll(sel).forEach(hideNode);
            } catch (e) {}
        });
    }

    function isAppDocument(doc) {
        try {
            return !!doc.querySelector('[data-testid="stApp"], .stApp');
        } catch (e) {
            return false;
        }
    }

    function removeLegacyCornerCovers(doc) {
        if (!doc) return;
        try {
            doc.querySelectorAll("#ps-cloud-corner-cover").forEach(function (el) {
                el.remove();
            });
        } catch (e) {}
    }

    function hideCloudProfileChips(doc) {
        if (!doc || isAppDocument(doc)) return;

        doc.querySelectorAll("a, button, div").forEach(function (el) {
            let style;
            try {
                style = doc.defaultView.getComputedStyle(el);
            } catch (e) {
                return;
            }

            if (style.position !== "fixed" && style.position !== "absolute") return;

            const rect = el.getBoundingClientRect();
            if (rect.width > 96 || rect.height > 96 || rect.width < 6) return;

            const vw = doc.documentElement.clientWidth || 0;
            const vh = doc.documentElement.clientHeight || 0;
            if (rect.right < vw - 100 || rect.bottom < vh - 100) return;

            const href = (el.getAttribute("href") || "").toLowerCase();
            const aria = (el.getAttribute("aria-label") || "").toLowerCase();
            const title = (el.getAttribute("title") || "").toLowerCase();
            const cls = String(el.className || "").toLowerCase();
            const meta = href + " " + aria + " " + title + " " + cls;
            const hasAvatar = el.querySelector(
                'img, svg, picture, [class*="avatar"], [class*="Avatar"]'
            );

            if (
                /discuss\.streamlit|share\.streamlit|viewerbadge|creator|profile|user-badge|userbadge/.test(
                    meta
                ) ||
                (hasAvatar && rect.width <= 80 && rect.height <= 80)
            ) {
                hideNode(el);
            }
        });
    }

    function parentDocuments() {
        const docs = [];
        let win = window;
        for (let i = 0; i < 8; i += 1) {
            try {
                if (win.document && !docs.includes(win.document)) docs.push(win.document);
                if (!win.parent || win.parent === win) break;
                win = win.parent;
            } catch (e) {
                break;
            }
        }
        try {
            if (window.top && window.top.document && !docs.includes(window.top.document)) {
                docs.push(window.top.document);
            }
        } catch (e) {}
        return docs;
    }

    window.__psStreamlitChromeSweep = function (appCss, cloudCss, badgeSelectors) {
        injectStyle(document, appCss, APP_STYLE_ID);
        hideMatches(document, badgeSelectors);

        parentDocuments().forEach(function (doc) {
            if (doc === document) return;
            injectStyle(doc, cloudCss, CLOUD_STYLE_ID);
            hideMatches(doc, badgeSelectors);
            hideCloudProfileChips(doc);
            removeLegacyCornerCovers(doc);
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


_APP_SHELL_SYNC_JS = r"""
(function () {
    const doc = window.parent.document;
    if (!doc || !doc.documentElement) return;

    const isAuth = !!doc.querySelector(".cm-auth-page, .auth-page-marker");
    doc.documentElement.classList.toggle("cm-auth-active", isAuth);

    if (!isAuth) {
        doc.querySelectorAll(
            ".auth-page-marker, .auth-page-backdrop, .auth-form-back, .cm-auth-backdrop, .cm-auth-back"
        ).forEach(function (el) {
            el.remove();
        });
    }

    const header = doc.querySelector(".site-header");
    const drawerOpen = !!(header && header.classList.contains("is-mobile-open"));
    if (!drawerOpen) {
        doc.documentElement.classList.remove("ps-nav-open");
    }
})();
"""


def install_app_shell_sync() -> None:
    """Keep document-level layout classes in sync with the current Streamlit view."""
    components.html(
        f"""
        <script>
        {_APP_SHELL_SYNC_JS}
        </script>
        """,
        height=0,
        width=0,
    )


def install_streamlit_branding_hide_bridge() -> None:
    """Hide in-app chrome + Cloud badge/profile in parent frame without touching app layout."""
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
                if (ticks >= 16) clearInterval(fast);
            }}, 400);
            setInterval(run, 3000);
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
