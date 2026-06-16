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
    normalize_competitor_sentiment_payload,
    normalize_marketing_teaser_payload,
    normalize_web_intelligence_payload,
)
from ecom_evaluator.models import (
    FreeCorePayload,
    MarketSearchHit,
    CompetitorSentimentPayload,
    MarketingTeaserPayload,
    ProductEvaluationResponse,
    WebIntelligencePayload,
)
from ecom_evaluator.plans import PlanTier, get_plan_config
from ecom_evaluator.product_links import ProductLinkInfo, format_product_link_for_prompt
from ecom_evaluator.scoring import format_scoring_guidance_for_prompt
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research

FREE_TIER_JSON = """
Return ONE flat JSON object. Use STRING values for all scores (e.g. "72" not 72).
No markdown fences. Do NOT include overall_score — Python computes it from your five metrics.

Keys exactly:
"product_profile_summary", "physical_weight_assessment", "fragility_assessment",
"variant_complexity", "shipping_complexity",
"metric_logistics_margin", "metric_logistics_margin_note",
"metric_market_saturation", "metric_market_saturation_note",
"metric_marketing_velocity", "metric_marketing_velocity_note",
"metric_seasonality", "metric_seasonality_note",
"metric_brandability", "metric_brandability_note",
"red_flag_headline", "red_flag_analysis", "red_flag_1", "red_flag_2", "red_flag_3"

Scoring rules — output ONLY these five sub-scores (0-100 strings). On EVERY metric, higher = better for the seller:
1. metric_logistics_margin — unit economics after shipping (lightweight + strong markup = high score; thin/negative contribution = low score)
2. metric_market_saturation — MARKET OPPORTUNITY score (100 = wide-open niche, 0 = hyper-saturated red ocean). Do NOT score high when the category is crowded.
3. metric_marketing_velocity — organic viral / paid acquisition viability (easy to demo on TikTok = high; boring commodity = low)
4. metric_brandability — durable brand vs fad (repeat purchases & defensible positioning = high; generic impulse gadget = low)
5. metric_seasonality — year-round demand (100 = steady all year, 0 = holiday-only spike)

Calibration — be brutally honest like Shark Tank live on TV:
- Use the FULL range. Winners can score 85–96. Average products land 40–58. Bad ideas belong at 10–30.
- FORBIDDEN: putting all five metrics in a tight 60–75 band unless every dimension is truly mediocre.
- If you write harsh red flags, the metrics MUST reflect that (typically 2+ metrics below 40).
- Follow the Python "Scoring anchors" section in the user prompt — those override your instincts.
- Metrics must reflect THIS product — do NOT default to 50 or play it safe in the middle.
red_flag_* must be brutal and product-specific (returns, compliance, fragility, sizing, etc.).
"""

FREE_SYSTEM = f"""You are an elite Shark Tank investor and 8-figure e-commerce operator.
Analyze ONLY the user's form inputs and product image — you have NO live web search.

Your default stance is skeptical: most product ideas fail. Score LOW without hesitation when margins,
saturation, differentiation, or compliance are weak. Score HIGH only when the evidence supports it.
Never hedge every metric into a "safe" 60–80 range — that is inaccurate and unhelpful.

If the product name is too vague to identify a specific sellable item (for example a single generic word
like "doodle", "gadget", or "thing" without a listing URL or concrete product type), do NOT invent a
product or speculate. The application should block such inputs before you see them — if you still receive
an ambiguous name, set all five metric_* scores to "5", red_flag_headline to "Input too vague to evaluate",
and explain in red_flag_analysis that a specific product title or supplier URL is required.

Be specific, actionable, and honest — not optimistic by default. Use the computed economics and scoring
anchors in the user message. Do NOT output marketing channel recommendations or ad scripts — those are paid tiers.

{FREE_TIER_JSON}"""

MARKETING_TEASER_JSON = """
Return ONE flat JSON object with STRING values only:
"marketing_primary_channel", "scroll_stopping_hook_index", "buyer_persona_hint", "marketing_teaser"

marketing_primary_channel: TikTok Organic vs Meta Paid (pick one primary recommendation).
scroll_stopping_hook_index: string "1" to "10" for Scroll-Stopping Visual Hook Index.
buyer_persona_hint: Core Buyer Persona mapping in 2-3 sentences.
marketing_teaser: Strategic direction only — NO full ad scripts.
"""

MARKETING_TEASER_SYSTEM = f"""You are a DTC growth strategist.
Based on the product profile and scores already computed, output the Marketing Viability Teaser.

{MARKETING_TEASER_JSON}"""

WEB_INTEL_JSON = """
Return ONE flat JSON object with STRING values only:
"web_intelligence_summary", "web_amazon_snapshot", "web_aliexpress_sourcing",
"web_competitor_tracking", "web_sourcing_links"

Cite real URLs and listing titles from the web research provided. sourcing_links should list actionable supplier/competitor URLs.
"""

WEB_INTEL_SYSTEM = f"""You are a competitive intelligence analyst for e-commerce brands.
Synthesize the live web research into sourcing and competitor intelligence.

{WEB_INTEL_JSON}"""

COMPETITOR_SENTIMENT_JSON = """
Return ONE flat JSON object. Use STRING values for anger_frustration_index (e.g. "78" not 78).

Keys exactly:
"sentiment_executive_summary",
"sentiment_pain_points",
"sentiment_improvement_directives",
"sentiment_shopify_hooks"

sentiment_executive_summary: 2-3 sentences summarizing competitor weakness patterns in THIS niche.

sentiment_pain_points: array of EXACTLY 3 objects, each with:
- "category": one of "Quality / Durability", "Usability / UX", "Expectations vs. Reality" (or a niche-specific variant)
- "negative_trend": data-driven summary of what 1–3★ reviewers complain about
- "anger_frustration_index": string "0" to "100"
- "review_evidence": paraphrased patterns from typical low-star reviews (no fake star counts)

sentiment_improvement_directives: array of EXACTLY 3 objects aligned 1:1 with pain_points, each with:
- "linked_category": must match the corresponding pain point category
- "engineering_directive": concrete manufacturing, materials, QC, packaging, or sourcing fix — not generic marketing advice
- "roi_badge": exactly "High ROI Improvement" or "Low-Cost / High-Value"

sentiment_shopify_hooks: array of 2–3 objects with:
- "angle": short label for the positioning angle
- "copy_block": 1–2 sentences of Shopify-ready copy that explicitly contrasts your improved product vs. competitor failures
"""

COMPETITOR_SENTIMENT_SYSTEM = f"""You are a senior product strategist and manufacturing consultant for DTC brands.
Analyze the specific product niche using web research, category knowledge, and the user's product inputs.

Your job: extract realistic competitor weaknesses from typical 1–3 star review patterns in this category,
then translate each weakness into an exact engineering or sourcing improvement for the user's product.

Rules:
- Be niche-specific — reference materials, components, sizing, instructions, or QC steps relevant to THIS product.
- Do NOT output generic advice like "improve quality" without naming what to change.
- Do NOT invent fake review counts or star averages.
- Each improvement must map directly to a listed pain point.
- Shopify hooks must call out competitor failures and your concrete fixes.

{COMPETITOR_SENTIMENT_JSON}"""

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
    used_physical_baseline: bool = False,
    used_sales_price_estimate: bool = False,
    web_research_text: str = "",
    product_link: ProductLinkInfo | None = None,
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
    baseline_note = (
        "Physical inputs used lightweight-package baseline (0.15 kg, 15×10×5 cm) — note uncertainty in assessments."
        if used_physical_baseline
        else ""
    )
    price_note = (
        f"Selling price was estimated at ${sales_price:.2f} (3× purchase cost) — margin metrics are directional."
        if used_sales_price_estimate
        else ""
    )
    research_block = web_research_text or (
        "## Web research\nNot available for this tier — rely on category knowledge only."
    )
    description_block = description.strip() or "No additional description provided."
    link_block = format_product_link_for_prompt(product_link) if product_link else ""
    scoring_guidance = format_scoring_guidance_for_prompt(econ)

    return f"""## Product
- Name: {product_name}
{link_block}

## Computed economics (use for logistics/margin metrics)
- Purchase: ${econ.purchase_price:.2f} | Sell: ${econ.sales_price:.2f}
- Gross margin: ${econ.gross_margin_usd:.2f} ({econ.gross_margin_pct:.1f}%)
- Billable weight: {econ.billable_weight_kg:.3f} kg | Volume: {econ.volume_dm3:.2f} dm³
- Est. shipping: ${ship_low:.2f}–${ship_high:.2f} ({econ.shipping_tier_label})
- Contribution after shipping: ${econ.contribution_margin_usd:.2f}
{baseline_note}
{price_note}

{scoring_guidance}

## Dimensions & weight
- {weight_kg:.3f} kg | {length_cm}×{width_cm}×{height_cm} cm

## Founder notes
{description_block}

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
    used_physical_baseline: bool = False,
    used_sales_price_estimate: bool = False,
    product_url: str = "",
) -> ProductEvaluationResponse:
    if not api_key.strip():
        raise AnalysisError("API key is required.")

    plan = get_plan_config(tier)
    client = genai.Client(api_key=api_key.strip())

    from ecom_evaluator.product_links import parse_product_url

    product_link = parse_product_url(product_url) if product_url.strip() else None

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

    with st.spinner("Analyzing product profile and risks…"):
        free_core = run_phase_with_retries(
            client,
            model=plan.gemini_model,
            system_instruction=FREE_SYSTEM,
            user_parts=build_user_parts(
                f"{context}\n\n"
                "Score like a Shark Tank investor on live TV — decisive highs and lows, not a safe middle cluster.\n"
                "Return the free-tier JSON now.",
                image_bytes,
                image_mime,
            ),
            model_class=FreeCorePayload,
            normalize_fn=normalize_free_evaluation_payload,
            phase_label="Product evaluation",
            max_output_tokens=plan.core_max_tokens,
            temperature=0.52,
        )

    result = ProductEvaluationResponse.model_validate(free_core.model_dump())

    if plan.runs_marketing_teaser:
        with st.spinner("Building marketing blueprint (advanced AI engine)…"):
            teaser = run_phase_with_retries(
                client,
                model=plan.gemini_model,
                system_instruction=MARKETING_TEASER_SYSTEM,
                user_parts=build_user_parts(
                    f"{context}\n\nOverall score: {result.overall_score}/100.\n"
                    "Return marketing teaser JSON now.",
                    image_bytes,
                    image_mime,
                ),
                model_class=MarketingTeaserPayload,
                normalize_fn=normalize_marketing_teaser_payload,
                phase_label="Marketing teaser",
                max_output_tokens=plan.premium_max_tokens,
            )
        result = result.model_copy(update=teaser.model_dump())

    if plan.runs_web_search:
        hits = web_research or run_web_market_research(
            product_name=product_name,
            description=description,
            max_results=plan.web_search_max_results,
            product_url=product_url,
        )
        web_text = format_web_research_for_prompt(hits)
        with st.spinner("Scanning live market intelligence…"):
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

        if plan.runs_competitor_sentiment:
            with st.spinner("Analyzing competitor review sentiment…"):
                sentiment_block = run_phase_with_retries(
                    client,
                    model=plan.gemini_pro_model or GEMINI_PRO_MODEL,
                    system_instruction=COMPETITOR_SENTIMENT_SYSTEM,
                    user_parts=build_user_parts(
                        f"{context}\n\n{web_text}\n\n"
                        f"Overall score: {result.overall_score}. "
                        f"Primary channel: {result.marketing_primary_channel or 'N/A'}.\n"
                        "Return competitor sentiment JSON now.",
                        image_bytes,
                        image_mime,
                    ),
                    model_class=CompetitorSentimentPayload,
                    normalize_fn=normalize_competitor_sentiment_payload,
                    phase_label="Competitor sentiment",
                    max_output_tokens=plan.premium_max_tokens,
                    temperature=0.4,
                )
            result = result.model_copy(update=sentiment_block.model_dump())

    return result


run_shark_tank_analysis = run_product_evaluation
