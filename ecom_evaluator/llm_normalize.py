"""Normalize LLM JSON payloads before Pydantic validation."""

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
    return default


def _coerce_competitor_count(value: Any) -> str:
    return _pick_literal(
        value,
        ("Few", "Moderate", "Many", "Unknown"),
        {
            "low": "Few",
            "few": "Few",
            "light": "Few",
            "medium": "Moderate",
            "moderate": "Moderate",
            "mid": "Moderate",
            "average": "Moderate",
            "high": "Many",
            "many": "Many",
            "heavy": "Many",
            "crowded": "Many",
            "unknown": "Unknown",
            "unclear": "Unknown",
            "n/a": "Unknown",
        },
        "Unknown",
    )


def _coerce_demand_level(value: Any) -> str:
    return _pick_literal(
        value,
        ("Low", "Medium", "High", "Unknown"),
        {
            "low": "Low",
            "medium": "Medium",
            "moderate": "Medium",
            "mid": "Medium",
            "high": "High",
            "unknown": "Unknown",
            "unclear": "Unknown",
        },
        "Unknown",
    )


def _coerce_saturation_level(value: Any) -> str:
    return _pick_literal(
        value,
        ("Low", "Medium", "High"),
        {
            "low": "Low",
            "medium": "Medium",
            "moderate": "Medium",
            "mid": "Medium",
            "high": "High",
        },
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
            "hybrid": "Balanced",
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
    lower = text.lower()
    aliases = {
        "tiktok": "TikTok",
        "tik tok": "TikTok",
        "instagram": "Instagram",
        "ig": "Instagram",
        "facebook": "Facebook",
        "fb": "Facebook",
        "meta": "Facebook",
        "youtube": "YouTube",
        "yt": "YouTube",
        "google ads": "Google Ads",
        "google": "Google Ads",
        "amazon ads": "Amazon Ads",
        "amazon": "Amazon Ads",
        "pinterest": "Pinterest",
        "email": "Email/SMS",
        "sms": "Email/SMS",
        "email/sms": "Email/SMS",
    }
    if lower in aliases:
        return aliases[lower]
    return "Other"


def _coerce_competitor_platform(value: Any) -> str:
    return _pick_literal(
        value,
        ("Amazon", "AliExpress", "Independent", "Other"),
        {
            "amazon": "Amazon",
            "aliexpress": "AliExpress",
            "ali express": "AliExpress",
            "independent": "Independent",
            "independent stores": "Independent",
            "shopify": "Independent",
            "dtc": "Independent",
            "other": "Other",
        },
        "Other",
    )


def _ensure_text(value: Any, fallback: str) -> str:
    text = _as_str(value)
    return text if text else fallback


def _ensure_str_list(value: Any, *, min_items: int, max_items: int, fallback: str) -> list[str]:
    items: list[str] = []
    if isinstance(value, list):
        for item in value:
            text = _as_str(item)
            if text:
                items.append(text)
    elif _as_str(value):
        items.append(_as_str(value))
    while len(items) < min_items:
        items.append(fallback)
    return items[:max_items]


def _normalize_scored_dimension(raw: Any) -> dict[str, Any]:
    data = raw if isinstance(raw, dict) else {}
    score = data.get("score", 50)
    try:
        score = int(score)
    except (TypeError, ValueError):
        score = 50
    score = max(0, min(100, score))
    return {
        "score": score,
        "motivation": _ensure_text(data.get("motivation"), "No rationale provided."),
    }


def _normalize_market_research(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    demand = data.get("demand_estimate") if isinstance(data.get("demand_estimate"), dict) else {}

    competitors: list[dict[str, Any]] = []
    for item in data.get("key_competitors") or []:
        if not isinstance(item, dict):
            continue
        competitors.append(
            {
                "platform": _coerce_competitor_platform(item.get("platform")),
                "listing_title": _ensure_text(item.get("listing_title"), "Unknown listing"),
                "source_url": _ensure_text(item.get("source_url"), "https://example.com"),
                "price_signal": _ensure_text(item.get("price_signal"), "Not stated"),
                "similarity_note": _ensure_text(item.get("similarity_note"), "Similar product"),
            }
        )

    return {
        "executive_summary": _ensure_text(
            data.get("executive_summary"),
            _ensure_text(data.get("strategic_implications"), "Market research summary unavailable."),
        ),
        "competitor_count_signal": _coerce_competitor_count(data.get("competitor_count_signal")),
        "amazon_landscape": _ensure_text(data.get("amazon_landscape"), "No Amazon data in search results."),
        "aliexpress_landscape": _ensure_text(
            data.get("aliexpress_landscape"), "No AliExpress data in search results."
        ),
        "independent_stores_landscape": _ensure_text(
            data.get("independent_stores_landscape"), "No independent store data in search results."
        ),
        "price_range_observed": _ensure_text(data.get("price_range_observed"), "Not observed"),
        "demand_estimate": {
            "level": _coerce_demand_level(demand.get("level")),
            "estimated_sales_note": _ensure_text(
                demand.get("estimated_sales_note"), "Qualitative demand only."
            ),
            "reasoning": _ensure_text(demand.get("reasoning"), "Based on limited search snippets."),
        },
        "key_competitors": competitors[:3],
        "strategic_implications": _ensure_text(
            data.get("strategic_implications"), "Differentiate on brand and offer."
        ),
        "data_limitations": _ensure_text(
            data.get("data_limitations"), "Search snippets only; no verified sales figures."
        ),
    }


def _normalize_marketing_plan(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    audience = data.get("target_audience") if isinstance(data.get("target_audience"), dict) else {}
    organic = data.get("organic_strategy") if isinstance(data.get("organic_strategy"), dict) else {}
    paid = data.get("paid_ads_strategy") if isinstance(data.get("paid_ads_strategy"), dict) else {}

    platforms: list[dict[str, Any]] = []
    for item in data.get("platform_recommendations") or []:
        if not isinstance(item, dict):
            continue
        fit = item.get("fit_score", 50)
        try:
            fit = max(0, min(100, int(fit)))
        except (TypeError, ValueError):
            fit = 50
        platforms.append(
            {
                "platform": _coerce_platform(item.get("platform")),
                "fit_score": fit,
                "roi_potential": _coerce_roi_level(item.get("roi_potential")),
                "organic_vs_paid": _coerce_organic_vs_paid(item.get("organic_vs_paid")),
                "why_it_works": _ensure_text(item.get("why_it_works"), "Fits this audience."),
                "competitor_success_signal": _ensure_text(
                    item.get("competitor_success_signal"), "Similar products active on this channel."
                ),
            }
        )
    while len(platforms) < 3:
        platforms.append(
            {
                "platform": "Other",
                "fit_score": 40,
                "roi_potential": "Medium",
                "organic_vs_paid": "Balanced",
                "why_it_works": "Test after core channels.",
                "competitor_success_signal": "Limited evidence from search.",
            }
        )

    concepts: list[dict[str, Any]] = []
    for item in data.get("creative_concepts") or []:
        if not isinstance(item, dict):
            continue
        concepts.append(
            {
                "title": _ensure_text(item.get("title"), "Concept"),
                "format": _ensure_text(item.get("format"), "Short video"),
                "hook_angle": _ensure_text(item.get("hook_angle"), "Problem-solution"),
                "script_or_copy": _ensure_text(item.get("script_or_copy"), "Demo the product benefit."),
                "recommended_platform": _ensure_text(item.get("recommended_platform"), "TikTok"),
            }
        )
    while len(concepts) < 2:
        concepts.append(
            {
                "title": f"Concept {len(concepts) + 1}",
                "format": "Short video",
                "hook_angle": "Before/after demo",
                "script_or_copy": "Show the product solving a clear pain point.",
                "recommended_platform": "TikTok",
            }
        )

    return {
        "executive_summary": _ensure_text(
            data.get("executive_summary"), "Lead with short-form video and retarget warm traffic."
        ),
        "target_audience": {
            "persona_name": _ensure_text(audience.get("persona_name"), "Target buyer"),
            "age_range": _ensure_text(audience.get("age_range"), "25-44"),
            "psychographics": _ensure_text(audience.get("psychographics"), "Practical online shopper."),
            "pain_points": _ensure_str_list(
                audience.get("pain_points"), min_items=2, max_items=5, fallback="Unclear product fit"
            ),
            "platforms_they_use": _ensure_str_list(
                audience.get("platforms_they_use"),
                min_items=2,
                max_items=6,
                fallback="Instagram",
            ),
        },
        "organic_strategy": {
            "overview": _ensure_text(organic.get("overview"), "Publish short demo content."),
            "content_formats": _ensure_str_list(
                organic.get("content_formats"), min_items=2, max_items=5, fallback="Short video"
            ),
            "posting_cadence": _ensure_text(organic.get("posting_cadence"), "3-4 posts per week"),
            "creator_angles": _ensure_str_list(
                organic.get("creator_angles"), min_items=2, max_items=4, fallback="Product demo"
            ),
        },
        "paid_ads_strategy": {
            "overview": _ensure_text(paid.get("overview"), "Start with small paid tests."),
            "primary_channels": _ensure_str_list(
                paid.get("primary_channels"), min_items=1, max_items=4, fallback="Meta Ads"
            ),
            "budget_starter_usd": _ensure_text(paid.get("budget_starter_usd"), "$20-40/day"),
            "targeting_approach": _ensure_text(paid.get("targeting_approach"), "Interest-based targeting."),
            "roi_outlook": _coerce_roi_level(paid.get("roi_outlook")),
        },
        "platform_recommendations": platforms[:3],
        "competitor_marketing_insights": _ensure_text(
            data.get("competitor_marketing_insights"), "Competitors rely on demos and offer-led ads."
        ),
        "creative_concepts": concepts[:2],
        "priority_playbook": _ensure_str_list(
            data.get("priority_playbook"),
            min_items=3,
            max_items=3,
            fallback="Launch a test campaign",
        ),
    }


def normalize_evaluation_payload(raw: Any) -> dict[str, Any]:
    """Coerce common LLM JSON mistakes into a ProductEvaluationResponse-shaped dict."""
    data = dict(raw) if isinstance(raw, dict) else {}

    try:
        final_score = max(0, min(100, int(data.get("final_score", 50))))
    except (TypeError, ValueError):
        final_score = 50

    saturation = data.get("market_saturation") if isinstance(data.get("market_saturation"), dict) else {}

    return {
        "final_score": final_score,
        "market_research": _normalize_market_research(data.get("market_research")),
        "short_term_potential": _normalize_scored_dimension(data.get("short_term_potential")),
        "long_term_stability": _normalize_scored_dimension(data.get("long_term_stability")),
        "scalability": _normalize_scored_dimension(data.get("scalability")),
        "marketing_suitability": _normalize_scored_dimension(data.get("marketing_suitability")),
        "market_saturation": {
            "level": _coerce_saturation_level(saturation.get("level")),
            "motivation": _ensure_text(saturation.get("motivation"), "Moderate competitive pressure."),
        },
        "estimated_shipping_category": _ensure_text(
            data.get("estimated_shipping_category"), "Standard small parcel shipping."
        ),
        "marketing_plan": _normalize_marketing_plan(data.get("marketing_plan")),
        "go_to_market_strategy": _ensure_text(
            data.get("go_to_market_strategy"), "## Phase 1\nValidate offer and creative."
        ),
    }
