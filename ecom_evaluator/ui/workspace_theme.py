"""Workspace appearance — dark (navy) or bright."""

from __future__ import annotations

import html

import streamlit as st

WORKSPACE_THEME_DARK = "dark"
WORKSPACE_THEME_BRIGHT = "bright"
WORKSPACE_THEMES = (WORKSPACE_THEME_DARK, WORKSPACE_THEME_BRIGHT)
DEFAULT_WORKSPACE_THEME = WORKSPACE_THEME_DARK

_LEGACY_THEME_MAP = {
    "black": WORKSPACE_THEME_DARK,
    "original": WORKSPACE_THEME_DARK,
    "white": WORKSPACE_THEME_BRIGHT,
    "dark": WORKSPACE_THEME_DARK,
    "bright": WORKSPACE_THEME_BRIGHT,
}

_THEME_LABELS = {
    WORKSPACE_THEME_DARK: "Dark",
    WORKSPACE_THEME_BRIGHT: "Bright",
}


def _normalize_theme(mode: str | None) -> str:
    if not mode:
        return DEFAULT_WORKSPACE_THEME
    return _LEGACY_THEME_MAP.get(mode, DEFAULT_WORKSPACE_THEME)


def init_workspace_theme_state() -> None:
    if "workspace_theme" not in st.session_state:
        st.session_state["workspace_theme"] = DEFAULT_WORKSPACE_THEME
        return
    st.session_state["workspace_theme"] = _normalize_theme(st.session_state.get("workspace_theme"))


def get_workspace_theme() -> str:
    init_workspace_theme_state()
    return _normalize_theme(st.session_state.get("workspace_theme"))


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
        cols = st.columns(2, gap="small")
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
