"""Workspace appearance — black, original (dark blue), or white."""

from __future__ import annotations

import html

import streamlit as st
import streamlit.components.v1 as components

WORKSPACE_THEME_BLACK = "black"
WORKSPACE_THEME_ORIGINAL = "original"
WORKSPACE_THEME_WHITE = "white"
WORKSPACE_THEMES = (WORKSPACE_THEME_BLACK, WORKSPACE_THEME_ORIGINAL, WORKSPACE_THEME_WHITE)
DEFAULT_WORKSPACE_THEME = WORKSPACE_THEME_ORIGINAL

_THEME_LABELS = {
    WORKSPACE_THEME_BLACK: "Black",
    WORKSPACE_THEME_ORIGINAL: "Blue",
    WORKSPACE_THEME_WHITE: "White",
}


def init_workspace_theme_state() -> None:
    if "workspace_theme" not in st.session_state:
        st.session_state["workspace_theme"] = DEFAULT_WORKSPACE_THEME


def get_workspace_theme() -> str:
    init_workspace_theme_state()
    mode = st.session_state.get("workspace_theme", DEFAULT_WORKSPACE_THEME)
    return mode if mode in WORKSPACE_THEMES else DEFAULT_WORKSPACE_THEME


def render_workspace_marker() -> None:
    mode = get_workspace_theme()
    st.markdown(
        f'<div class="form-workspace-marker cm-tool-form cm-workspace cm-workspace-mode-{html.escape(mode)}" '
        f'data-workspace-theme="{html.escape(mode)}" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )


def render_workspace_theme_switcher() -> None:
    init_workspace_theme_state()
    mode = get_workspace_theme()
    with st.container(key="workspace_theme_strip"):
        cols = st.columns(3, gap="small")
        for col, theme_key in zip(cols, WORKSPACE_THEMES, strict=True):
            with col:
                label = _THEME_LABELS[theme_key]
                is_active = mode == theme_key
                if st.button(
                    label,
                    key=f"ws_theme_pick_{theme_key}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                ):
                    if not is_active:
                        st.session_state["workspace_theme"] = theme_key
                        st.rerun()


def install_workspace_theme_button_sync() -> None:
    """Beat Streamlit emotion styles that paint secondary buttons white-on-white."""
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (!doc || win.__cmWsThemeButtonSync) return;
            win.__cmWsThemeButtonSync = true;

            const PALETTES = {
                original: {
                    idle: "#AEAEB2",
                    activeBg: "rgba(255, 255, 255, 0.1)",
                    activeText: "#F5F5F7",
                    activeBorder: "rgba(147, 197, 253, 0.35)",
                },
                black: {
                    idle: "#86868B",
                    activeBg: "rgba(255, 255, 255, 0.1)",
                    activeText: "#F5F5F7",
                    activeBorder: "rgba(255, 255, 255, 0.22)",
                },
                white: {
                    idle: "#6E6E73",
                    activeBg: "#FFFFFF",
                    activeText: "#1D1D1F",
                    activeBorder: "#D2D2D7",
                },
            };

            function readMode() {
                const marker = doc.querySelector("[class*='cm-workspace-mode-']");
                if (!marker) return "original";
                const match = String(marker.className).match(/cm-workspace-mode-(\\w+)/);
                return match ? match[1] : "original";
            }

            function paintButton(btn, palette) {
                const isPrimary =
                    btn.getAttribute("data-testid") === "stBaseButton-primary" ||
                    btn.getAttribute("kind") === "primary";
                const bg = isPrimary ? palette.activeBg : "transparent";
                const color = isPrimary ? palette.activeText : palette.idle;
                const border = isPrimary ? palette.activeBorder : "transparent";

                btn.style.setProperty("background", bg, "important");
                btn.style.setProperty("background-color", bg, "important");
                btn.style.setProperty("background-image", "none", "important");
                btn.style.setProperty("color", color, "important");
                btn.style.setProperty("-webkit-text-fill-color", color, "important");
                btn.style.setProperty("border-color", border, "important");
                btn.style.setProperty("box-shadow", "none", "important");
                btn.style.setProperty("filter", "none", "important");

                btn.querySelectorAll("div, span, p").forEach(function (node) {
                    node.style.setProperty("color", color, "important");
                    node.style.setProperty("-webkit-text-fill-color", color, "important");
                });
            }

            function syncThemeButtons() {
                if (!doc.querySelector(".cm-workspace")) return;
                const palette = PALETTES[readMode()] || PALETTES.original;
                doc
                    .querySelectorAll('[class*="st-key-ws_theme_pick_"] button')
                    .forEach(function (btn) {
                        paintButton(btn, palette);
                    });
            }

            syncThemeButtons();
            win.setInterval(syncThemeButtons, 400);
            try {
                new MutationObserver(syncThemeButtons).observe(doc.body, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: ["class", "data-testid", "kind", "style"],
                });
            } catch (e) {}
        })();
        </script>
        """,
        height=0,
        width=0,
    )
