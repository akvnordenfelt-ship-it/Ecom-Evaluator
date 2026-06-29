"""Route JSON generation to Claude (Anthropic SDK)."""

from __future__ import annotations

from typing import Callable, TypeVar

import streamlit as st
from pydantic import BaseModel

from ecom_evaluator.evaluation_engine import parse_json_phase, run_json_phase

T = TypeVar("T", bound=BaseModel)


def is_claude_model(model: str) -> bool:
    return model.strip().lower().startswith("claude")


def generate_json(
    *,
    provider: str,
    gemini_client=None,
    anthropic_api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
    max_output_tokens: int,
    temperature: float = 0.35,
    enable_web_search: bool = False,
) -> str:
    from ecom_evaluator.anthropic_client import generate_json as anthropic_generate_json

    return anthropic_generate_json(
        api_key=anthropic_api_key,
        model=model,
        system_instruction=system_instruction,
        user_text=user_prompt,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        image_bytes=image_bytes,
        image_mime=image_mime,
        enable_web_search=enable_web_search,
    )


def run_phase_with_retries(
    *,
    provider: str,
    gemini_client=None,
    anthropic_api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
    model_class: type[T],
    normalize_fn: Callable,
    phase_label: str,
    max_output_tokens: int,
    temperature: float = 0.35,
    max_parse_attempts: int = 3,
    enable_web_search: bool = False,
) -> T:
    from ecom_evaluator.anthropic_client import generate_json as anthropic_generate_json
    from ecom_evaluator.exceptions import AnalysisError

    last_error: AnalysisError | None = None
    for attempt in range(max_parse_attempts):
        if attempt > 0:
            st.warning(f"{phase_label} — retrying ({attempt + 1}/{max_parse_attempts})…")
        raw = anthropic_generate_json(
            api_key=anthropic_api_key,
            model=model,
            system_instruction=system_instruction,
            user_text=user_prompt,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            image_bytes=image_bytes,
            image_mime=image_mime,
            enable_web_search=enable_web_search,
        )
        try:
            return parse_json_phase(raw, model_class, normalize_fn, phase_label=phase_label)
        except AnalysisError as exc:
            last_error = exc
            if attempt >= max_parse_attempts - 1:
                raise
    raise last_error or AnalysisError(f"{phase_label} failed.")
