"""Coerce lightweight Claude JSON (mostly strings) before Pydantic validation."""

from __future__ import annotations

from typing import Any

from ecom_evaluator.scoring import compute_confidence_percentage, compute_overall_score, compute_risk_score, risk_tier_label


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


def normalize_section1_payload(raw: Any, *, input_count: int = 5) -> dict[str, Any]:
    """Section 1 — profile and sub-scores. Overall score computed in Python."""
    data = dict(raw) if isinstance(raw, dict) else {}

    logistics = _coerce_score(
        data.get("logistics_score") or data.get("metric_logistics_margin"), default=50
    )
    saturation = _coerce_score(
        data.get("saturation_score") or data.get("metric_market_saturation"), default=50
    )
    velocity = _coerce_score(
        data.get("marketing_score") or data.get("metric_marketing_velocity"), default=50
    )
    brandability = _coerce_score(
        data.get("brandability_score") or data.get("metric_brandability"), default=50
    )
    seasonality = _coerce_score(
        data.get("seasonality_score") or data.get("metric_seasonality"), default=50
    )
    logistics = 50 if logistics is None else logistics
    saturation = 50 if saturation is None else saturation
    velocity = 50 if velocity is None else velocity
    brandability = 50 if brandability is None else brandability
    seasonality = 50 if seasonality is None else seasonality
    overall = compute_overall_score(logistics, saturation, velocity, brandability, seasonality)

    category = _ensure_text(data.get("category"), "General e-commerce")
    product_type = _ensure_text(data.get("product_type"), "Consumer product")
    main_use = _ensure_text(data.get("main_use"), "Everyday use")
    key_feature = _ensure_text(data.get("key_feature"), "Core utility")
    weight_class = _ensure_text(data.get("weight_class"), "Standard parcel")
    fragility = _ensure_text(data.get("fragility"), "Standard handling")
    variants = _ensure_text(data.get("variants"), "Single SKU assumed")
    shipping = _ensure_text(data.get("shipping_complexity"), "Standard shipping")

    confidence = _coerce_score(data.get("confidence_percentage"))
    if confidence is None:
        confidence = compute_confidence_percentage(input_count=input_count)

    summary = _ensure_text(
        data.get("product_profile_summary"),
        f"{category} — {product_type}. {main_use}. Key feature: {key_feature}.",
    )
    one_line = _ensure_text(data.get("one_line_verdict"), "Evaluate margins before scaling.")

    return {
        "overall_score": overall,
        "product_category": category,
        "product_type": product_type,
        "main_use": main_use,
        "key_feature": key_feature,
        "one_line_verdict": one_line[:120],
        "confidence_percentage": confidence,
        "product_profile_summary": summary,
        "physical_weight_assessment": weight_class,
        "fragility_assessment": fragility,
        "variant_complexity": variants,
        "shipping_complexity": shipping,
        "metric_logistics_margin": logistics,
        "metric_logistics_margin_note": _ensure_text(
            data.get("logistics_note") or data.get("metric_logistics_margin_note"),
            "Lightweight, high-markup products score highest on logistics and margin.",
        ),
        "metric_market_saturation": saturation,
        "metric_market_saturation_note": _ensure_text(
            data.get("saturation_note") or data.get("metric_market_saturation_note"),
            "Market opportunity — lower scores mean heavier crowding.",
        ),
        "metric_marketing_velocity": velocity,
        "metric_marketing_velocity_note": _ensure_text(
            data.get("marketing_note") or data.get("metric_marketing_velocity_note"),
            "Organic viral potential vs paid viability.",
        ),
        "metric_seasonality": seasonality,
        "metric_seasonality_note": _ensure_text(
            data.get("seasonality_note") or data.get("metric_seasonality_note"),
            "Year-round demand scores higher than holiday-only spikes.",
        ),
        "metric_brandability": brandability,
        "metric_brandability_note": _ensure_text(
            data.get("brandability_note") or data.get("metric_brandability_note"),
            "Long-term brand potential vs impulse-buy fad risk.",
        ),
        "red_flag_headline": "Pending risk analysis",
        "red_flag_analysis": "Section 2 will analyse red flags.",
        "red_flag_1": "Pending",
        "red_flag_2": "Pending",
        "red_flag_3": "Pending",
    }


def normalize_section2_payload(raw: Any) -> dict[str, Any]:
    """Section 2 — red flags. Risk score computed in Python."""
    data = dict(raw) if isinstance(raw, dict) else {}
    flags_raw = data.get("flags") if isinstance(data.get("flags"), list) else []

    flags: list[dict[str, str]] = []
    severities: list[str] = []
    for item in flags_raw[:6]:
        if not isinstance(item, dict):
            continue
        severity = _ensure_text(item.get("severity"), "MEDIUM").upper()
        if severity not in {"SEVERE", "HIGH", "MEDIUM", "LOW"}:
            severity = "MEDIUM"
        severities.append(severity)
        flags.append(
            {
                "title": _ensure_text(item.get("title"), "Risk factor"),
                "severity": severity,
                "explanation": _ensure_text(item.get("explanation"), "Review before scaling."),
                "means_for_you": _ensure_text(
                    item.get("means_for_you"),
                    "What this means for you: validate with a sample order first.",
                ),
            }
        )

    if len(flags) < 3:
        defaults = [
            ("Thin margins", "MEDIUM", "Unit economics may not survive paid ads.", "What this means for you: model CPA before spending."),
            ("Category competition", "HIGH", "Incumbents may undercut on price.", "What this means for you: differentiate or avoid price wars."),
            ("Operational risk", "MEDIUM", "Shipping or QC surprises erode margin.", "What this means for you: order samples and test carriers."),
        ]
        for title, sev, expl, means in defaults[len(flags) : 3]:
            severities.append(sev)
            flags.append(
                {"title": title, "severity": sev, "explanation": expl, "means_for_you": means}
            )

    risk_score = compute_risk_score(severities)
    risk_tier = risk_tier_label(risk_score)

    would_invest = data.get("would_invest")
    if isinstance(would_invest, str):
        would_invest = would_invest.strip().lower() in {"true", "yes", "1"}
    elif would_invest is None:
        would_invest = risk_score < 56

    invest_reasoning = _ensure_text(
        data.get("invest_reasoning"),
        "Yes with conditions" if would_invest else "No — risks outweigh upside at current inputs.",
    )

    titles = [f["title"] for f in flags[:3]]
    analysis_parts = [f"{f['title']}: {f['explanation']}" for f in flags]

    return {
        "risk_score": risk_score,
        "risk_tier": risk_tier,
        "risk_flags": flags,
        "would_invest": bool(would_invest),
        "invest_reasoning": invest_reasoning,
        "red_flag_headline": _ensure_text(
            data.get("red_flag_headline"),
            f"{len(flags)} material risks identified",
        ),
        "red_flag_analysis": _ensure_text(
            data.get("red_flag_analysis"),
            " ".join(analysis_parts[:4]),
        ),
        "red_flag_1": titles[0] if len(titles) > 0 else "Margin risk",
        "red_flag_2": titles[1] if len(titles) > 1 else "Competition risk",
        "red_flag_3": titles[2] if len(titles) > 2 else "Operational risk",
    }


def merge_section1_and_section2(section1: dict[str, Any], section2: dict[str, Any]) -> dict[str, Any]:
    merged = dict(section1)
    merged.update(section2)
    return merged


def normalize_free_evaluation_payload(raw: Any) -> dict[str, Any]:
    """Legacy combined S1+S2 normalizer."""
    section1 = normalize_section1_payload(raw)
    section2 = normalize_section2_payload(raw)
    return merge_section1_and_section2(section1, section2)


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
                "problem": _ensure_text(item.get("problem"), ""),
                "solution": _ensure_text(item.get("solution"), fallback["body"]),
                "social_proof": _ensure_text(item.get("social_proof"), ""),
                "cta": _ensure_text(item.get("cta"), fallback["cta"]),
                "visual_cues": _ensure_text(item.get("visual_cues"), ""),
                "estimated_length": _ensure_text(item.get("estimated_length"), "30–45 sec"),
                "body": _ensure_text(
                    item.get("body") or item.get("solution"),
                    fallback["body"],
                ),
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
            "marketing_angle_details": _normalize_string_list(
                data.get("marketing_angle_details") or data.get("marketing_angles"),
                count=3,
                fallback_prefix="Angle detail",
            ),
            "channel_recommendation_reason": _ensure_text(
                data.get("channel_recommendation_reason"),
                "Lead with the channel where this product is easiest to demo visually.",
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
        "financial_recommendation": _ensure_text(
            data.get("financial_recommendation"),
            "Validate break-even CPA with a small paid test before scaling spend.",
        ),
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
        "trending_keywords": _normalize_string_list(
            data.get("trending_keywords"),
            count=3,
            fallback_prefix="Keyword",
        ),
        "live_market_summary": _ensure_text(
            data.get("live_market_summary") or data.get("web_intelligence_summary"),
            "Live market summary unavailable — re-run Section 5.",
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
        "supplier_briefing_note": _ensure_text(
            data.get("supplier_briefing_note"),
            "Request pre-shipment QC on the top complaint areas identified in competitor reviews.",
        ),
        "competitive_opportunity_summary": _ensure_text(
            data.get("competitive_opportunity_summary") or data.get("sentiment_executive_summary"),
            "Competitive opportunity summary synthesized from category review patterns.",
        ),
    }
