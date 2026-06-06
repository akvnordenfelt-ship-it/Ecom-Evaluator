"""Gemini evaluation pipeline — free tier (inputs + image only), premium web intel, pro marketing."""

from __future__ import annotations

import json
import time
from typing import TypeVar

import streamlit as st
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel, ValidationError

from ecom_evaluator.config import (
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_MODEL,
    GEMINI_PRO_MODEL,
    MAX_API_ATTEMPTS,
    MAX_PARSE_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    TRANSIENT_API_CODES,
)
from ecom_evaluator.economics import compute_economics_snapshot
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_normalize import (
    normalize_free_evaluation_payload,
    normalize_marketing_deep_dive_payload,
    normalize_web_intelligence_payload,
)
from ecom_evaluator.models import (
    MarketSearchHit,
    MarketingDeepDivePayload,
    ProductEvaluationResponse,
    WebIntelligencePayload,
)
from ecom_evaluator.plans import PlanTier, get_plan_config
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research

FREE_TIER_JSON = """
Return ONE flat JSON object. Use STRING values for all scores (e.g. "72" not 72).
No markdown fences. Keys exactly:

"overall_score", "product_profile_summary", "physical_weight_assessment", "fragility_assessment",
"variant_complexity", "shipping_complexity",
"metric_market_saturation", "metric_market_saturation_note",
"metric_marketing_velocity", "metric_marketing_velocity_note",
"metric_logistics_margin", "metric_logistics_margin_note",
"metric_seasonality", "metric_seasonality_note",
"metric_brandability", "metric_brandability_note",
"red_flag_headline", "red_flag_analysis", "red_flag_1", "red_flag_2", "red_flag_3",
"marketing_primary_channel", "scroll_stopping_hook_index", "buyer_persona_hint", "marketing_teaser"

Scoring rules:
- overall_score ≈ average of the five metric_* scores (within 15 points).
- Metrics must reflect THIS product — do NOT default all scores to 50.
- metric_logistics_margin: high for lightweight + high markup (e.g. $0.10 cost → $10 sell).
- scroll_stopping_hook_index: string "1" to "10".
- red_flag_* must be brutal and product-specific (returns, compliance, fragility, sizing, etc.).
- marketing_teaser: strategic direction only — NO full ad scripts.
"""

FREE_SYSTEM = f"""You are an elite Shark Tank investor and 8-figure e-commerce operator.
Analyze ONLY the user's form inputs and product image — you have NO live web search.

Your job: show the CEILING, not the floor. Free-tier output must feel premium, specific, and actionable.
Use the computed economics numbers in the prompt for logistics/margin reasoning.

{FREE_TIER_JSON}"""

WEB_INTEL_JSON = """
Return ONE flat JSON object with STRING values only:
"web_intelligence_summary", "web_amazon_snapshot", "web_aliexpress_sourcing",
"web_competitor_tracking", "web_sourcing_links"

Cite real URLs and listing titles from the web research provided. sourcing_links should list actionable supplier/competitor URLs.
"""

WEB_INTEL_SYSTEM = f"""You are a competitive intelligence analyst for e-commerce brands.
Synthesize the live web research into sourcing and competitor intelligence.

{WEB_INTEL_JSON}"""

MARKETING_DEEP_JSON = """
Return ONE flat JSON object with STRING values only (use markdown inside strings for formatting):
"marketing_ad_scripts", "marketing_targeting_blueprint", "marketing_influencer_templates", "marketing_positioning_matrix"

marketing_ad_scripts: exactly 5 complete TikTok/Reels scripts with visual cues.
marketing_targeting_blueprint: exact Facebook & TikTok interest stacks and demographics.
marketing_influencer_templates: 3 copy-paste DM templates.
marketing_positioning_matrix: 3 distinct angles vs competitors.
"""

MARKETING_DEEP_SYSTEM = f"""You are a $100M DTC growth lead (Claude Opus-level depth).
Build the ultimate marketing blueprint for this specific product.

{MARKETING_DEEP_JSON}"""

T = TypeVar("T", bound=BaseModel)


def build_input_context(
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
    web_research_text: str = "",
) -> str:
    econ = compute_economics_snapshot(
        purchase_price=purchase_price,
        sales_price=sales_price,
        weight_kg=weight_kg,
        length_cm=length_cm,
        width_cm=width_cm,
        height_cm=height_cm,
    )
    ship_low, ship_high = econ.shipping_band_usd
    image_note = (
        "Product image attached — analyze packaging, materials, variants visible, and creative potential."
        if has_image
        else "No image — infer cautiously from description; note visual uncertainty."
    )
    research_block = web_research_text or (
        "## Web research\nNot available for this tier — rely on category knowledge only."
    )

    return f"""## Product
- Name: {product_name}

## Computed economics (use for logistics/margin metrics)
- Purchase: ${econ.purchase_price:.2f} | Sell: ${econ.sales_price:.2f}
- Gross margin: ${econ.gross_margin_usd:.2f} ({econ.gross_margin_pct:.1f}%)
- Billable weight: {econ.billable_weight_kg:.3f} kg | Volume: {econ.volume_dm3:.2f} dm³
- Est. shipping: ${ship_low:.2f}–${ship_high:.2f} ({econ.shipping_tier_label})
- Contribution after shipping: ${econ.contribution_margin_usd:.2f}

## Dimensions & weight
- {weight_kg:.3f} kg | {length_cm}×{width_cm}×{height_cm} cm

## Founder notes
{description}

## Visual
{image_note}

{research_block}"""


def build_user_parts(
    prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
) -> list[types.Part]:
    parts: list[types.Part] = [types.Part.from_text(text=prompt)]
    if image_bytes:
        parts.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime or "image/jpeg"))
    return parts


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


def api_error_message(exc: Exception) -> str:
    if isinstance(exc, genai_errors.APIError):
        return f"Gemini API error ({getattr(exc, 'code', 'unknown')}): {exc}"
    return f"Gemini API error: {exc}"


def generate_json(
    client: genai.Client,
    *,
    model: str,
    system_instruction: str,
    user_parts: list[types.Part],
    max_output_tokens: int,
    temperature: float = 0.35,
) -> str:
    last_error: Exception | None = None
    for attempt in range(MAX_API_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[types.Content(role="user", parts=user_parts)],
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )
            content = (response.text or "").strip()
            if not content:
                raise AnalysisError("Gemini returned an empty response. Try again.")
            return content
        except AnalysisError:
            raise
        except Exception as exc:
            last_error = exc
            if attempt >= MAX_API_ATTEMPTS - 1 or not is_transient_api_error(exc):
                raise AnalysisError(api_error_message(exc)) from exc
            wait = RETRY_BACKOFF_SECONDS[attempt]
            st.warning(f"Gemini busy — retrying in {wait}s…")
            time.sleep(wait)
    raise AnalysisError(f"Gemini unavailable after {MAX_API_ATTEMPTS} attempts: {last_error}")


def parse_json_phase(
    raw: str,
    model_class: type[T],
    normalize_fn,
    *,
    phase_label: str,
) -> T:
    cleaned = extract_json_text(raw)
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AnalysisError(f"{phase_label}: invalid JSON. Try again.") from exc
    try:
        normalized = normalize_fn(payload)
        return model_class.model_validate(normalized)
    except ValueError as err:
        raise AnalysisError(f"{phase_label}: incomplete fields ({err}). Try again.") from err
    except ValidationError as err:
        loc = str(err.errors()[0]["loc"]) if err.errors() else "unknown"
        raise AnalysisError(f"{phase_label}: validation failed near {loc}. Try again.") from err


def run_phase_with_retries(
    client: genai.Client,
    *,
    model: str,
    system_instruction: str,
    user_parts: list[types.Part],
    model_class: type[T],
    normalize_fn,
    phase_label: str,
    max_output_tokens: int,
    temperature: float = 0.35,
) -> T:
    last_error: AnalysisError | None = None
    for attempt in range(MAX_PARSE_ATTEMPTS):
        if attempt > 0:
            st.warning(f"{phase_label} — retrying ({attempt + 1}/{MAX_PARSE_ATTEMPTS})…")
        raw = generate_json(
            client,
            model=model,
            system_instruction=system_instruction,
            user_parts=user_parts,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        try:
            return parse_json_phase(raw, model_class, normalize_fn, phase_label=phase_label)
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
    tier: PlanTier = PlanTier.FREE,
) -> ProductEvaluationResponse:
    if not api_key.strip():
        raise AnalysisError("API key is required.")

    plan = get_plan_config(tier)
    client = genai.Client(api_key=api_key.strip())
    context = build_input_context(
        product_name=product_name,
        purchase_price=purchase_price,
        sales_price=sales_price,
        weight_kg=weight_kg,
        length_cm=length_cm,
        width_cm=width_cm,
        height_cm=height_cm,
        description=description,
        has_image=image_bytes is not None,
    )

    with st.spinner("Analyzing product profile, risks, and marketing fit (Gemini 2.5 Flash)…"):
        free_core = run_phase_with_retries(
            client,
            model=plan.gemini_model,
            system_instruction=FREE_SYSTEM,
            user_parts=build_user_parts(f"{context}\n\nReturn the free-tier JSON now.", image_bytes, image_mime),
            model_class=ProductEvaluationResponse,
            normalize_fn=normalize_free_evaluation_payload,
            phase_label="Product evaluation",
            max_output_tokens=plan.core_max_tokens,
        )

    result = free_core

    if plan.runs_web_search:
        hits = web_research or run_web_market_research(
            product_name=product_name,
            description=description,
            max_results=plan.web_search_max_results,
        )
        web_text = format_web_research_for_prompt(hits)
        with st.spinner("Running live web-intelligence search (Premium)…"):
            web_block = run_phase_with_retries(
                client,
                model=plan.gemini_model,
                system_instruction=WEB_INTEL_SYSTEM,
                user_parts=build_user_parts(
                    f"{context}\n\n{web_text}\n\nReturn web intelligence JSON now.",
                    image_bytes,
                    image_mime,
                ),
                model_class=WebIntelligencePayload,
                normalize_fn=normalize_web_intelligence_payload,
                phase_label="Web intelligence",
                max_output_tokens=plan.premium_max_tokens,
            )
        result = result.model_copy(update=web_block.model_dump())

        if plan.runs_marketing_deep_dive:
            with st.spinner("Building Ultimate Marketing Blueprint (Gemini 2.5 Pro)…"):
                marketing_block = run_phase_with_retries(
                    client,
                    model=plan.gemini_pro_model or GEMINI_PRO_MODEL,
                    system_instruction=MARKETING_DEEP_SYSTEM,
                    user_parts=build_user_parts(
                        f"{context}\n\n{web_text}\n\n"
                        f"Overall score: {result.overall_score}. Channel: {result.marketing_primary_channel}.\n"
                        "Return marketing deep-dive JSON now.",
                        image_bytes,
                        image_mime,
                    ),
                    model_class=MarketingDeepDivePayload,
                    normalize_fn=normalize_marketing_deep_dive_payload,
                    phase_label="Marketing deep-dive",
                    max_output_tokens=plan.premium_max_tokens,
                    temperature=0.45,
                )
            result = result.model_copy(update=marketing_block.model_dump())

    return result


run_shark_tank_analysis = run_product_evaluation
