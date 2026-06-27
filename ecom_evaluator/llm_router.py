"""Route JSON generation to Gemini (free tier) or Claude (premium paid sections)."""

from __future__ import annotations

from typing import TypeVar

import streamlit as st
from pydantic import BaseModel

from ecom_evaluator.anthropic_client import generate_json as anthropic_generate_json
from ecom_evaluator.anthropic_client import build_user_text as anthropic_user_text
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.gemini_client import (
    build_user_parts,
    generate_json as gemini_generate_json,
    parse_json_phase,
)
from google import genai

T = TypeVar("T", bound=BaseModel)


def is_claude_model(model: str) -> bool:
    return model.strip().lower().startswith("claude")


def generate_json(
    *,
    provider: str,
    gemini_client: genai.Client | None,
    anthropic_api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
    max_output_tokens: int,
    temperature: float = 0.35,
) -> str:
    if provider == "anthropic" or is_claude_model(model):
        if not anthropic_api_key.strip():
            raise AnalysisError(
                "Anthropic API key is required for premium AI sections. "
                "Add ANTHROPIC_API_KEY to your .env or Streamlit secrets."
            )
        return anthropic_generate_json(
            api_key=anthropic_api_key,
            model=model,
            system_instruction=system_instruction,
            user_text=anthropic_user_text(
                prompt=user_prompt,
                image_bytes=image_bytes,
                image_mime=image_mime,
            ),
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )

    if gemini_client is None:
        raise AnalysisError("Gemini client is required for this evaluation phase.")
    return gemini_generate_json(
        gemini_client,
        model=model,
        system_instruction=system_instruction,
        user_parts=build_user_parts(user_prompt, image_bytes, image_mime),
        max_output_tokens=max_output_tokens,
        temperature=temperature,
    )


def run_phase_with_retries(
    *,
    provider: str,
    gemini_client: genai.Client | None,
    anthropic_api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
    model_class: type[T],
    normalize_fn,
    phase_label: str,
    max_output_tokens: int,
    temperature: float = 0.35,
    max_parse_attempts: int = 3,
) -> T:
    last_error: AnalysisError | None = None
    for attempt in range(max_parse_attempts):
        if attempt > 0:
            st.warning(f"{phase_label} — retrying ({attempt + 1}/{max_parse_attempts})…")
        raw = generate_json(
            provider=provider,
            gemini_client=gemini_client,
            anthropic_api_key=anthropic_api_key,
            model=model,
            system_instruction=system_instruction,
            user_prompt=user_prompt,
            image_bytes=image_bytes,
            image_mime=image_mime,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        try:
            return parse_json_phase(raw, model_class, normalize_fn, phase_label=phase_label)
        except AnalysisError as exc:
            last_error = exc
            if attempt >= max_parse_attempts - 1:
                raise
    raise last_error or AnalysisError(f"{phase_label} failed.")
