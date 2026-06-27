"""Shared helpers for LLM JSON parsing and transient error detection."""

from __future__ import annotations

from ecom_evaluator.config import TRANSIENT_API_CODES


def extract_json_text(raw: str) -> str:
    text = raw.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def is_transient_api_error(exc: Exception) -> bool:
    status_code = getattr(exc, "status_code", None) or getattr(exc, "code", None)
    if status_code in TRANSIENT_API_CODES:
        return True
    message = str(exc).lower()
    return any(p in message for p in ("rate limit", "overloaded", "try again", "503", "429"))
