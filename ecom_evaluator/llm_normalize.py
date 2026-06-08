"""Coerce lightweight Gemini JSON (mostly strings) before Pydantic validation."""

from __future__ import annotations

from typing import Any

from ecom_evaluator.scoring import compute_overall_score


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _coerce_score(value: Any, *, default: int | None = None) -> int | None:
    if value is None:
        return default
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return max(0, min(100, int(round(value))))
    text = _as_str(value)
    if not text:
        return default
    if "/" in text:
        text = text.split("/")[0].strip()
    text = text.rstrip("%").strip()
    try:
        return max(0, min(100, int(round(float(text)))))
    except ValueError:
        return default


def _coerce_hook_index(value: Any) -> int:
    parsed = _coerce_score(value, default=5)
    return max(1, min(10, parsed or 5))


def _ensure_text(value: Any, fallback: str) -> str:
    text = _as_str(value)
    return text if text else fallback


def normalize_free_evaluation_payload(raw: Any) -> dict[str, Any]:
    """Sections 1–2 only. Overall score is computed in Python — never from the LLM."""
    data = dict(raw) if isinstance(raw, dict) else {}

    logistics = _coerce_score(data.get("metric_logistics_margin"), default=50)
    saturation = _coerce_score(data.get("metric_market_saturation"), default=50)
    velocity = _coerce_score(data.get("metric_marketing_velocity"), default=50)
    brandability = _coerce_score(data.get("metric_brandability"), default=50)
    seasonality = _coerce_score(data.get("metric_seasonality"), default=50)
    logistics = 50 if logistics is None else logistics
    saturation = 50 if saturation is None else saturation
    velocity = 50 if velocity is None else velocity
    brandability = 50 if brandability is None else brandability
    seasonality = 50 if seasonality is None else seasonality
    overall = compute_overall_score(logistics, saturation, velocity, brandability, seasonality)

    return {
        "overall_score": overall,
        "product_profile_summary": _ensure_text(
            data.get("product_profile_summary"),
            "Product profile could not be fully analyzed — re-run with a clearer image and description.",
        ),
        "physical_weight_assessment": _ensure_text(
            data.get("physical_weight_assessment"),
            "Confirm weight and dimensions with your supplier before quoting shipping.",
        ),
        "fragility_assessment": _ensure_text(
            data.get("fragility_assessment"),
            "Assess packaging requirements with a sample unit before scaling.",
        ),
        "variant_complexity": _ensure_text(
            data.get("variant_complexity"),
            "Variant complexity depends on SKU count and packaging differences.",
        ),
        "shipping_complexity": _ensure_text(
            data.get("shipping_complexity"),
            "Shipping complexity should be validated against billable weight and carrier rules.",
        ),
        "metric_logistics_margin": logistics,
        "metric_logistics_margin_note": _ensure_text(
            data.get("metric_logistics_margin_note"),
            "Lightweight, high-markup products score highest on logistics and margin.",
        ),
        "metric_market_saturation": saturation,
        "metric_market_saturation_note": _ensure_text(
            data.get("metric_market_saturation_note"),
            "Estimated from category knowledge — unlock Premium for live competitor data.",
        ),
        "metric_marketing_velocity": velocity,
        "metric_marketing_velocity_note": _ensure_text(
            data.get("metric_marketing_velocity_note"),
            "Organic viral potential vs paid viability based on product visual appeal.",
        ),
        "metric_seasonality": seasonality,
        "metric_seasonality_note": _ensure_text(
            data.get("metric_seasonality_note"),
            "Year-round demand scores higher than holiday-only spikes.",
        ),
        "metric_brandability": brandability,
        "metric_brandability_note": _ensure_text(
            data.get("metric_brandability_note"),
            "Long-term brand potential vs impulse-buy fad risk.",
        ),
        "red_flag_headline": _ensure_text(
            data.get("red_flag_headline"),
            "Key risks to validate before investing",
        ),
        "red_flag_analysis": _ensure_text(
            data.get("red_flag_analysis"),
            "Review return rates, compliance, and margin compression before scaling.",
        ),
        "red_flag_1": _ensure_text(data.get("red_flag_1"), "Margin may not survive paid acquisition at scale."),
        "red_flag_2": _ensure_text(data.get("red_flag_2"), "Category competition could force price wars."),
        "red_flag_3": _ensure_text(data.get("red_flag_3"), "Shipping or sizing surprises can erode contribution margin."),
    }


def normalize_marketing_teaser_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    return {
        "marketing_primary_channel": _ensure_text(
            data.get("marketing_primary_channel"),
            "TikTok Organic",
        ),
        "scroll_stopping_hook_index": _coerce_hook_index(data.get("scroll_stopping_hook_index")),
        "buyer_persona_hint": _ensure_text(
            data.get("buyer_persona_hint"),
            "Problem-aware buyer seeking a practical solution they can show off or use daily.",
        ),
        "marketing_teaser": _ensure_text(
            data.get("marketing_teaser"),
            "Lead with visual proof and a clear before/after — full scripts unlock on Pro.",
        ),
    }


def normalize_web_intelligence_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    return {
        "web_intelligence_summary": _ensure_text(data.get("web_intelligence_summary"), "Summary unavailable."),
        "web_amazon_snapshot": _ensure_text(data.get("web_amazon_snapshot"), "No Amazon data captured."),
        "web_aliexpress_sourcing": _ensure_text(data.get("web_aliexpress_sourcing"), "No AliExpress sourcing data."),
        "web_competitor_tracking": _ensure_text(data.get("web_competitor_tracking"), "No competitor tracking data."),
        "web_sourcing_links": _ensure_text(data.get("web_sourcing_links"), "No sourcing links found."),
    }


def normalize_marketing_deep_dive_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    return {
        "marketing_ad_scripts": _ensure_text(data.get("marketing_ad_scripts"), "Scripts unavailable."),
        "marketing_targeting_blueprint": _ensure_text(
            data.get("marketing_targeting_blueprint"), "Targeting blueprint unavailable."
        ),
        "marketing_influencer_templates": _ensure_text(
            data.get("marketing_influencer_templates"), "Influencer templates unavailable."
        ),
        "marketing_positioning_matrix": _ensure_text(
            data.get("marketing_positioning_matrix"), "Positioning matrix unavailable."
        ),
    }
