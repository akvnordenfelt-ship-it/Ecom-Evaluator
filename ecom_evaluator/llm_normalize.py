"""Coerce LLM enum mistakes before Pydantic validation."""

from __future__ import annotations

from typing import Any

from ecom_evaluator.models import ScoredDimension
from ecom_evaluator.scoring import reconcile_final_score


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


def _coerce_viability(value: Any) -> str:
    return _pick_literal(
        value,
        ("Strong", "Marginal", "Weak"),
        {"strong": "Strong", "marginal": "Marginal", "weak": "Weak", "poor": "Weak"},
        "Marginal",
    )


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


def _ensure_text(value: Any, fallback: str) -> str:
    text = _as_str(value)
    return text if text else fallback


def _extract_dimension_score(raw: Any) -> int | None:
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return _coerce_score(raw)
    if isinstance(raw, str):
        return _coerce_score(raw)
    if isinstance(raw, dict):
        for key in ("score", "value", "rating", "points", "score_out_of_100"):
            if key in raw:
                parsed = _coerce_score(raw[key])
                if parsed is not None:
                    return parsed
    return None


def _extract_dimension_motivation(raw: Any) -> str:
    if isinstance(raw, dict):
        for key in ("motivation", "rationale", "reasoning", "explanation", "summary"):
            text = _as_str(raw.get(key))
            if text:
                return text
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return ""


def _normalize_scored_dimension(raw: Any, *, label: str) -> dict[str, Any]:
    score = _extract_dimension_score(raw)
    motivation = _extract_dimension_motivation(raw)
    if score is None:
        raise ValueError(f"{label} score missing or invalid")
    if not motivation:
        motivation = f"Scored {score}/100 for {label.replace('_', ' ')}."
    return {"score": score, "motivation": motivation}


def _normalize_unit_economics(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    legacy_summary = _as_str(data.get("unit_economics_summary"))
    return {
        "viability": _coerce_viability(data.get("viability")),
        "margin_verdict": _ensure_text(
            data.get("margin_verdict") or legacy_summary,
            "Margin viability could not be assessed from the model output.",
        ),
        "shipping_impact": _ensure_text(
            data.get("shipping_impact"),
            "Estimate shipping using billable weight and your carrier rate card.",
        ),
        "pricing_vs_market": _ensure_text(
            data.get("pricing_vs_market"),
            "Compare your intended sell price to the observed market range in the research section.",
        ),
        "break_even_guidance": _ensure_text(
            data.get("break_even_guidance"),
            "Validate break-even with a small test batch before scaling inventory.",
        ),
        "max_affordable_cac": _ensure_text(
            data.get("max_affordable_cac"),
            "Keep paid CAC below roughly 20–30% of gross margin per order.",
        ),
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
                "price_signal": _ensure_text(item.get("price_signal"), "Price not listed in snippet."),
                "similarity_note": _ensure_text(item.get("similarity_note"), "Similar product category."),
            }
        )

    return {
        "executive_summary": _ensure_text(
            data.get("executive_summary"),
            "Market research was limited in this run — competitor density and demand remain uncertain.",
        ),
        "competitor_count_signal": _coerce_competitor_count(data.get("competitor_count_signal")),
        "amazon_landscape": _ensure_text(
            data.get("amazon_landscape"),
            "No Amazon listings were captured in this scan's search snippets; treat Amazon competition as unverified.",
        ),
        "aliexpress_landscape": _ensure_text(
            data.get("aliexpress_landscape"),
            "No AliExpress listings were captured in this scan's search snippets; sourcing pressure is unverified.",
        ),
        "independent_stores_landscape": _ensure_text(
            data.get("independent_stores_landscape"),
            "No independent DTC stores were captured in this scan's search snippets.",
        ),
        "price_range_observed": _ensure_text(
            data.get("price_range_observed"),
            "Price range not clearly observed in search snippets for this run.",
        ),
        "demand_estimate": {
            "level": _coerce_demand_level(demand.get("level")),
            "estimated_sales_note": _ensure_text(
                demand.get("estimated_sales_note"),
                "Exact sales volume is unavailable from search snippets alone.",
            ),
            "reasoning": _ensure_text(
                demand.get("reasoning"),
                "Demand was inferred from listing density and review language where visible in search results.",
            ),
        },
        "key_competitors": competitors[:3],
        "strategic_implications": _ensure_text(
            data.get("strategic_implications"),
            "Validate differentiation and margin with a sample order before scaling inventory.",
        ),
        "data_limitations": _ensure_text(
            data.get("data_limitations"),
            "Analysis is based on DuckDuckGo search snippets only — no verified sales or ad-spend data.",
        ),
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
        fit = _coerce_score(item.get("fit_score"))
        platforms.append(
            {
                "platform": _coerce_platform(item.get("platform")),
                "fit_score": fit if fit is not None else 50,
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
        raise ValueError(f"expected at least {min_items} list items, got {len(cleaned)}")
    return cleaned


def normalize_core_payload(raw: Any) -> dict[str, Any]:
    data = dict(raw) if isinstance(raw, dict) else {}
    saturation = data.get("market_saturation") if isinstance(data.get("market_saturation"), dict) else {}

    short_term = _normalize_scored_dimension(data.get("short_term_potential"), label="short_term_potential")
    long_term = _normalize_scored_dimension(data.get("long_term_stability"), label="long_term_stability")
    scalability = _normalize_scored_dimension(data.get("scalability"), label="scalability")
    marketing = _normalize_scored_dimension(data.get("marketing_suitability"), label="marketing_suitability")

    llm_final = _coerce_score(data.get("final_score"))
    final_score = reconcile_final_score(
        llm_final,
        ScoredDimension.model_validate(short_term),
        ScoredDimension.model_validate(long_term),
        ScoredDimension.model_validate(scalability),
        ScoredDimension.model_validate(marketing),
    )

    return {
        "final_score": final_score,
        "investment_headline": _ensure_text(
            data.get("investment_headline"),
            f"Overall investment score {final_score}/100 — review risks and next steps before committing.",
        ),
        "market_research": _normalize_market_research(data.get("market_research")),
        "short_term_potential": short_term,
        "long_term_stability": long_term,
        "scalability": scalability,
        "marketing_suitability": marketing,
        "market_saturation": {
            "level": _coerce_saturation_level(saturation.get("level")),
            "motivation": _ensure_text(
                saturation.get("motivation"),
                "Saturation reflects how crowded similar listings appear in the search snapshot.",
            ),
        },
        "estimated_shipping_category": _ensure_text(
            data.get("estimated_shipping_category"),
            "Shipping class could not be determined — confirm billable weight with your carrier or 3PL.",
        ),
        "unit_economics": _normalize_unit_economics(
            data.get("unit_economics") or {"unit_economics_summary": data.get("unit_economics_summary")}
        ),
        "marketing_fit_preview": _ensure_text(
            data.get("marketing_fit_preview"),
            "Visual demo channels such as TikTok or Instagram are typical starting points for physical products.",
        ),
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
