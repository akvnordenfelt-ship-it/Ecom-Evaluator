"""Gemini 2.5 Flash product evaluation — JSON output with score reconciliation."""

from __future__ import annotations

import json
import time
from typing import Any, TypeVar

import streamlit as st
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel, ValidationError

from ecom_evaluator.config import (
    GEMINI_MAX_OUTPUT_TOKENS,
    GEMINI_MODEL,
    MAX_API_ATTEMPTS,
    MAX_PARSE_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    TRANSIENT_API_CODES,
)
from ecom_evaluator.economics import compute_economics_snapshot
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_normalize import normalize_core_payload, normalize_marketing_payload
from ecom_evaluator.models import (
    MarketSearchHit,
    MarketingPhaseResponse,
    ProductCoreResponse,
    ProductEvaluationResponse,
)
from ecom_evaluator.plans import PlanTier, get_plan_config, includes_premium_sections
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research

ENUM_RULES = """
Use EXACT enum strings:
- competitor_count_signal: Few | Moderate | Many | Unknown  (NOT "Medium")
- demand_estimate.level: Low | Medium | High | Unknown
- market_saturation.level: Low | Medium | High
- unit_economics.viability: Strong | Marginal | Weak
- roi_potential / roi_outlook: Low | Medium | High
- organic_vs_paid: Organic-first | Paid-first | Balanced
"""

JSON_SHAPE = """
Return ONE JSON object matching this shape exactly:
{
  "final_score": 42,
  "investment_headline": "one punchy sentence",
  "short_term_potential": {"score": 35, "motivation": "2-3 sentences with evidence"},
  "long_term_stability": {"score": 40, "motivation": "2-3 sentences"},
  "scalability": {"score": 50, "motivation": "2-3 sentences"},
  "marketing_suitability": {"score": 45, "motivation": "2-3 sentences"},
  "market_research": { ... },
  "market_saturation": {"level": "High", "motivation": "2-3 sentences"},
  "estimated_shipping_category": "string",
  "unit_economics": {
    "viability": "Weak",
    "margin_verdict": "2-3 sentences using the computed margin numbers provided",
    "shipping_impact": "2-3 sentences using billable weight",
    "pricing_vs_market": "2-3 sentences vs observed price range",
    "break_even_guidance": "2-3 sentences",
    "max_affordable_cac": "e.g. $4-6 per order"
  },
  "marketing_fit_preview": "2-3 sentences",
  "top_risks": ["risk 1", "risk 2"],
  "top_opportunities": ["opp 1", "opp 2"],
  "next_steps": ["step 1", "step 2", "step 3"]
}

CRITICAL scoring rules:
- Each dimension MUST be an object with integer "score" (0-100) and string "motivation".
- NEVER return a bare integer for short_term_potential, long_term_stability, scalability, or marketing_suitability.
- Dimension scores must differ when the evidence differs — do NOT default every score to 50.
- final_score must be close to the average of the four dimension scores (within ~10 points).
"""

CORE_SYSTEM_INSTRUCTION = f"""You are ruthless Shark Tank investors plus senior e-commerce operators.
Evaluate the product using the form data, computed economics, AND live web research.

Respond with valid JSON only. No markdown fences.

Quality bar:
- investment_headline: one punchy go/no-go sentence.
- market_research.executive_summary: 4-6 sentences with evidence from search results.
- Each channel landscape (Amazon, AliExpress, independent stores): 2-4 sentences; never empty.
- unit_economics: use the COMPUTED MARGIN and SHIPPING numbers from the prompt — be specific with dollars.
- top_risks / top_opportunities / next_steps: product-specific, not generic e-commerce platitudes.

{ENUM_RULES}

{JSON_SHAPE}"""

MARKETING_SYSTEM_INSTRUCTION = f"""You are a performance marketing strategist for e-commerce brands.
Build a detailed marketing playbook grounded in the core evaluation and web research provided.

Respond with ONE valid JSON object only. No markdown fences.

JSON keys: marketing_plan, go_to_market_strategy.

{ENUM_RULES}"""

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
    econ = compute_economics_snapshot(
        purchase_price=purchase_price,
        sales_price=sales_price,
        weight_kg=weight_kg,
        length_cm=length_cm,
        width_cm=width_cm,
        height_cm=height_cm,
    )
    logistics = logistics_summary(weight_kg, length_cm, width_cm, height_cm)
    image_note = (
        "Product image attached — assess packaging, quality, and feed-stopping visual appeal."
        if has_image
        else "No image — note uncertainty on visual/creative angles."
    )
    ship_low, ship_high = econ.shipping_band_usd

    return f"""## Product
- Name: {product_name}

## Computed unit economics (USE THESE NUMBERS in unit_economics)
- Purchase cost: ${econ.purchase_price:.2f}
- Intended sell price: ${econ.sales_price:.2f}
- Gross margin: ${econ.gross_margin_usd:.2f} ({econ.gross_margin_pct:.1f}% of sell price)
- Est. shipping band: ${ship_low:.2f}–${ship_high:.2f} ({econ.shipping_tier_label})
- Contribution margin after mid-range shipping: ${econ.contribution_margin_usd:.2f} ({econ.contribution_margin_pct:.1f}%)
- Max affordable CAC @ 30% of gross margin: ${econ.max_cac_30pct_margin:.2f}
- Max affordable CAC @ 20% of gross margin: ${econ.max_cac_20pct_margin:.2f}

## Logistics
- Weight: {weight_kg:.3f} kg | Dims: {length_cm}×{width_cm}×{height_cm} cm
- Volume: {logistics['volume_dm3']:.2f} dm³ | Dim weight: {logistics['dimensional_weight_kg']:.3f} kg | Billable: {logistics['billable_weight_kg']:.3f} kg

## Founder notes
{description}

## Visual
{image_note}

{web_research_text}"""


def build_core_user_prompt(context: str) -> str:
    return f"{context}\n\nReturn the evaluation JSON now."


def build_marketing_user_prompt(context: str, core: ProductCoreResponse) -> str:
    mr = core.market_research
    return f"""{context}

## Core evaluation (already completed)
- Final score: {core.final_score}/100
- Headline: {core.investment_headline}
- Saturation: {core.market_saturation.level} — {core.market_saturation.motivation}
- Economics viability: {core.unit_economics.viability}
- Research summary: {mr.executive_summary}

Return marketing_plan and go_to_market_strategy JSON only."""


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
    return any(
        phrase in message
        for phrase in ("rate limit", "overloaded", "try again", "temporarily unavailable", "503", "429")
    )


def api_error_message(exc: Exception) -> str:
    if isinstance(exc, genai_errors.APIError):
        return f"Gemini API error ({getattr(exc, 'code', 'unknown')}): {exc}"
    return f"Gemini API error: {exc}"


def build_user_parts(
    prompt: str,
    image_bytes: bytes | None,
    image_mime: str | None,
) -> list[types.Part]:
    parts: list[types.Part] = [types.Part.from_text(text=prompt)]
    if image_bytes:
        parts.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_mime or "image/jpeg",
            )
        )
    return parts


def generate_with_retry(
    client: genai.Client,
    *,
    model: str,
    system_instruction: str,
    user_parts: list[types.Part],
    max_output_tokens: int,
    temperature: float,
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
            wait_seconds = RETRY_BACKOFF_SECONDS[attempt]
            st.warning(f"Gemini busy — retrying in {wait_seconds}s…")
            time.sleep(wait_seconds)
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
        raise AnalysisError(
            f"{phase_label}: model returned incomplete scores or fields ({err}). Try again."
        ) from err
    except ValidationError as err:
        detail = str(err.errors()[0]["loc"]) if err.errors() else "unknown field"
        raise AnalysisError(
            f"{phase_label}: incomplete report near {detail}. "
            "The model did not generate enough detail — try again."
        ) from err


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
    temperature: float,
) -> T:
    last_error: AnalysisError | None = None
    for attempt in range(MAX_PARSE_ATTEMPTS):
        if attempt > 0:
            st.warning(f"{phase_label} incomplete — retrying ({attempt + 1}/{MAX_PARSE_ATTEMPTS})…")
        raw = generate_with_retry(
            client,
            model=model,
            system_instruction=system_instruction,
            user_parts=user_parts,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        )
        try:
            return parse_json_phase(
                raw,
                model_class,
                normalize_fn,
                phase_label=phase_label,
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
    tier: PlanTier = PlanTier.FREE,
) -> ProductEvaluationResponse:
    if not api_key.strip():
        raise AnalysisError("API key is required.")

    plan = get_plan_config(tier)
    model = plan.gemini_model or GEMINI_MODEL

    research_hits = (
        web_research
        if web_research is not None
        else run_web_market_research(
            product_name=product_name,
            description=description,
            max_results=plan.web_search_max_results,
        )
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

    client = genai.Client(api_key=api_key.strip())
    temperature = 0.35 if tier == PlanTier.FREE else 0.45

    with st.spinner(
        f"{'Phase 1/2 — ' if includes_premium_sections(tier) else ''}"
        "Analyzing market, economics, and investment verdict…"
    ):
        core = run_phase_with_retries(
            client,
            model=model,
            system_instruction=CORE_SYSTEM_INSTRUCTION,
            user_parts=build_user_parts(build_core_user_prompt(context), image_bytes, image_mime),
            model_class=ProductCoreResponse,
            normalize_fn=normalize_core_payload,
            phase_label="Product evaluation",
            max_output_tokens=plan.core_max_tokens,
            temperature=temperature,
        )

    if not includes_premium_sections(tier):
        return ProductEvaluationResponse(
            **core.model_dump(),
            marketing_plan=None,
            go_to_market_strategy=None,
        )

    with st.spinner("Phase 2/2 — Marketing playbook and launch strategy…"):
        marketing = run_phase_with_retries(
            client,
            model=model,
            system_instruction=MARKETING_SYSTEM_INSTRUCTION,
            user_parts=build_user_parts(build_marketing_user_prompt(context, core), None, None),
            model_class=MarketingPhaseResponse,
            normalize_fn=normalize_marketing_payload,
            phase_label="Marketing plan",
            max_output_tokens=plan.marketing_max_tokens,
            temperature=temperature,
        )

    return ProductEvaluationResponse(
        **core.model_dump(),
        marketing_plan=marketing.marketing_plan,
        go_to_market_strategy=marketing.go_to_market_strategy,
    )


run_shark_tank_analysis = run_product_evaluation
