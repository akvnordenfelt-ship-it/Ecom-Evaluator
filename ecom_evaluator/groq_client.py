"""Groq LLM product evaluation — two-phase JSON output for richer reports."""

from __future__ import annotations

import base64
import json
import time
from typing import Any, TypeVar

import streamlit as st
from groq import APIStatusError, Groq, RateLimitError
from pydantic import BaseModel, ValidationError

from ecom_evaluator.config import (
    GROQ_MAX_COMPLETION_TOKENS,
    GROQ_MODEL,
    GROQ_VISION_MODEL,
    MAX_API_ATTEMPTS,
    MAX_PARSE_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    TRANSIENT_API_CODES,
)
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_normalize import normalize_core_payload, normalize_marketing_payload
from ecom_evaluator.models import (
    MarketSearchHit,
    MarketingPhaseResponse,
    ProductCoreResponse,
    ProductEvaluationResponse,
)
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research

ENUM_RULES = """
Use EXACT enum strings:
- competitor_count_signal: Few | Moderate | Many | Unknown  (NOT "Medium")
- demand_estimate.level: Low | Medium | High | Unknown
- market_saturation.level: Low | Medium | High
- roi_potential / roi_outlook: Low | Medium | High
- organic_vs_paid: Organic-first | Paid-first | Balanced
"""

CORE_SYSTEM_INSTRUCTION = f"""You are ruthless Shark Tank investors plus senior e-commerce operators.
Evaluate the product opportunity using the form data AND live web research.

Respond with ONE valid JSON object only. No markdown fences.

Quality bar (critical):
- Write 3-5 substantive sentences for market_research.executive_summary.
- Each channel landscape (Amazon, AliExpress, independent stores) must be 2-4 specific sentences citing search results.
- Each score motivation must be 2-3 sentences referencing margin, competition, or demand evidence.
- key_competitors: up to 3 REAL listings from the research with actual URLs and titles.
- estimated_shipping_category: analyze billable weight using L×W×H÷5000 vs actual weight.

{ENUM_RULES}

JSON keys: final_score, market_research, short_term_potential, long_term_stability,
scalability, marketing_suitability, market_saturation, estimated_shipping_category."""

MARKETING_SYSTEM_INSTRUCTION = f"""You are a performance marketing strategist for e-commerce brands.
Build a detailed marketing playbook grounded in the core evaluation and web research provided.

Respond with ONE valid JSON object only. No markdown fences.

Quality bar (critical):
- marketing_plan.executive_summary: 3-4 sentences on exactly how to market THIS product.
- target_audience: specific persona, not generic "online shopper".
- organic_strategy + paid_ads_strategy: concrete formats, cadence, budget, targeting.
- platform_recommendations: exactly 3 platforms with fit_score, ROI signal, and competitor evidence from research.
- creative_concepts: exactly 2 with full script/copy lines, not one-liners.
- priority_playbook: exactly 3 actionable steps for this week.
- go_to_market_strategy: markdown with 3 phases, ~200 words total.

{ENUM_RULES}

JSON keys: marketing_plan, go_to_market_strategy."""

T = TypeVar("T", bound=BaseModel)


def logistics_summary(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> dict[str, float]:
    volume_cm3 = length_cm * width_cm * height_cm
    volume_dm3 = volume_cm3 / 1000
    dimensional_weight_kg = volume_cm3 / 5000 if volume_cm3 > 0 else 0.0
    billable_weight_kg = max(weight_kg, dimensional_weight_kg)
    return {
        "volume_cm3": volume_cm3,
        "volume_dm3": volume_dm3,
        "dimensional_weight_kg": dimensional_weight_kg,
        "billable_weight_kg": billable_weight_kg,
    }


def build_product_context(
    *,
    product_name: str,
    purchase_price: float,
    sales_price: float,
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
    description: str,
    has_image: bool,
    web_research_text: str,
) -> str:
    margin = sales_price - purchase_price
    margin_pct = (margin / sales_price * 100) if sales_price > 0 else 0.0
    logistics = logistics_summary(weight_kg, length_cm, width_cm, height_cm)
    image_note = (
        "Product image attached — assess packaging, quality, and feed-stopping visual appeal."
        if has_image
        else "No image — note uncertainty on visual/creative angles."
    )

    return f"""## Product
- Name: {product_name}

## Economics (USD)
- Purchase: ${purchase_price:.2f} | Sell: ${sales_price:.2f} | Margin: ${margin:.2f} ({margin_pct:.1f}%)

## Logistics
- Weight: {weight_kg:.3f} kg | Dims: {length_cm}×{width_cm}×{height_cm} cm
- Volume: {logistics['volume_dm3']:.2f} dm³ | Dim weight: {logistics['dimensional_weight_kg']:.3f} kg | Billable: {logistics['billable_weight_kg']:.3f} kg

## Founder notes
{description}

## Visual
{image_note}

{web_research_text}"""


def build_core_user_prompt(context: str) -> str:
    return f"{context}\n\nReturn phase-1 JSON: scores, market_research, shipping analysis."


def build_marketing_user_prompt(context: str, core: ProductCoreResponse) -> str:
    mr = core.market_research
    return f"""{context}

## Core evaluation (already completed)
- Final score: {core.final_score}/100
- Saturation: {core.market_saturation.level} — {core.market_saturation.motivation}
- Marketing suitability: {core.marketing_suitability.score}/100 — {core.marketing_suitability.motivation}
- Research summary: {mr.executive_summary}
- Strategic implications: {mr.strategic_implications}

Return phase-2 JSON: marketing_plan and go_to_market_strategy only. Be specific to this product."""


def build_messages(
    prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
    *,
    system_instruction: str,
) -> list[dict[str, Any]]:
    system = {"role": "system", "content": system_instruction}
    if image_bytes:
        mime = image_mime or "image/jpeg"
        encoded = base64.standard_b64encode(image_bytes).decode("ascii")
        user = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{encoded}"}},
            ],
        }
    else:
        user = {"role": "user", "content": prompt}
    return [system, user]


def select_model(*, has_image: bool) -> str:
    return GROQ_VISION_MODEL if has_image else GROQ_MODEL


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
    if isinstance(exc, RateLimitError):
        return True
    status_code = getattr(exc, "status_code", None)
    if status_code in TRANSIENT_API_CODES:
        return True
    message = str(exc).lower()
    return any(
        phrase in message
        for phrase in ("rate limit", "overloaded", "try again", "temporarily unavailable")
    )


def api_error_message(exc: Exception) -> str:
    if isinstance(exc, APIStatusError):
        return f"Groq API error ({exc.status_code}): {exc.message}"
    if isinstance(exc, RateLimitError):
        return f"Groq rate limit: {exc}"
    return f"Groq API error: {exc}"


def generate_with_retry(
    client: Groq,
    *,
    model: str,
    messages: list[dict[str, Any]],
) -> tuple[str, str | None]:
    last_error: Exception | None = None
    for attempt in range(MAX_API_ATTEMPTS):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.55,
                max_completion_tokens=GROQ_MAX_COMPLETION_TOKENS,
                response_format={"type": "json_object"},
            )
            choice = response.choices[0]
            content = choice.message.content or ""
            finish_reason = getattr(choice, "finish_reason", None)
            if not content.strip():
                raise AnalysisError("Groq returned an empty response. Try again.")
            return content, finish_reason
        except AnalysisError:
            raise
        except Exception as exc:
            last_error = exc
            if attempt >= MAX_API_ATTEMPTS - 1 or not is_transient_api_error(exc):
                raise AnalysisError(api_error_message(exc)) from exc
            wait_seconds = RETRY_BACKOFF_SECONDS[attempt]
            st.warning(f"Groq busy — retrying in {wait_seconds}s…")
            time.sleep(wait_seconds)
    raise AnalysisError(f"Groq unavailable after {MAX_API_ATTEMPTS} attempts: {last_error}")


def parse_json_phase(
    raw: str,
    model_class: type[T],
    normalize_fn,
    *,
    phase_label: str,
    truncated: bool = False,
) -> T:
    cleaned = extract_json_text(raw)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        hint = " Response may have been cut off." if truncated else ""
        raise AnalysisError(f"{phase_label}: invalid JSON.{hint} Try again.") from exc
    try:
        return model_class.model_validate(normalize_fn(payload))
    except ValidationError as err:
        detail = str(err.errors()[0]["loc"]) if err.errors() else "unknown field"
        raise AnalysisError(
            f"{phase_label}: incomplete report near {detail}. "
            "The model did not generate enough detail — try again."
        ) from err


def run_phase_with_retries(
    client: Groq,
    *,
    model: str,
    messages: list[dict[str, Any]],
    model_class: type[T],
    normalize_fn,
    phase_label: str,
) -> T:
    last_error: AnalysisError | None = None
    for attempt in range(MAX_PARSE_ATTEMPTS):
        if attempt > 0:
            st.warning(f"{phase_label} incomplete — retrying ({attempt + 1}/{MAX_PARSE_ATTEMPTS})…")
        raw, finish_reason = generate_with_retry(client, model=model, messages=messages)
        try:
            return parse_json_phase(
                raw,
                model_class,
                normalize_fn,
                phase_label=phase_label,
                truncated=finish_reason == "length",
            )
        except AnalysisError as exc:
            last_error = exc
            if attempt >= MAX_PARSE_ATTEMPTS - 1:
                raise
    raise last_error or AnalysisError(f"{phase_label} failed.")


def run_product_evaluation(
    *,
    api_key: str,
    product_name: str,
    purchase_price: float,
    sales_price: float,
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
    description: str,
    image_bytes: bytes | None,
    image_mime: str | None = None,
    web_research: list[MarketSearchHit] | None = None,
) -> ProductEvaluationResponse:
    if not api_key.strip():
        raise AnalysisError("API key is required.")

    research_hits = (
        web_research
        if web_research is not None
        else run_web_market_research(product_name=product_name, description=description)
    )
    web_research_text = format_web_research_for_prompt(research_hits)
    context = build_product_context(
        product_name=product_name,
        purchase_price=purchase_price,
        sales_price=sales_price,
        weight_kg=weight_kg,
        length_cm=length_cm,
        width_cm=width_cm,
        height_cm=height_cm,
        description=description,
        has_image=image_bytes is not None,
        web_research_text=web_research_text,
    )

    client = Groq(api_key=api_key.strip())
    vision_model = select_model(has_image=image_bytes is not None)

    with st.spinner("Phase 1/2 — Scores, market research, and investment verdict…"):
        core_messages = build_messages(
            build_core_user_prompt(context),
            image_bytes,
            image_mime,
            system_instruction=CORE_SYSTEM_INSTRUCTION,
        )
        core = run_phase_with_retries(
            client,
            model=vision_model,
            messages=core_messages,
            model_class=ProductCoreResponse,
            normalize_fn=normalize_core_payload,
            phase_label="Investment analysis",
        )

    with st.spinner("Phase 2/2 — Marketing playbook and go-to-market strategy…"):
        marketing_messages = build_messages(
            build_marketing_user_prompt(context, core),
            None,
            None,
            system_instruction=MARKETING_SYSTEM_INSTRUCTION,
        )
        marketing = run_phase_with_retries(
            client,
            model=GROQ_MODEL,
            messages=marketing_messages,
            model_class=MarketingPhaseResponse,
            normalize_fn=normalize_marketing_payload,
            phase_label="Marketing plan",
        )

    return ProductEvaluationResponse(
        **core.model_dump(),
        marketing_plan=marketing.marketing_plan,
        go_to_market_strategy=marketing.go_to_market_strategy,
    )


run_shark_tank_analysis = run_product_evaluation
