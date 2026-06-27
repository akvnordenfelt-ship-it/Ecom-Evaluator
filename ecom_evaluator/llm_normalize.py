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
            "Market opportunity estimated from category knowledge — lower scores mean heavier crowding.",
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
            "Lead with visual proof and a clear before/after — Premium unlocks the full marketing blueprint.",
        ),
    }


def _normalize_string_list(raw: Any, *, count: int, fallback_prefix: str) -> list[str]:
    items = raw if isinstance(raw, list) else []
    normalized: list[str] = []
    for index in range(count):
        item = items[index] if index < len(items) else ""
        normalized.append(_ensure_text(item, f"{fallback_prefix} {index + 1}"))
    return normalized


def _normalize_ad_scripts(raw: Any) -> list[dict[str, str]]:
    defaults = [
        {
            "platform": "TikTok",
            "hook": "POV: you finally found the version that actually works",
            "body": "Show the problem in 2 seconds, demo the fix in 5, reveal price anchor vs competitors.",
            "cta": "Link in bio — 48h launch discount",
        },
        {
            "platform": "Instagram Reels",
            "hook": "Stop scrolling if [pain point] ruins your day",
            "body": "Before/after split screen with text overlays; social proof sticker.",
            "cta": "Shop now — free returns",
        },
        {
            "platform": "TikTok",
            "hook": "I tested 5 Amazon versions so you don't have to",
            "body": "Side-by-side durability test; call out competitor failure modes.",
            "cta": "Comment SEND for the link",
        },
        {
            "platform": "Meta Feed",
            "hook": "The [category] everyone on my FYP is gatekeeping",
            "body": "UGC selfie + product in use; mention specific improvement vs reviews.",
            "cta": "Learn more",
        },
        {
            "platform": "TikTok",
            "hook": "3 reasons this beats the viral version",
            "body": "Fast cuts: material, sizing, warranty — each tied to a review complaint.",
            "cta": "Tap to shop",
        },
    ]
    items = raw if isinstance(raw, list) else []
    normalized: list[dict[str, str]] = []
    for index in range(5):
        item = items[index] if index < len(items) and isinstance(items[index], dict) else {}
        fallback = defaults[index]
        normalized.append(
            {
                "platform": _ensure_text(item.get("platform"), fallback["platform"]),
                "hook": _ensure_text(item.get("hook"), fallback["hook"]),
                "body": _ensure_text(item.get("body"), fallback["body"]),
                "cta": _ensure_text(item.get("cta"), fallback["cta"]),
            }
        )
    return normalized


def normalize_marketing_blueprint_payload(raw: Any) -> dict[str, Any]:
    base = normalize_marketing_teaser_payload(raw)
    data = dict(raw) if isinstance(raw, dict) else {}
    base.update(
        {
            "competitor_ad_angles": _normalize_string_list(
                data.get("competitor_ad_angles"),
                count=3,
                fallback_prefix="Competitor angle",
            ),
            "marketing_angles": _normalize_string_list(
                data.get("marketing_angles"),
                count=3,
                fallback_prefix="Fresh angle",
            ),
            "ad_script_frameworks": _normalize_ad_scripts(data.get("ad_script_frameworks")),
            "targeting_stack": _ensure_text(
                data.get("targeting_stack"),
                "Meta: interest stacks around the core use case + lookalike 1–3% from add-to-cart. "
                "TikTok: broad + creative-led, age 22–44, exclude purchasers 30d.",
            ),
            "influencer_dm_templates": _normalize_string_list(
                data.get("influencer_dm_templates"),
                count=3,
                fallback_prefix="DM template",
            ),
        }
    )
    return base


def normalize_financial_verdict_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    verdict = _ensure_text(data.get("financial_verdict"), "CONDITIONAL GO").upper()
    if verdict not in {"GO", "NO-GO", "CONDITIONAL GO"}:
        verdict = "CONDITIONAL GO"
    conditions = _normalize_string_list(
        data.get("financial_conditions"),
        count=3,
        fallback_prefix="Condition",
    )
    risks = _normalize_string_list(
        data.get("financial_key_risks"),
        count=3,
        fallback_prefix="Risk",
    )
    return {
        "financial_verdict": verdict,
        "financial_verdict_headline": _ensure_text(
            data.get("financial_verdict_headline"),
            "Margins workable only if acquisition stays below break-even CPA",
        ),
        "cfo_summary": _ensure_text(
            data.get("cfo_summary"),
            "Unit economics require disciplined paid spend and confirmed supplier COGS before scaling.",
        ),
        "financial_conditions": conditions[:5],
        "financial_key_risks": risks[:5],
    }


def _normalize_suppliers(raw: Any) -> list[dict[str, str]]:
    defaults = [
        {
            "name": "AliExpress top-rated listing",
            "url": "https://www.aliexpress.com",
            "price_signal": "Lowest MOQ tier — verify sample quality",
            "moq_signal": "1–50 units typical",
            "rating_signal": "4.5+ stars with 500+ orders",
        },
        {
            "name": "1688 / domestic supplier cluster",
            "url": "https://www.1688.com",
            "price_signal": "15–30% below retail COGS at volume",
            "moq_signal": "100+ units for best pricing",
            "rating_signal": "Factory audit recommended",
        },
        {
            "name": "Amazon competitor reference SKU",
            "url": "https://www.amazon.com",
            "price_signal": "Retail anchor for positioning",
            "moq_signal": "N/A — benchmark only",
            "rating_signal": "Check BSR and review velocity",
        },
    ]
    items = raw if isinstance(raw, list) else []
    normalized: list[dict[str, str]] = []
    for index in range(3):
        item = items[index] if index < len(items) and isinstance(items[index], dict) else {}
        fallback = defaults[index]
        normalized.append(
            {
                "name": _ensure_text(item.get("name"), fallback["name"]),
                "url": _ensure_text(item.get("url"), fallback["url"]),
                "price_signal": _ensure_text(item.get("price_signal"), fallback["price_signal"]),
                "moq_signal": _ensure_text(item.get("moq_signal"), fallback["moq_signal"]),
                "rating_signal": _ensure_text(item.get("rating_signal"), fallback["rating_signal"]),
            }
        )
    return normalized[:3]


def normalize_web_intelligence_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    trend = _ensure_text(data.get("demand_trend"), "stable").lower()
    if trend not in {"rising", "stable", "declining"}:
        trend = "stable"
    return {
        "web_intelligence_summary": _ensure_text(data.get("web_intelligence_summary"), "Summary unavailable."),
        "web_amazon_snapshot": _ensure_text(data.get("web_amazon_snapshot"), "No Amazon data captured."),
        "web_aliexpress_sourcing": _ensure_text(data.get("web_aliexpress_sourcing"), "No AliExpress sourcing data."),
        "web_competitor_tracking": _ensure_text(data.get("web_competitor_tracking"), "No competitor tracking data."),
        "web_sourcing_links": _ensure_text(data.get("web_sourcing_links"), "No sourcing links found."),
        "supplier_recommendations": _normalize_suppliers(data.get("supplier_recommendations")),
        "competitor_price_range": _ensure_text(data.get("competitor_price_range"), "Price range unavailable."),
        "demand_trend": trend,
        "market_timing_assessment": _ensure_text(
            data.get("market_timing_assessment"),
            "Validate demand with a small test batch before committing inventory.",
        ),
    }


def _normalize_pain_points(raw_points: Any) -> list[dict[str, Any]]:
    defaults = [
        {
            "category": "Quality / Durability",
            "negative_trend": "Units fail under normal use within weeks of purchase.",
            "anger_frustration_index": 78,
            "review_evidence": "Repeated 1–3★ mentions of breakage, cheap materials, or loose joints.",
        },
        {
            "category": "Usability / UX",
            "negative_trend": "Setup or daily use is confusing relative to competitor listings.",
            "anger_frustration_index": 71,
            "review_evidence": "Buyers cite unclear instructions, poor ergonomics, or missing accessories.",
        },
        {
            "category": "Expectations vs. Reality",
            "negative_trend": "Listing photos overpromise size, finish, or performance.",
            "anger_frustration_index": 84,
            "review_evidence": "Reviews compare received product unfavorably to ads and hero images.",
        },
    ]
    points = raw_points if isinstance(raw_points, list) else []
    normalized: list[dict[str, Any]] = []
    for index in range(3):
        item = points[index] if index < len(points) and isinstance(points[index], dict) else {}
        fallback = defaults[index]
        anger = _coerce_score(item.get("anger_frustration_index"), default=fallback["anger_frustration_index"])
        normalized.append(
            {
                "category": _ensure_text(item.get("category"), fallback["category"]),
                "negative_trend": _ensure_text(item.get("negative_trend"), fallback["negative_trend"]),
                "anger_frustration_index": 50 if anger is None else anger,
                "review_evidence": _ensure_text(item.get("review_evidence"), fallback["review_evidence"]),
            }
        )
    return normalized


def _normalize_improvements(raw_items: Any, pain_points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    defaults = [
        "Reinforce the highest-stress component with a denser ABS or nylon blend and add a pre-shipment torque check.",
        "Redesign packaging with numbered setup steps and a QR-linked 60-second demo video.",
        "Align hero photography with a scale reference and add a comparison chart to the PDP above the fold.",
    ]
    badges = ["High ROI Improvement", "Low-Cost / High-Value", "High ROI Improvement"]
    items = raw_items if isinstance(raw_items, list) else []
    normalized: list[dict[str, Any]] = []
    for index in range(3):
        item = items[index] if index < len(items) and isinstance(items[index], dict) else {}
        badge = _ensure_text(item.get("roi_badge"), badges[index])
        if badge not in {"High ROI Improvement", "Low-Cost / High-Value"}:
            badge = badges[index]
        normalized.append(
            {
                "linked_category": _ensure_text(
                    item.get("linked_category"),
                    pain_points[index]["category"],
                ),
                "engineering_directive": _ensure_text(item.get("engineering_directive"), defaults[index]),
                "roi_badge": badge,
            }
        )
    return normalized


def _normalize_shopify_hooks(raw_items: Any) -> list[dict[str, Any]]:
    defaults = [
        {
            "angle": "Durability proof",
            "copy_block": (
                "Unlike models that crack under daily use, ours uses reinforced internal bracing "
                "stress-tested before shipment — built for real routines, not photo shoots."
            ),
        },
        {
            "angle": "Honest expectations",
            "copy_block": (
                "No inflated hero shots — every listing includes exact dimensions and a side-by-side "
                "comparison so you know exactly what arrives at your door."
            ),
        },
    ]
    items = raw_items if isinstance(raw_items, list) else []
    normalized: list[dict[str, Any]] = []
    count = max(2, min(3, len(items) if items else 2))
    for index in range(count):
        item = items[index] if index < len(items) and isinstance(items[index], dict) else {}
        fallback = defaults[min(index, len(defaults) - 1)]
        normalized.append(
            {
                "angle": _ensure_text(item.get("angle"), fallback["angle"]),
                "copy_block": _ensure_text(item.get("copy_block"), fallback["copy_block"]),
            }
        )
    if len(normalized) < 2:
        normalized = defaults.copy()
    return normalized[:3]


def normalize_competitor_sentiment_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    pain_points = _normalize_pain_points(data.get("sentiment_pain_points"))
    category_score = _coerce_score(data.get("category_sentiment_score"), default=55)
    return {
        "sentiment_executive_summary": _ensure_text(
            data.get("sentiment_executive_summary"),
            "Competitor review sentiment synthesized from typical 1–3★ patterns in this niche.",
        ),
        "category_sentiment_score": 50 if category_score is None else category_score,
        "praised_features": _normalize_string_list(
            data.get("praised_features"),
            count=3,
            fallback_prefix="Praised feature",
        ),
        "unmet_needs": _normalize_string_list(
            data.get("unmet_needs"),
            count=3,
            fallback_prefix="Unmet need",
        ),
        "sentiment_pain_points": pain_points,
        "sentiment_improvement_directives": _normalize_improvements(
            data.get("sentiment_improvement_directives"),
            pain_points,
        ),
        "sentiment_shopify_hooks": _normalize_shopify_hooks(data.get("sentiment_shopify_hooks")),
    }
