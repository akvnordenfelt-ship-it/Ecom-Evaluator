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
    st.segmented_control(
        "Appearance",
        options=list(WORKSPACE_THEMES),
        format_func=lambda key: _THEME_LABELS.get(key, str(key)),
        key="workspace_theme",
        label_visibility="collapsed",
    )
