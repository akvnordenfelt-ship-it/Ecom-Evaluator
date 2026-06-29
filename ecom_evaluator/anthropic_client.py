"""Anthropic Claude JSON generation for all evaluation sections."""

from __future__ import annotations

import base64
import os
import time
from typing import Any

import streamlit as st

from ecom_evaluator.config import CROW_SYSTEM_PROMPT, MAX_API_ATTEMPTS, RETRY_BACKOFF_SECONDS, TRANSIENT_API_CODES
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_utils import is_transient_api_error


def _resolve_api_key(api_key: str) -> str:
    key = api_key.strip()
    if key:
        return key
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    try:
        key = (st.secrets.get("ANTHROPIC_API_KEY") or "").strip()
        if key:
            return key
    except Exception:
        pass
    return ""


def _anthropic_error_message(exc: Exception) -> str:
    return f"Claude API error: {exc}"


def _extract_text(response: Any) -> str:
    parts: list[str] = []
    for block in response.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    content = "".join(parts).strip()
    if not content:
        raise AnalysisError("Claude returned an empty response. Try again.")
    return content


def _build_user_content(
    *,
    prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
) -> str | list[dict[str, Any]]:
    if not image_bytes:
        return prompt
    mime = image_mime or "image/jpeg"
    encoded = base64.standard_b64encode(image_bytes).decode("ascii")
    return [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": mime,
                "data": encoded,
            },
        },
        {"type": "text", "text": prompt},
    ]


def generate_json(
    *,
    api_key: str = "",
    model: str,
    system_instruction: str,
    user_text: str,
    max_output_tokens: int,
    temperature: float = 0.35,
    image_bytes: bytes | None = None,
    image_mime: str | None = None,
    enable_web_search: bool = False,
    web_search_max_uses: int = 5,
) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise AnalysisError("anthropic package is not installed. Run: pip install anthropic") from exc

    resolved_key = _resolve_api_key(api_key)
    if not resolved_key:
        raise AnalysisError(
            "Anthropic API key is required. Add ANTHROPIC_API_KEY to Streamlit secrets or .env."
        )

    client = anthropic.Anthropic(api_key=resolved_key)
    system = (
        f"{CROW_SYSTEM_PROMPT}\n\n{system_instruction}\n\n"
        "Respond with valid JSON only — no markdown fences or commentary."
    )
    user_content = _build_user_content(
        prompt=user_text,
        image_bytes=image_bytes,
        image_mime=image_mime,
    )
    tools: list[dict[str, Any]] | None = None
    if enable_web_search:
        tools = [
            {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": web_search_max_uses,
            }
        ]

    last_error: Exception | None = None
    for attempt in range(MAX_API_ATTEMPTS):
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "max_tokens": max_output_tokens,
                "temperature": temperature,
                "system": system,
                "messages": [{"role": "user", "content": user_content}],
            }
            if tools:
                kwargs["tools"] = tools
            response = client.messages.create(**kwargs)
            return _extract_text(response)
        except AnalysisError:
            raise
        except Exception as exc:
            last_error = exc
            if enable_web_search and attempt == 0:
                tools = None
                continue
            status = getattr(exc, "status_code", None)
            if status in TRANSIENT_API_CODES or is_transient_api_error(exc):
                if attempt < MAX_API_ATTEMPTS - 1:
                    wait = RETRY_BACKOFF_SECONDS[min(attempt, len(RETRY_BACKOFF_SECONDS) - 1)]
                    st.warning(f"Claude busy — retrying in {wait}s…")
                    time.sleep(wait)
                    continue
            raise AnalysisError(_anthropic_error_message(exc)) from exc

    raise AnalysisError(f"Claude unavailable after {MAX_API_ATTEMPTS} attempts: {last_error}")


def build_user_text(*, prompt: str, image_bytes: bytes | None, image_mime: str | None) -> str:
    """Backward-compatible text-only helper."""
    if image_bytes is None:
        return prompt
    return (
        f"{prompt}\n\n"
        "[Note: a product image was provided — analyse packaging, materials, and visual appeal.]"
    )
