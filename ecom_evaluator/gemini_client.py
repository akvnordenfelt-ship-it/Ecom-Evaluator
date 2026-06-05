"""Gemini 2.5 Flash product evaluation with structured JSON output."""

from __future__ import annotations

import json
import time

import streamlit as st
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import ValidationError

from ecom_evaluator.config import (
    GEMINI_MODEL,
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

Rules:
- Be critical, specific, and honest. No generic praise.
- You MUST fully populate `market_research` by analyzing the "Live web research (DuckDuckGo)" section.
- In `market_research`, synthesize Amazon, AliExpress, and independent-store findings separately.
- `key_competitors` must list real listings from the web research (use their URLs and titles). If none were found for a channel, say so in the landscape fields and leave competitors empty.
- `demand_estimate.estimated_sales_note` must be qualitative (e.g. "likely moderate demand based on review volume language") — never invent precise monthly unit counts unless a snippet states them.
- Ground `market_saturation` and all score motivations in BOTH the form data AND your `market_research` conclusions.
- Do not invent URLs, prices, or sales numbers absent from the web research snippets.
- Scores are integers from 0 (terrible) to 100 (exceptional).
- market_saturation.level must be exactly "Low", "Medium", or "High".
- estimated_shipping_category must analyze volumetric/dimensional weight using the dimensions
  (common air-cargo formula: L×W×H cm ÷ 5000 = dimensional weight in kg) and compare to actual weight.
- Fully populate `marketing_plan` as a serious go-to-market marketing blueprint:
  - `target_audience`: infer persona, age range, psychographics, pain points, and platforms they use from the product description AND web research.
  - `organic_strategy`: UGC, content formats, posting cadence, creator angles — be specific to this product.
  - `paid_ads_strategy`: which paid channels, starter budget tier (as a string like "$20–50/day"), targeting, ROI outlook.
  - `platform_recommendations`: 3–6 platforms ranked by fit_score; each must cite how similar products/competitors succeeded there (highest-ROI signals from web research). Set organic_vs_paid to Organic-first, Paid-first, or Balanced.
  - `competitor_marketing_insights`: synthesize how competitors with similar products marketed (ads, influencers, Amazon PPC, etc.) based on search snippets — no invented campaigns.
  - `creative_concepts`: 2–4 concrete ad/content concepts with hook, format, and copy — not generic TikTok-only hooks.
  - `priority_playbook`: ordered list of the first actions to take this week.
- go_to_market_strategy must be a detailed multi-paragraph operational plan in Markdown (phases, fulfillment, risks).
- Output must match the JSON schema exactly."""


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
        "and whether it stands out in a TikTok feed."
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

Return a complete Shark Tank-style evaluation with a full `marketing_plan` (organic + paid + platform mix) as JSON matching the required schema."""


def build_contents(prompt: str, image_bytes: bytes | None, image_mime: str | None) -> list:
    parts: list = [types.Part.from_text(text=prompt)]
    if image_bytes:
        mime = image_mime or "image/jpeg"
        parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime))
    return parts


def is_transient_api_error(exc: genai_errors.APIError) -> bool:
    if exc.code in TRANSIENT_API_CODES:
        return True
    message = (exc.message or "").lower()
    return any(
        phrase in message
        for phrase in ("high demand", "unavailable", "overloaded", "try again later")
    )


def generate_with_retry(client: genai.Client, contents: list) -> genai.types.GenerateContentResponse:
    last_error: genai_errors.APIError | None = None

    for attempt in range(MAX_API_ATTEMPTS):
        try:
            return client.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.6,
                    max_output_tokens=8192,
                    response_mime_type="application/json",
                    response_schema=ProductEvaluationResponse,
                ),
            )
        except genai_errors.APIError as exc:
            last_error = exc
            is_last_attempt = attempt >= MAX_API_ATTEMPTS - 1
            if is_last_attempt or not is_transient_api_error(exc):
                raise AnalysisError(f"Gemini API error ({exc.code}): {exc.message}") from exc

            wait_seconds = RETRY_BACKOFF_SECONDS[attempt]
            st.warning(
                f"Google servers are busy (error {exc.code}). "
                f"Retrying in {wait_seconds} seconds… "
                f"(attempt {attempt + 2} of {MAX_API_ATTEMPTS})"
            )
            time.sleep(wait_seconds)

    if last_error is not None:
        raise AnalysisError(
            f"Gemini API unavailable after {MAX_API_ATTEMPTS} attempts "
            f"(last error {last_error.code}): {last_error.message}"
        ) from last_error
    raise AnalysisError("Gemini API call failed after multiple retries. Please try again shortly.")


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

    client = genai.Client(api_key=api_key.strip())
    contents = build_contents(prompt, image_bytes, image_mime)
    response = generate_with_retry(client, contents)

    raw = (response.text or "").strip()
    if not raw:
        raise AnalysisError("Gemini returned an empty response. Try again.")

    try:
        return ProductEvaluationResponse.model_validate_json(raw)
    except ValidationError:
        try:
            return ProductEvaluationResponse.model_validate(json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as inner:
            raise AnalysisError(
                "The model response did not match the expected schema. Please run the analysis again."
            ) from inner


run_shark_tank_analysis = run_product_evaluation
