"""Crow Metrics evaluation engine — Anthropic Claude only (Haiku S1–S2, Sonnet S3–S6)."""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Callable, TypeVar

import streamlit as st
from pydantic import BaseModel, ValidationError

from ecom_evaluator.anthropic_client import generate_json
from ecom_evaluator.config import (
    CLAUDE_HAIKU_MODEL,
    CLAUDE_MAX_OUTPUT_TOKENS,
    CLAUDE_SONNET_MODEL,
    CROW_SYSTEM_PROMPT,
    MAX_PARSE_ATTEMPTS,
    SECTION_API_DELAY_SECONDS,
)
from ecom_evaluator.economics import (
    compute_all_platform_economics,
    compute_economics_snapshot,
    compute_financial_summary,
    compute_scaling_matrix,
    format_economics_for_verdict,
)
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.llm_normalize import (
    merge_section1_and_section2,
    normalize_competitor_sentiment_payload,
    normalize_financial_verdict_payload,
    normalize_marketing_blueprint_payload,
    normalize_section1_payload,
    normalize_section2_payload,
    normalize_web_intelligence_payload,
)
from ecom_evaluator.llm_utils import extract_json_text
from ecom_evaluator.models import (
    CompetitorSentimentPayload,
    FinancialVerdictPayload,
    FreeCorePayload,
    MarketSearchHit,
    MarketingBlueprintPayload,
    ProductEvaluationResponse,
    WebIntelligencePayload,
)
from ecom_evaluator.plans import PlanTier, get_plan_config
from ecom_evaluator.product_links import ProductLinkInfo, format_product_link_for_prompt, parse_product_url
from ecom_evaluator.scoring import format_scoring_guidance_for_prompt

T = TypeVar("T", bound=BaseModel)

SECTION1_JSON = """
Return ONE flat JSON object with STRING values for all scores (e.g. "72" not 72).
Do NOT include overall_score — Python computes it.

Keys exactly:
"category", "product_type", "main_use", "key_feature",
"weight_class", "fragility", "variants", "shipping_complexity",
"logistics_score", "saturation_score", "marketing_score", "seasonality_score", "brandability_score",
"logistics_note", "saturation_note", "marketing_note", "seasonality_note", "brandability_note",
"one_line_verdict", "confidence_percentage", "product_profile_summary"

Scoring (0-100 strings, higher = better for seller):
- logistics_score: margin + shipping + fragility (30% weight in overall)
- saturation_score: market opportunity (100 = open niche, 0 = saturated)
- marketing_score: viral/paid acquisition potential (20% weight)
- seasonality_score: year-round demand (10% weight)
- brandability_score: brand vs fad durability (15% weight)

one_line_verdict: max 15 words, plain English.
confidence_percentage: string "0"-"100" based on how much input data was provided.
"""

SECTION2_JSON = """
Return ONE flat JSON object.

Keys exactly:
"flags", "would_invest", "invest_reasoning", "red_flag_headline", "red_flag_analysis"

flags: array of 3-6 objects, each with:
- "title": bold punchy title, max 5 words
- "severity": exactly one of "SEVERE", "HIGH", "MEDIUM", "LOW"
- "explanation": two sentences plain English
- "means_for_you": one sentence starting with "What this means for you:"

would_invest: boolean
invest_reasoning: one sentence explaining Yes with conditions or No.

Do NOT pad with weak flags. Only genuine risks supported by the product data.
Do NOT include risk_score — Python computes it from severities.
"""

SECTION1_SYSTEM = f"""You are Crow Metrics analysing a product for Section 1 — Product Profile and Core Metrics.
Generate a structured product profile and five sub-scores only. Python calculates the overall score.

{SECTION1_JSON}"""

SECTION2_SYSTEM = f"""You are a brutally honest ecommerce analyst for Section 2 — Red Flag and Risk Analysis.
Your job is to identify real problems that would cause a dropshipper to lose money.
Do not sugarcoat. Do not add weak flags to fill space.
Only flag genuine risks that would materially affect profitability or scalability.

{SECTION2_JSON}"""

FINANCIAL_VERDICT_JSON = """
Return ONE flat JSON object with STRING values only:
"financial_verdict", "financial_verdict_headline", "cfo_summary",
"financial_conditions", "financial_key_risks", "financial_recommendation"

financial_verdict: exactly "GO", "NO-GO", or "CONDITIONAL GO"
financial_recommendation: one actionable recommendation sentence.
Do NOT recalculate margins — treat Python economics as ground truth.
"""

FINANCIAL_VERDICT_SYSTEM = f"""You are a CFO synthesising Python-computed unit economics into a final GO/NO-GO verdict.
Reference specific dollar amounts. Be decisive.

{FINANCIAL_VERDICT_JSON}"""

MARKETING_BLUEPRINT_JSON = """
Return ONE flat JSON object.

Keys exactly:
"marketing_primary_channel", "scroll_stopping_hook_index", "buyer_persona_hint", "marketing_teaser",
"competitor_ad_angles", "marketing_angles", "marketing_angle_details",
"ad_script_frameworks", "targeting_stack", "influencer_dm_templates", "channel_recommendation_reason"

marketing_angles: EXACTLY 3 DISTINCT angles (name + emotion + hook + why it works — one string each).
ad_script_frameworks: EXACTLY 5 objects with "platform", "hook", "problem", "solution", "social_proof", "cta", "visual_cues", "estimated_length".
targeting_stack: Facebook AND TikTok interests (specific names), demographics, behaviours, lookalike suggestion.
Be specific. Reference the exact product. Scripts ready to film.
"""

MARKETING_BLUEPRINT_SYSTEM = f"""Senior performance media buyer. Use web search for current Meta Ad Library and TikTok Creative Center patterns.
{MARKETING_BLUEPRINT_JSON}"""

WEB_INTEL_JSON = """
Return ONE flat JSON object.

Keys: "web_intelligence_summary", "web_amazon_snapshot", "web_aliexpress_sourcing",
"web_competitor_tracking", "web_sourcing_links", "supplier_recommendations",
"competitor_price_range", "demand_trend", "market_timing_assessment",
"trending_keywords", "live_market_summary"

supplier_recommendations: EXACTLY 3 objects with "name", "url", "price_signal", "moq_signal", "rating_signal".
Only report what you find via web search. Say "Could not verify current data" when uncertain.
trending_keywords: array of 3 strings.
"""

WEB_INTEL_SYSTEM = f"""Competitive intelligence analyst. Use web search for live AliExpress, Amazon, Google Trends, TikTok data.
{WEB_INTEL_JSON}"""

COMPETITOR_SENTIMENT_JSON = """
Return ONE flat JSON object.

Keys: "sentiment_executive_summary", "category_sentiment_score",
"praised_features", "unmet_needs", "sentiment_pain_points", "sentiment_improvement_directives",
"sentiment_shopify_hooks", "supplier_briefing_note", "competitive_opportunity_summary"

Analyse real customer reviews for competing products via web search.
supplier_briefing_note: specific quality requirements for AliExpress supplier.
Every recommendation traceable to review patterns, not generic advice.
"""

COMPETITOR_SENTIMENT_SYSTEM = f"""Senior product strategist analysing competitor reviews via web search.
{COMPETITOR_SENTIMENT_JSON}"""


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
    used_physical_baseline: bool = False,
    used_sales_price_estimate: bool = False,
    product_link: ProductLinkInfo | None = None,
    section1_summary: str = "",
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
        "Product image attached — analyse packaging, materials, variants, visual appeal."
        if has_image
        else "No image — infer cautiously; note visual uncertainty."
    )
    baseline_note = (
        "Physical inputs used lightweight baseline (0.15 kg, 15×10×5 cm)."
        if used_physical_baseline
        else ""
    )
    price_note = (
        f"Selling price estimated at ${sales_price:.2f} (3× purchase cost)."
        if used_sales_price_estimate
        else ""
    )
    link_block = format_product_link_for_prompt(product_link) if product_link else ""
    scoring_guidance = format_scoring_guidance_for_prompt(econ)
    profile_block = f"\n## Section 1 profile\n{section1_summary}\n" if section1_summary else ""

    return f"""## Product
- Name: {product_name}
{link_block}

## Computed economics
- Purchase: ${econ.purchase_price:.2f} | Sell: ${econ.sales_price:.2f}
- Gross margin: ${econ.gross_margin_usd:.2f} ({econ.gross_margin_pct:.1f}%)
- Billable weight: {econ.billable_weight_kg:.3f} kg
- Est. shipping: ${ship_low:.2f}–${ship_high:.2f}
- Contribution after shipping: ${econ.contribution_margin_usd:.2f}
{baseline_note}
{price_note}

{scoring_guidance}

## Dimensions & weight
- {weight_kg:.3f} kg | {length_cm}×{width_cm}×{height_cm} cm

## Description
{description.strip() or "No additional description provided."}

## Visual
{image_note}
{profile_block}"""


def _count_inputs_provided(
    *,
    product_name: str,
    product_url: str,
    purchase_price: float,
    sales_price: float,
    description: str,
    weight_kg: float,
    has_image: bool,
) -> int:
    count = 0
    if product_name.strip():
        count += 1
    if product_url.strip():
        count += 1
    if purchase_price > 0:
        count += 1
    if sales_price > 0:
        count += 1
    if description.strip():
        count += 1
    if weight_kg > 0:
        count += 1
    if has_image:
        count += 1
    return count


def _cache_key(**kwargs: Any) -> str:
    blob = json.dumps(kwargs, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def parse_json_phase(
    raw: str,
    model_class: type[T],
    normalize_fn: Callable[[Any], dict[str, Any]],
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


def run_json_phase(
    *,
    api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    normalize_fn: Callable[[Any], dict[str, Any]],
    phase_label: str,
    max_output_tokens: int,
    temperature: float = 0.35,
    image_bytes: bytes | None = None,
    image_mime: str | None = None,
    enable_web_search: bool = False,
    max_parse_attempts: int = MAX_PARSE_ATTEMPTS,
) -> dict[str, Any]:
    last_error: AnalysisError | None = None
    for attempt in range(max_parse_attempts):
        if attempt > 0:
            st.warning(f"{phase_label} — retrying ({attempt + 1}/{max_parse_attempts})…")
        raw = generate_json(
            api_key=api_key,
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
            cleaned = extract_json_text(raw)
            payload = json.loads(cleaned)
            return normalize_fn(payload)
        except json.JSONDecodeError as exc:
            last_error = AnalysisError(f"{phase_label}: invalid JSON. Try again.")
            if attempt >= max_parse_attempts - 1:
                raise last_error from exc
        except ValueError as err:
            last_error = AnalysisError(f"{phase_label}: incomplete fields ({err}). Try again.")
            if attempt >= max_parse_attempts - 1:
                raise last_error
    raise last_error or AnalysisError(f"{phase_label} failed.")


def run_phase_with_retries(
    *,
    api_key: str,
    model: str,
    system_instruction: str,
    user_prompt: str,
    model_class: type[T],
    normalize_fn: Callable[[Any], dict[str, Any]],
    phase_label: str,
    max_output_tokens: int,
    temperature: float = 0.35,
    image_bytes: bytes | None = None,
    image_mime: str | None = None,
    enable_web_search: bool = False,
    max_parse_attempts: int = MAX_PARSE_ATTEMPTS,
) -> T:
    last_error: AnalysisError | None = None
    for attempt in range(max_parse_attempts):
        if attempt > 0:
            st.warning(f"{phase_label} — retrying ({attempt + 1}/{max_parse_attempts})…")
        raw = generate_json(
            api_key=api_key,
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


def _section_delay() -> None:
    if SECTION_API_DELAY_SECONDS > 0:
        time.sleep(SECTION_API_DELAY_SECONDS)


def _run_section_safe(
    *,
    label: str,
    runner: Callable[[], dict[str, Any]],
    errors: dict[str, str],
) -> dict[str, Any]:
    try:
        return runner()
    except AnalysisError as exc:
        errors[label] = str(exc)
        st.error(f"{label} failed: {exc}")
        return {}
    except Exception as exc:
        errors[label] = str(exc)
        st.error(f"{label} failed unexpectedly: {exc}")
        return {}


def run_product_evaluation(
    *,
    api_key: str = "",
    anthropic_api_key: str = "",
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
    used_physical_baseline: bool = False,
    used_sales_price_estimate: bool = False,
    product_url: str = "",
) -> ProductEvaluationResponse:
    resolved_key = (anthropic_api_key or api_key).strip()
    if not resolved_key:
        raise AnalysisError(
            "Anthropic API key is required. Add ANTHROPIC_API_KEY to Streamlit secrets or .env."
        )

    plan = get_plan_config(tier)
    product_link = parse_product_url(product_url) if product_url.strip() else None
    input_count = _count_inputs_provided(
        product_name=product_name,
        product_url=product_url,
        purchase_price=purchase_price,
        sales_price=sales_price,
        description=description,
        weight_kg=weight_kg,
        has_image=image_bytes is not None,
    )

    cache_id = _cache_key(
        product_name=product_name,
        purchase_price=purchase_price,
        sales_price=sales_price,
        tier=tier.value,
    )
    cache_bucket = st.session_state.setdefault("evaluation_section_cache", {})
    cached = cache_bucket.get(cache_id)

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
        used_physical_baseline=used_physical_baseline,
        used_sales_price_estimate=used_sales_price_estimate,
        product_link=product_link,
    )

    section_errors: dict[str, str] = {}
    updates: dict[str, Any] = {}

    # --- Section 1 ---
    if cached and cached.get("section1"):
        section1_data = cached["section1"]
    else:
        with st.spinner("Section 1 — Product profile & metrics (Claude Haiku)…"):
            section1_data = run_json_phase(
                api_key=resolved_key,
                model=plan.claude_haiku_model,
                system_instruction=SECTION1_SYSTEM,
                user_prompt=f"{context}\n\nReturn Section 1 JSON now.",
                normalize_fn=lambda raw: normalize_section1_payload(raw, input_count=input_count),
                phase_label="Section 1 — Product profile",
                max_output_tokens=plan.core_max_tokens,
                temperature=0.45,
                image_bytes=image_bytes,
                image_mime=image_mime,
            )
        if cache_id not in cache_bucket:
            cache_bucket[cache_id] = {}
        cache_bucket[cache_id]["section1"] = section1_data

    updates.update(section1_data)
    _section_delay()

    section1_summary = json.dumps(
        {
            "category": updates.get("product_category"),
            "type": updates.get("product_type"),
            "overall_score": updates.get("overall_score"),
            "verdict": updates.get("one_line_verdict"),
        },
        indent=2,
    )
    context_with_s1 = build_input_context(
        product_name=product_name,
        purchase_price=purchase_price,
        sales_price=sales_price,
        weight_kg=weight_kg,
        length_cm=length_cm,
        width_cm=width_cm,
        height_cm=height_cm,
        description=description,
        has_image=image_bytes is not None,
        used_physical_baseline=used_physical_baseline,
        used_sales_price_estimate=used_sales_price_estimate,
        product_link=product_link,
        section1_summary=section1_summary,
    )

    # --- Section 2 ---
    if cached and cached.get("section2"):
        section2_data = cached["section2"]
    else:
        with st.spinner("Section 2 — Red flags & risk analysis (Claude Haiku)…"):
            section2_data = run_json_phase(
                api_key=resolved_key,
                model=plan.claude_haiku_model,
                system_instruction=SECTION2_SYSTEM,
                user_prompt=f"{context_with_s1}\n\nReturn Section 2 JSON now.",
                normalize_fn=normalize_section2_payload,
                phase_label="Section 2 — Red flags",
                max_output_tokens=plan.core_max_tokens,
                temperature=0.4,
            )
        cache_bucket[cache_id]["section2"] = section2_data

    updates.update(section2_data)
    result = ProductEvaluationResponse.model_validate(merge_section1_and_section2(section1_data, section2_data))
    _section_delay()

    if plan.runs_financial_verdict:
        def _run_s3() -> dict[str, Any]:
            econ = compute_economics_snapshot(
                purchase_price=purchase_price,
                sales_price=sales_price,
                weight_kg=weight_kg,
                length_cm=length_cm,
                width_cm=width_cm,
                height_cm=height_cm,
            )
            fin = compute_financial_summary(econ)
            matrix = compute_scaling_matrix(econ)
            platform_rows = compute_all_platform_economics(econ)
            economics_block = format_economics_for_verdict(
                econ=econ, fin=fin, matrix=matrix, platform_rows=platform_rows
            )
            with st.spinner("Section 3 — Financial matrix & verdict (Claude Sonnet)…"):
                payload = run_phase_with_retries(
                    api_key=resolved_key,
                    model=plan.claude_sonnet_model,
                    system_instruction=FINANCIAL_VERDICT_SYSTEM,
                    user_prompt=(
                        f"{context_with_s1}\n\n{economics_block}\n\n"
                        f"Overall score: {result.overall_score}/100.\n"
                        "Return financial verdict JSON now."
                    ),
                    model_class=FinancialVerdictPayload,
                    normalize_fn=normalize_financial_verdict_payload,
                    phase_label="Section 3 — Financial verdict",
                    max_output_tokens=plan.premium_max_tokens,
                    temperature=0.25,
                )
            return payload.model_dump()

        s3 = _run_section_safe(label="Section 3", runner=_run_s3, errors=section_errors)
        if s3:
            result = result.model_copy(update=s3)
        _section_delay()

    if plan.runs_marketing_teaser:
        def _run_s4() -> dict[str, Any]:
            with st.spinner("Section 4 — Marketing blueprint (Claude Sonnet + web search)…"):
                payload = run_phase_with_retries(
                    api_key=resolved_key,
                    model=plan.claude_sonnet_model,
                    system_instruction=MARKETING_BLUEPRINT_SYSTEM,
                    user_prompt=(
                        f"{context_with_s1}\n\nOverall score: {result.overall_score}/100.\n"
                        "Return marketing blueprint JSON now."
                    ),
                    model_class=MarketingBlueprintPayload,
                    normalize_fn=normalize_marketing_blueprint_payload,
                    phase_label="Section 4 — Marketing blueprint",
                    max_output_tokens=plan.premium_max_tokens,
                    enable_web_search=True,
                )
            return payload.model_dump()

        s4 = _run_section_safe(label="Section 4", runner=_run_s4, errors=section_errors)
        if s4:
            result = result.model_copy(update=s4)
        _section_delay()

    if plan.runs_web_search:
        def _run_s5() -> dict[str, Any]:
            with st.spinner("Section 5 — Live web intelligence (Claude Sonnet + web search)…"):
                payload = run_phase_with_retries(
                    api_key=resolved_key,
                    model=plan.claude_sonnet_model,
                    system_instruction=WEB_INTEL_SYSTEM,
                    user_prompt=f"{context_with_s1}\n\nReturn web intelligence JSON now.",
                    model_class=WebIntelligencePayload,
                    normalize_fn=normalize_web_intelligence_payload,
                    phase_label="Section 5 — Web intelligence",
                    max_output_tokens=plan.premium_max_tokens,
                    enable_web_search=True,
                )
            return payload.model_dump()

        s5 = _run_section_safe(label="Section 5", runner=_run_s5, errors=section_errors)
        if s5:
            result = result.model_copy(update=s5)
        _section_delay()

        if plan.runs_competitor_sentiment:
            def _run_s6() -> dict[str, Any]:
                with st.spinner("Section 6 — Competitor sentiment (Claude Sonnet + web search)…"):
                    payload = run_phase_with_retries(
                        api_key=resolved_key,
                        model=plan.claude_sonnet_model,
                        system_instruction=COMPETITOR_SENTIMENT_SYSTEM,
                        user_prompt=(
                            f"{context_with_s1}\n\n"
                            f"Overall score: {result.overall_score}. "
                            f"Primary channel: {result.marketing_primary_channel or 'N/A'}.\n"
                            "Return competitor sentiment JSON now."
                        ),
                        model_class=CompetitorSentimentPayload,
                        normalize_fn=normalize_competitor_sentiment_payload,
                        phase_label="Section 6 — Competitor sentiment",
                        max_output_tokens=plan.premium_max_tokens,
                        temperature=0.4,
                        enable_web_search=True,
                    )
                return payload.model_dump()

            s6 = _run_section_safe(label="Section 6", runner=_run_s6, errors=section_errors)
            if s6:
                result = result.model_copy(update=s6)

    if section_errors:
        result = result.model_copy(update={"section_errors": section_errors})

    cache_bucket[cache_id]["full"] = result.model_dump()
    return result


run_shark_tank_analysis = run_product_evaluation
