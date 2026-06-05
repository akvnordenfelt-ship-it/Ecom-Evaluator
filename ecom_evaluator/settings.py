"""Environment and API key resolution."""

from __future__ import annotations

import os

from ecom_evaluator.config import PROJECT_ROOT


def load_env_api_key() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass

    key = os.getenv("GROQ_API_KEY", "").strip()
    if key:
        return key

    try:
        import streamlit as st

        if hasattr(st, "secrets"):
            return (st.secrets.get("GROQ_API_KEY") or "").strip()
    except Exception:
        pass

    return ""


def resolve_api_key(form_key: str) -> str:
    if form_key.strip():
        return form_key.strip()
    return load_env_api_key()


def has_shared_api_key() -> bool:
    """True when the server provides a key (env / Streamlit secrets)."""
    return bool(load_env_api_key())


def uses_shared_api_key(form_key: str) -> bool:
    """True when this run will bill the hosted key, not a user override."""
    return has_shared_api_key() and not form_key.strip()
