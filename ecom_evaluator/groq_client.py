"""Groq LLM product evaluation with JSON output + Pydantic validation."""

from __future__ import annotations

import base64
import json
import time
from typing import Any

import streamlit as st
from groq import APIStatusError, Groq, RateLimitError
from pydantic import ValidationError

from ecom_evaluator.config import (
    GROQ_MAX_COMPLETION_TOKENS,
    GROQ_MODEL,
    GROQ_VISION_MODEL,
    MAX_API_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    TRANSIENT_API_CODES,
)
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.models import MarketSearchHit, ProductEvaluationResponse
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research

SYSTEM_INSTRUCTION = """You are a panel of ruthless Shark Tank investors combined with senior
e-commerce operators (DTC, TikTok Shop, Amazon FBA). Your job is to evaluate whether a product
deserves investment of time and ad spend.

Respond with ONE valid JSON object only. No markdown fences, no commentary outside JSON.

Rules:
- Be critical, specific, and honest. No generic praise.
- You MUST fully populate `market_research` by analyzing the "Live web research (DuckDuckGo)" section.
- In `market_research`, synthesize Amazon, AliExpress, and independent-store findings separately.
- `key_competitors` must list real listings from the web research (use their URLs and titles). If none were found for a channel, say so in the landscape fields and leave competitors empty.
- `demand_estimate.estimated_sales_note` must be qualitative — never invent precise monthly unit counts unless a snippet states them.
- Ground `market_saturation` and all score motivations in BOTH the form data AND your `market_research` conclusions.
- Do not invent URLs, prices, or sales numbers absent from the web research snippets.
- Scores are integers from 0 (terrible) to 100 (exceptional).
- market_saturation.level must be exactly "Low", "Medium", or "High".
- estimated_shipping_category must analyze volumetric/dimensional weight using L×W×H cm ÷ 5000.
- Fully populate `marketing_plan` (target_audience, organic_strategy, paid_ads_strategy,
  platform_recommendations, competitor_marketing_insights, creative_concepts, priority_playbook).
- go_to_market_strategy must be a detailed multi-paragraph operational plan in Markdown (phases, fulfillment, risks).
- Top-level JSON keys required: final_score, market_research, short_term_potential, long_term_stability,
  scalability, marketing_suitability, market_saturation, estimated_shipping_category, marketing_plan,
  go_to_market_strategy."""


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


def build_user_prompt(
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
        "A product image is attached — assess packaging, perceived quality, visual hook potential, "
        "and whether it stands out in social feeds."
        if has_image
        else "No product image was provided — rely on the text and flag visual/marketing uncertainty."
    )

    return f"""Evaluate this e-commerce product opportunity.

## Product
- Name: {product_name}

## Economics (USD)
- Purchase price: ${purchase_price:.2f}
- Intended selling price: ${sales_price:.2f}
- Gross margin per unit: ${margin:.2f} ({margin_pct:.1f}% of selling price)

## Logistics
- Actual weight: {weight_kg:.3f} kg
- Dimensions (L×W×H cm): {length_cm:.1f} × {width_cm:.1f} × {height_cm:.1f}
- Package volume: {logistics['volume_dm3']:.2f} dm³ ({logistics['volume_cm3']:.0f} cm³)
- Dimensional weight (L×W×H/5000): {logistics['dimensional_weight_kg']:.3f} kg
- Estimated billable weight: {logistics['billable_weight_kg']:.3f} kg

## Founder notes
{description}

## Visual context
{image_note}

{web_research_text}

Return the complete evaluation as a single JSON object with marketing_plan included."""


def build_messages(
    prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
) -> list[dict[str, Any]]:
    system = {
        "role": "system",
        "content": SYSTEM_INSTRUCTION,
    }

    if image_bytes:
        mime = image_mime or "image/jpeg"
        encoded = base64.standard_b64encode(image_bytes).decode("ascii")
        user = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{encoded}"},
                },
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
    if isinstance(exc, APIStatusError):
        message = str(exc).lower()
        return any(
            phrase in message
            for phrase in ("rate limit", "overloaded", "try again", "temporarily unavailable")
        )
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
) -> str:
    last_error: Exception | None = None

    for attempt in range(MAX_API_ATTEMPTS):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.6,
                max_completion_tokens=GROQ_MAX_COMPLETION_TOKENS,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or ""
            if not content.strip():
                raise AnalysisError("Groq returned an empty response. Try again.")
            return content
        except AnalysisError:
            raise
        except Exception as exc:
            last_error = exc
            is_last_attempt = attempt >= MAX_API_ATTEMPTS - 1
            if is_last_attempt or not is_transient_api_error(exc):
                raise AnalysisError(api_error_message(exc)) from exc

            wait_seconds = RETRY_BACKOFF_SECONDS[attempt]
            st.warning(
                f"Groq servers are busy. Retrying in {wait_seconds} seconds… "
                f"(attempt {attempt + 2} of {MAX_API_ATTEMPTS})"
            )
            time.sleep(wait_seconds)

    if last_error is not None:
        raise AnalysisError(
            f"Groq API unavailable after {MAX_API_ATTEMPTS} attempts: {last_error}"
        ) from last_error
    raise AnalysisError("Groq API call failed after multiple retries. Please try again shortly.")


def parse_evaluation_response(raw: str) -> ProductEvaluationResponse:
    cleaned = extract_json_text(raw)
    try:
        return ProductEvaluationResponse.model_validate_json(cleaned)
    except ValidationError as first_error:
        try:
            return ProductEvaluationResponse.model_validate(json.loads(cleaned))
        except (json.JSONDecodeError, ValidationError) as inner:
            detail = str(first_error.errors()[0]["loc"]) if first_error.errors() else "unknown field"
            raise AnalysisError(
                "The AI response could not be parsed into a complete report "
                f"(validation failed near {detail}). Try running the analysis again."
            ) from inner


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

    prompt = build_user_prompt(
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
    model = select_model(has_image=image_bytes is not None)
    messages = build_messages(prompt, image_bytes, image_mime)
    raw = generate_with_retry(client, model=model, messages=messages)
    return parse_evaluation_response(raw)


run_shark_tank_analysis = run_product_evaluation
