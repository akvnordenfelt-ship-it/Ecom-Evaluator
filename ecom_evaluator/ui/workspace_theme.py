"""Workspace appearance — black, original (dark blue), or white."""

from __future__ import annotations

import html

import streamlit as st

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
    st.markdown('<div class="cm-workspace-theme-row">', unsafe_allow_html=True)
    st.markdown('<div class="cm-theme-pills-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)
