"""Anthropic Claude JSON generation for premium evaluation phases."""

from __future__ import annotations

import json
import time
from typing import Any

import streamlit as st

from ecom_evaluator.config import MAX_API_ATTEMPTS, RETRY_BACKOFF_SECONDS, TRANSIENT_API_CODES
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_utils import is_transient_api_error


def _anthropic_error_message(exc: Exception) -> str:
    return f"Claude API error: {exc}"


def generate_json(
    *,
    api_key: str,
    model: str,
    system_instruction: str,
    user_text: str,
    max_output_tokens: int,
    temperature: float = 0.35,
) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise AnalysisError("anthropic package is not installed. Run: pip install anthropic") from exc

    client = anthropic.Anthropic(api_key=api_key.strip())
    last_error: Exception | None = None

    for attempt in range(MAX_API_ATTEMPTS):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=max_output_tokens,
                temperature=temperature,
                system=(
                    f"{system_instruction}\n\n"
                    "Respond with valid JSON only — no markdown fences or commentary."
                ),
                messages=[{"role": "user", "content": user_text}],
            )
            parts: list[str] = []
            for block in response.content:
                text = getattr(block, "text", None)
                if text:
                    parts.append(text)
            content = "".join(parts).strip()
            if not content:
                raise AnalysisError("Claude returned an empty response. Try again.")
            return content
        except AnalysisError:
            raise
        except Exception as exc:
            last_error = exc
            status = getattr(exc, "status_code", None)
            if status in TRANSIENT_API_CODES or is_transient_api_error(exc):
                if attempt < MAX_API_ATTEMPTS - 1:
                    wait = RETRY_BACKOFF_SECONDS[attempt]
                    st.warning(f"Claude busy — retrying in {wait}s…")
                    time.sleep(wait)
                    continue
            raise AnalysisError(_anthropic_error_message(exc)) from exc

    raise AnalysisError(f"Claude unavailable after {MAX_API_ATTEMPTS} attempts: {last_error}")


def build_user_text(*, prompt: str, image_bytes: bytes | None, image_mime: str | None) -> str:
    if image_bytes is None:
        return prompt
    return (
        f"{prompt}\n\n"
        "[Note: a product image was provided in the original evaluation context — "
        "use the product description and profile already embedded above.]"
    )
