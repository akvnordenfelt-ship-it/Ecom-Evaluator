"""Tests for Pydantic evaluation models."""

import pytest
from pydantic import ValidationError

from ecom_evaluator.llm_normalize import normalize_evaluation_payload
from ecom_evaluator.models import ProductEvaluationResponse


def _sample_marketing_plan() -> dict:
    return {
        "executive_summary": "Lead with short-form video on TikTok and retarget with Meta ads.",
        "target_audience": {
            "persona_name": "Budget-conscious home organizer",
            "age_range": "25–40",
            "psychographics": "Values practical gadgets that save time.",
            "pain_points": ["Cluttered drawers", "Overpriced branded tools"],
            "platforms_they_use": ["TikTok", "Instagram", "Amazon"],
        },
        "organic_strategy": {
            "overview": "UGC demos showing before/after organization wins.",
            "content_formats": ["15s demos", "Carousel tips", "Creator unboxings"],
            "posting_cadence": "4–5 posts per week for 30 days",
            "creator_angles": ["Kitchen hack", "Amazon find", "Gift idea"],
        },
        "paid_ads_strategy": {
            "overview": "Start with TikTok Spark Ads on top organic posts, then Meta retargeting.",
            "primary_channels": ["TikTok Ads", "Meta Ads"],
            "budget_starter_usd": "$30–50/day",
            "targeting_approach": "Interest stacks: home organization, Amazon Finds, kitchen gadgets.",
            "roi_outlook": "Medium",
        },
        "platform_recommendations": [
            {
                "platform": "TikTok",
                "fit_score": 88,
                "roi_potential": "High",
                "organic_vs_paid": "Organic-first",
                "why_it_works": "Visual demo products perform well in feed.",
                "competitor_success_signal": "Similar kits use POV cleaning hooks.",
            },
            {
                "platform": "Instagram",
                "fit_score": 72,
                "roi_potential": "Medium",
                "organic_vs_paid": "Balanced",
                "why_it_works": "Carousel before/after content converts for home niche.",
                "competitor_success_signal": "Indie brands run Reels with link-in-bio offers.",
            },
            {
                "platform": "Amazon Ads",
                "fit_score": 65,
                "roi_potential": "Medium",
                "organic_vs_paid": "Paid-first",
                "why_it_works": "High-intent shoppers already compare listings.",
                "competitor_success_signal": "Competitors sponsor exact-match keywords.",
            },
        ],
        "competitor_marketing_insights": "Top competitors lean on UGC demos and bundle discounts.",
        "creative_concepts": [
            {
                "title": "Drawer disaster fix",
                "format": "15s vertical video",
                "hook_angle": "Problem agitation in first 2 seconds",
                "script_or_copy": "POV: your junk drawer finally makes sense.",
                "recommended_platform": "TikTok",
            },
            {
                "title": "Amazon vs our kit",
                "format": "Carousel",
                "hook_angle": "Price/value comparison",
                "script_or_copy": "Same result, half the price — swipe to compare.",
                "recommended_platform": "Instagram",
            },
        ],
        "priority_playbook": [
            "Film 3 UGC demos this week",
            "Launch TikTok organic posts daily",
            "Turn best post into Spark Ad with $30/day cap",
        ],
    }


def _sample_payload() -> dict:
    return {
        "final_score": 72,
        "investment_headline": "Solid niche opportunity if you differentiate on creative and margin.",
        "market_research": {
            "executive_summary": "Moderate competition with room to niche.",
            "competitor_count_signal": "Moderate",
            "amazon_landscape": "Several similar listings on Amazon.",
            "aliexpress_landscape": "Many low-cost alternatives on AliExpress.",
            "independent_stores_landscape": "Few DTC brands found.",
            "price_range_observed": "$15–$35",
            "demand_estimate": {
                "level": "Medium",
                "estimated_sales_note": "Steady search interest; no exact sales data.",
                "reasoning": "Multiple listings and review language suggest ongoing demand.",
            },
            "key_competitors": [],
            "strategic_implications": "Differentiate on brand and creative.",
            "data_limitations": "Search snippets only; no verified sales figures.",
        },
        "short_term_potential": {"score": 70, "motivation": "Good margin and trend fit."},
        "long_term_stability": {"score": 60, "motivation": "Risk of commoditization."},
        "scalability": {"score": 65, "motivation": "Fulfillment is straightforward."},
        "marketing_suitability": {"score": 80, "motivation": "Strong visual demo potential."},
        "market_saturation": {"level": "Medium", "motivation": "Crowded but not saturated."},
        "estimated_shipping_category": "Small parcel; billable weight ~0.4 kg.",
        "unit_economics": {
            "viability": "Marginal",
            "margin_verdict": "Healthy gross margin at listed prices, but shipping and CAC headroom are tight.",
            "shipping_impact": "Billable weight keeps this in small-parcel tiers; budget $5–8 per order domestically.",
            "pricing_vs_market": "Sell price sits mid-range versus $15–35 competitors observed in search.",
            "break_even_guidance": "Break even on unit economics after ~40–60 orders if CAC stays under $6.",
            "max_affordable_cac": "$4–6 per order at target 3:1 ROAS",
        },
        "marketing_fit_preview": "Strong TikTok demo potential — full playbook covers organic cadence, paid tests, and creatives.",
        "top_risks": ["Crowded Amazon listings compress price", "Commoditization from AliExpress clones"],
        "top_opportunities": ["UGC-friendly before/after demos", "Bundle positioning vs single SKUs"],
        "next_steps": [
            "Order samples and film 3 short demo clips",
            "Validate $25–30 price point with a landing page test",
            "Check billable weight with your 3PL quote",
        ],
        "marketing_plan": _sample_marketing_plan(),
        "go_to_market_strategy": "## Phase 1\nValidate creative on TikTok before scaling paid.",
    }


def test_product_evaluation_response_validates():
    result = ProductEvaluationResponse.model_validate(normalize_evaluation_payload(_sample_payload()))
    assert result.final_score == 69
    assert result.market_research.demand_estimate.level == "Medium"
    assert len(result.marketing_plan.platform_recommendations) == 3


def test_product_evaluation_rejects_invalid_score():
    payload = _sample_payload()
    payload["final_score"] = 101
    with pytest.raises(ValidationError):
        ProductEvaluationResponse.model_validate(payload)


def test_product_evaluation_json_roundtrip():
    result = ProductEvaluationResponse.model_validate(normalize_evaluation_payload(_sample_payload()))
    restored = ProductEvaluationResponse.model_validate_json(result.model_dump_json())
    assert restored.final_score == result.final_score
