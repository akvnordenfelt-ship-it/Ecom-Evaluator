"""Workspace motion — reveal animations and micro-interactions."""

from __future__ import annotations

import streamlit.components.v1 as components

WORKSPACE_MOTION_CSS = """
@keyframes cm-ws-rise {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: none; }
}
@keyframes cm-ws-glow {
    0%, 100% { opacity: 0.35; transform: translate(-10%, -10%) scale(1); }
    50% { opacity: 0.65; transform: translate(6%, 6%) scale(1.08); }
}
@keyframes cm-ws-check-pop {
    0% { transform: scale(0.6); opacity: 0.4; }
    70% { transform: scale(1.15); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes cm-ws-shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

html.cm-ws-motion-ready .cm-ws-reveal {
    opacity: 0;
    transform: translateY(18px);
}
html.cm-ws-motion-ready .cm-ws-reveal.is-visible {
    animation: cm-ws-rise 0.65s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
html.cm-ws-motion-ready .cm-ws-reveal-delay-1.is-visible { animation-delay: 0.06s; }
html.cm-ws-motion-ready .cm-ws-reveal-delay-2.is-visible { animation-delay: 0.12s; }
html.cm-ws-motion-ready .cm-ws-reveal-delay-3.is-visible { animation-delay: 0.18s; }
html.cm-ws-motion-ready .cm-ws-reveal-delay-4.is-visible { animation-delay: 0.24s; }

.cm-tool-side-promo {
    position: relative;
    overflow: hidden;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
.cm-tool-side-promo::after {
    content: "";
    position: absolute;
    width: 140%;
    height: 140%;
    top: -20%;
    left: -20%;
    background: radial-gradient(circle, rgba(96, 165, 250, 0.22) 0%, transparent 62%);
    pointer-events: none;
    animation: cm-ws-glow 7s ease-in-out infinite;
}
.cm-tool-side-promo:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 36px rgba(0, 0, 0, 0.22);
}
.cm-tool-checklist,
.cm-tool-score-guide {
    transition: transform 0.22s ease, border-color 0.22s ease;
}
.cm-tool-checklist:hover,
.cm-tool-score-guide:hover {
    transform: translateY(-1px);
    border-color: rgba(96, 165, 250, 0.28);
}
.cm-tool-check-row.is-done .cm-tool-check-dot {
    animation: cm-ws-check-pop 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}
.cm-ws-score-row {
    border-radius: 8px;
    padding: 0.28rem 0.35rem;
    margin: 0 -0.35rem;
    cursor: default;
    transition: transform 0.2s ease, background 0.2s ease, color 0.2s ease;
}
.cm-ws-score-row:hover {
    transform: translateX(4px);
    background: rgba(43, 89, 255, 0.1);
    color: var(--ws-text);
}
.stApp:has(.cm-workspace-mode-white) .cm-ws-score-row:hover {
    background: rgba(43, 89, 255, 0.08);
}
.cm-tool-main-head {
    animation: cm-ws-rise 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_required_card"] {
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_required_card"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] {
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"]:hover {
    border-color: rgba(96, 165, 250, 0.28) !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] details[open] {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] details summary {
    transition: color 0.2s ease, background 0.2s ease;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] details summary:hover {
    color: #93C5FD !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"] {
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, filter 0.2s ease, box-shadow 0.2s ease !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]:hover:not(:disabled) {
    box-shadow: 0 10px 28px rgba(43, 89, 255, 0.35) !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        105deg,
        transparent 0%,
        rgba(255, 255, 255, 0.2) 48%,
        transparent 100%
    );
    background-size: 200% 100%;
    opacity: 0;
    transition: opacity 0.2s ease;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]:hover:not(:disabled)::after {
    opacity: 1;
    animation: cm-ws-shimmer 1.1s ease infinite;
}

@media (prefers-reduced-motion: reduce) {
    html.cm-ws-motion-ready .cm-ws-reveal,
    html.cm-ws-motion-ready .cm-ws-reveal.is-visible,
    .cm-tool-main-head,
    .cm-tool-side-promo::after,
    .cm-tool-check-row.is-done .cm-tool-check-dot {
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
    }
    .cm-tool-side-promo:hover,
    .cm-tool-checklist:hover,
    .cm-tool-score-guide:hover,
    .stApp:has(.cm-workspace) div[class*="st-key-form_required_card"]:hover {
        transform: none;
    }
}
"""

_MOTION_JS = r"""
(function () {
    const win = window.parent;
    const doc = win.document;
    if (!doc.querySelector(".cm-workspace")) return;

    function reveal(node) {
        if (!node.classList.contains("is-visible")) {
            node.classList.add("is-visible");
        }
    }

    function scan() {
        doc.documentElement.classList.add("cm-ws-motion-ready");
        doc.querySelectorAll(".cm-ws-reveal").forEach(function (node) {
            const rect = node.getBoundingClientRect();
            const vh = win.innerHeight || doc.documentElement.clientHeight || 0;
            if (rect.top < vh * 0.96) reveal(node);
        });
    }

    if (!win.__cmWsMotion) {
        win.__cmWsMotion = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) reveal(entry.target);
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -4% 0px" }
        );
        win.__cmWsMotionScan = scan;
        let scanQueued = false;
        function queueScan() {
            if (scanQueued) return;
            scanQueued = true;
            win.requestAnimationFrame(function () {
                scanQueued = false;
                scan();
            });
        }
        new MutationObserver(queueScan).observe(doc.body, { childList: true, subtree: true });
    }

    doc.querySelectorAll(".cm-ws-reveal:not([data-cm-ws-observed])").forEach(function (node) {
        node.dataset.cmWsObserved = "1";
        win.__cmWsMotion.observe(node);
    });
    scan();
})();
"""


_TOOL_SCROLL_CEIL_JS = r"""
(function () {
    const win = window.parent;
    const doc = win.document;
    if (!doc.querySelector(".cm-workspace")) return;

    function navHeight() {
        const raw = getComputedStyle(doc.documentElement).getPropertyValue("--ps-nav-h");
        const parsed = parseFloat(raw);
        return Number.isFinite(parsed) ? parsed : 76;
    }

    function anchor() {
        return (
            doc.querySelector('[class*="st-key-workspace_theme_strip"]') ||
            doc.querySelector(".cm-tool-main-head")
        );
    }

    function scrollTargets() {
        const targets = [doc.documentElement, doc.body];
        doc.querySelectorAll('[data-testid="stAppViewContainer"], section[data-testid="stMain"]').forEach(
            function (node) {
                targets.push(node);
            }
        );
        return targets;
    }

    if (!win.__cmToolScrollState) {
        win.__cmToolScrollState = { minScroll: null };
    }
    const state = win.__cmToolScrollState;

    function measure() {
        const mark = anchor();
        if (!mark) {
            state.minScroll = 0;
            return;
        }
        const scrollY = win.scrollY || doc.documentElement.scrollTop || 0;
        const offset = mark.getBoundingClientRect().top - navHeight();
        state.minScroll = Math.max(0, scrollY + offset);
    }

    function clamp() {
        if (state.minScroll === null) {
            measure();
        }
        const floor = state.minScroll || 0;
        scrollTargets().forEach(function (node) {
            if (typeof node.scrollTop === "number" && node.scrollTop < floor) {
                node.scrollTop = floor;
            }
        });
        const pageY = win.scrollY || doc.documentElement.scrollTop || 0;
        if (pageY < floor) {
            win.scrollTo(0, floor);
        }
    }

    if (!win.__cmToolScrollCeilListeners) {
        win.__cmToolScrollCeilListeners = true;
        win.addEventListener("scroll", clamp, { passive: true, capture: true });
        doc.addEventListener("scroll", clamp, { passive: true, capture: true });
        win.addEventListener("resize", function () {
            state.minScroll = null;
            measure();
            clamp();
        });
    }

    win.__cmToolScrollRemeasure = function () {
        state.minScroll = null;
        measure();
        clamp();
    };

    win.requestAnimationFrame(function () {
        state.minScroll = null;
        measure();
        clamp();
    });
})();
"""


def install_tool_scroll_ceil() -> None:
    """Prevent scrolling above the tool header / theme strip."""
    components.html(
        f"""
        <script>
        {_TOOL_SCROLL_CEIL_JS}
        </script>
        """,
        height=0,
        width=0,
    )


def install_workspace_motion() -> None:
    components.html(
        f"""
        <script>
        {_MOTION_JS}
        </script>
        """,
        height=0,
        width=0,
    )
