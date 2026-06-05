"""Coerce LLM enum mistakes before Pydantic validation — no generic filler text."""

from __future__ import annotations

from typing import Any


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _pick_literal(value: Any, allowed: tuple[str, ...], aliases: dict[str, str], default: str) -> str:
    text = _as_str(value)
    if text in allowed:
        return text
    mapped = aliases.get(text.lower())
    if mapped in allowed:
        return mapped
    for option in allowed:
        if option.lower() == text.lower():
            return option
    return default if not text else default


def _coerce_competitor_count(value: Any) -> str:
    return _pick_literal(
        value,
        ("Few", "Moderate", "Many", "Unknown"),
        {
            "low": "Few",
            "few": "Few",
            "medium": "Moderate",
            "moderate": "Moderate",
            "mid": "Moderate",
            "high": "Many",
            "many": "Many",
            "unknown": "Unknown",
        },
        "Unknown",
    )


def _coerce_demand_level(value: Any) -> str:
    return _pick_literal(
        value,
        ("Low", "Medium", "High", "Unknown"),
        {"low": "Low", "medium": "Medium", "moderate": "Medium", "high": "High", "unknown": "Unknown"},
        "Unknown",
    )


def _coerce_saturation_level(value: Any) -> str:
    return _pick_literal(
        value,
        ("Low", "Medium", "High"),
        {"low": "Low", "medium": "Medium", "moderate": "Medium", "high": "High"},
        "Medium",
    )


def _coerce_roi_level(value: Any) -> str:
    return _pick_literal(
        value,
        ("Low", "Medium", "High"),
        {"low": "Low", "medium": "Medium", "moderate": "Medium", "high": "High"},
        "Medium",
    )


def _coerce_organic_vs_paid(value: Any) -> str:
    return _pick_literal(
        value,
        ("Organic-first", "Paid-first", "Balanced"),
        {
            "organic-first": "Organic-first",
            "organic first": "Organic-first",
            "organic": "Organic-first",
            "paid-first": "Paid-first",
            "paid first": "Paid-first",
            "paid": "Paid-first",
            "balanced": "Balanced",
            "both": "Balanced",
        },
        "Balanced",
    )


def _coerce_platform(value: Any) -> str:
    allowed = (
        "TikTok",
        "Instagram",
        "Facebook",
        "YouTube",
        "Google Ads",
        "Amazon Ads",
        "Pinterest",
        "Email/SMS",
        "Other",
    )
    text = _as_str(value)
    if text in allowed:
        return text
    aliases = {
        "tiktok": "TikTok",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "meta": "Facebook",
        "youtube": "YouTube",
        "google ads": "Google Ads",
        "google": "Google Ads",
        "amazon ads": "Amazon Ads",
        "amazon": "Amazon Ads",
        "pinterest": "Pinterest",
        "email": "Email/SMS",
        "sms": "Email/SMS",
    }
    return aliases.get(text.lower(), "Other")


def _coerce_competitor_platform(value: Any) -> str:
    return _pick_literal(
        value,
        ("Amazon", "AliExpress", "Independent", "Other"),
        {
            "amazon": "Amazon",
            "aliexpress": "AliExpress",
            "independent": "Independent",
            "shopify": "Independent",
            "other": "Other",
        },
        "Other",
    )


def _coerce_score(value: Any, default: int = 50) -> int:
    try:
        return max(0, min(100, int(value)))
    except (TypeError, ValueError):
        return default


def _normalize_scored_dimension(raw: Any) -> dict[str, Any]:
    data = raw if isinstance(raw, dict) else {}
    return {
        "score": _coerce_score(data.get("score")),
        "motivation": _as_str(data.get("motivation")),
    }


def _normalize_market_research(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    demand = data.get("demand_estimate") if isinstance(data.get("demand_estimate"), dict) else {}

    competitors: list[dict[str, Any]] = []
    for item in data.get("key_competitors") or []:
        if not isinstance(item, dict):
            continue
        url = _as_str(item.get("source_url"))
        title = _as_str(item.get("listing_title"))
        if not url or not title or "example.com" in url.lower():
            continue
        competitors.append(
            {
                "platform": _coerce_competitor_platform(item.get("platform")),
                "listing_title": title,
                "source_url": url,
                "price_signal": _as_str(item.get("price_signal")),
                "similarity_note": _as_str(item.get("similarity_note")),
            }
        )

    return {
        "executive_summary": _as_str(data.get("executive_summary")),
        "competitor_count_signal": _coerce_competitor_count(data.get("competitor_count_signal")),
        "amazon_landscape": _as_str(data.get("amazon_landscape")),
        "aliexpress_landscape": _as_str(data.get("aliexpress_landscape")),
        "independent_stores_landscape": _as_str(data.get("independent_stores_landscape")),
        "price_range_observed": _as_str(data.get("price_range_observed")),
        "demand_estimate": {
            "level": _coerce_demand_level(demand.get("level")),
            "estimated_sales_note": _as_str(demand.get("estimated_sales_note")),
            "reasoning": _as_str(demand.get("reasoning")),
        },
        "key_competitors": competitors[:3],
        "strategic_implications": _as_str(data.get("strategic_implications")),
        "data_limitations": _as_str(data.get("data_limitations")),
    }


def _normalize_marketing_plan(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    audience = data.get("target_audience") if isinstance(data.get("target_audience"), dict) else {}
    organic = data.get("organic_strategy") if isinstance(data.get("organic_strategy"), dict) else {}
    paid = data.get("paid_ads_strategy") if isinstance(data.get("paid_ads_strategy"), dict) else {}

    def _str_list(value: Any, max_items: int) -> list[str]:
        items = [_as_str(v) for v in value] if isinstance(value, list) else []
        return [item for item in items if item][:max_items]

    platforms: list[dict[str, Any]] = []
    for item in data.get("platform_recommendations") or []:
        if not isinstance(item, dict):
            continue
        why = _as_str(item.get("why_it_works"))
        signal = _as_str(item.get("competitor_success_signal"))
        if not why and not signal:
            continue
        platforms.append(
            {
                "platform": _coerce_platform(item.get("platform")),
                "fit_score": _coerce_score(item.get("fit_score")),
                "roi_potential": _coerce_roi_level(item.get("roi_potential")),
                "organic_vs_paid": _coerce_organic_vs_paid(item.get("organic_vs_paid")),
                "why_it_works": why,
                "competitor_success_signal": signal,
            }
        )

    concepts: list[dict[str, Any]] = []
    for item in data.get("creative_concepts") or []:
        if not isinstance(item, dict):
            continue
        title = _as_str(item.get("title"))
        script = _as_str(item.get("script_or_copy"))
        if not title and not script:
            continue
        concepts.append(
            {
                "title": title,
                "format": _as_str(item.get("format")),
                "hook_angle": _as_str(item.get("hook_angle")),
                "script_or_copy": script,
                "recommended_platform": _as_str(item.get("recommended_platform")),
            }
        )

    return {
        "executive_summary": _as_str(data.get("executive_summary")),
        "target_audience": {
            "persona_name": _as_str(audience.get("persona_name")),
            "age_range": _as_str(audience.get("age_range")),
            "psychographics": _as_str(audience.get("psychographics")),
            "pain_points": _str_list(audience.get("pain_points"), 5),
            "platforms_they_use": _str_list(audience.get("platforms_they_use"), 6),
        },
        "organic_strategy": {
            "overview": _as_str(organic.get("overview")),
            "content_formats": _str_list(organic.get("content_formats"), 5),
            "posting_cadence": _as_str(organic.get("posting_cadence")),
            "creator_angles": _str_list(organic.get("creator_angles"), 4),
        },
        "paid_ads_strategy": {
            "overview": _as_str(paid.get("overview")),
            "primary_channels": _str_list(paid.get("primary_channels"), 4),
            "budget_starter_usd": _as_str(paid.get("budget_starter_usd")),
            "targeting_approach": _as_str(paid.get("targeting_approach")),
            "roi_outlook": _coerce_roi_level(paid.get("roi_outlook")),
        },
        "platform_recommendations": platforms[:3],
        "competitor_marketing_insights": _as_str(data.get("competitor_marketing_insights")),
        "creative_concepts": concepts[:2],
        "priority_playbook": _str_list(data.get("priority_playbook"), 3),
    }


def _str_list(value: Any, *, min_items: int, max_items: int) -> list[str]:
    items = [_as_str(v) for v in value] if isinstance(value, list) else []
    cleaned = [item for item in items if item][:max_items]
    if len(cleaned) < min_items:
        return cleaned
    return cleaned


def normalize_core_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    saturation = data.get("market_saturation") if isinstance(data.get("market_saturation"), dict) else {}
    return {
        "final_score": _coerce_score(data.get("final_score")),
        "investment_headline": _as_str(data.get("investment_headline")),
        "market_research": _normalize_market_research(data.get("market_research")),
        "short_term_potential": _normalize_scored_dimension(data.get("short_term_potential")),
        "long_term_stability": _normalize_scored_dimension(data.get("long_term_stability")),
        "scalability": _normalize_scored_dimension(data.get("scalability")),
        "marketing_suitability": _normalize_scored_dimension(data.get("marketing_suitability")),
        "market_saturation": {
            "level": _coerce_saturation_level(saturation.get("level")),
            "motivation": _as_str(saturation.get("motivation")),
        },
        "estimated_shipping_category": _as_str(data.get("estimated_shipping_category")),
        "unit_economics_summary": _as_str(data.get("unit_economics_summary")),
        "marketing_fit_preview": _as_str(data.get("marketing_fit_preview")),
        "top_risks": _str_list(data.get("top_risks"), min_items=2, max_items=3),
        "top_opportunities": _str_list(data.get("top_opportunities"), min_items=2, max_items=3),
        "next_steps": _str_list(data.get("next_steps"), min_items=3, max_items=3),
    }


def normalize_marketing_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    return {
        "marketing_plan": _normalize_marketing_plan(data.get("marketing_plan")),
        "go_to_market_strategy": _as_str(data.get("go_to_market_strategy")),
    }


def normalize_evaluation_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    core = normalize_core_payload(data)
    marketing = normalize_marketing_payload(data)
    return {**core, **marketing}
