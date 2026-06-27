"""Environment and API key resolution."""

from __future__ import annotations

import os

from ecom_evaluator.config import PROJECT_ROOT


def _read_key_from_env() -> str:
    for name in ("GEMINI_API_KEY", "GOOGLE_AI_API_KEY", "GROQ_API_KEY"):
        key = os.getenv(name, "").strip()
        if key:
            return key
    return ""


def _read_key_from_streamlit_secrets() -> str:
    try:
        import streamlit as st

        if not hasattr(st, "secrets"):
            return ""
        for name in ("GEMINI_API_KEY", "GOOGLE_AI_API_KEY", "GROQ_API_KEY"):
            key = (st.secrets.get(name) or "").strip()
            if key:
                return key
        gemini_block = st.secrets.get("gemini")
        if isinstance(gemini_block, dict):
            nested = (gemini_block.get("api_key") or "").strip()
            if nested:
                return nested
    except Exception:
        pass
    return ""


def load_env_api_key() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass

    return _read_key_from_env() or _read_key_from_streamlit_secrets()


def resolve_api_key(form_key: str) -> str:
    if form_key.strip():
        return form_key.strip()
    return load_env_api_key()


def has_shared_api_key() -> bool:
    return bool(load_env_api_key())


def uses_shared_api_key(form_key: str) -> bool:
    return has_shared_api_key() and not form_key.strip()


def _read_anthropic_key_from_env() -> str:
    return os.getenv("ANTHROPIC_API_KEY", "").strip()


def _read_anthropic_key_from_streamlit_secrets() -> str:
    try:
        import streamlit as st

        if not hasattr(st, "secrets"):
            return ""
        key = (st.secrets.get("ANTHROPIC_API_KEY") or "").strip()
        if key:
            return key
        anthropic_block = st.secrets.get("anthropic")
        if isinstance(anthropic_block, dict):
            nested = (anthropic_block.get("api_key") or "").strip()
            if nested:
                return nested
    except Exception:
        pass
    return ""


def load_anthropic_api_key() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass
    return _read_anthropic_key_from_env() or _read_anthropic_key_from_streamlit_secrets()


def resolve_anthropic_api_key() -> str:
    return load_anthropic_api_key()


def has_anthropic_api_key() -> bool:
    return bool(load_anthropic_api_key())
