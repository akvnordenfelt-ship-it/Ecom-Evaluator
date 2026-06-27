"""Pydantic schemas — lightweight strings from LLM, strict types after normalization."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class FreeCorePayload(BaseModel):
    """Sections 1–2 from Gemini Flash (free tier core)."""

    overall_score: int = Field(ge=0, le=100)
    product_profile_summary: str = Field(min_length=1)
    physical_weight_assessment: str = Field(min_length=1)
    fragility_assessment: str = Field(min_length=1)
    variant_complexity: str = Field(min_length=1)
    shipping_complexity: str = Field(min_length=1)
    metric_market_saturation: int = Field(ge=0, le=100)
    metric_market_saturation_note: str = Field(min_length=1)
    metric_marketing_velocity: int = Field(ge=0, le=100)
    metric_marketing_velocity_note: str = Field(min_length=1)
    metric_logistics_margin: int = Field(ge=0, le=100)
    metric_logistics_margin_note: str = Field(min_length=1)
    metric_seasonality: int = Field(ge=0, le=100)
    metric_seasonality_note: str = Field(min_length=1)
    metric_brandability: int = Field(ge=0, le=100)
    metric_brandability_note: str = Field(min_length=1)
    red_flag_headline: str = Field(min_length=1)
    red_flag_analysis: str = Field(min_length=1)
    red_flag_1: str = Field(min_length=1)
    red_flag_2: str = Field(min_length=1)
    red_flag_3: str = Field(min_length=1)


class MarketingTeaserPayload(BaseModel):
    marketing_primary_channel: str = Field(min_length=1)
    scroll_stopping_hook_index: int = Field(ge=1, le=10)
    buyer_persona_hint: str = Field(min_length=1)
    marketing_teaser: str = Field(min_length=1)


class AdScriptFramework(BaseModel):
    platform: str = Field(min_length=1)
    hook: str = Field(min_length=1)
    body: str = Field(min_length=1)
    cta: str = Field(min_length=1)


class MarketingBlueprintPayload(MarketingTeaserPayload):
    """Section 4 — full marketing brief (Premium, Claude Sonnet)."""

    competitor_ad_angles: list[str] = Field(min_length=2, max_length=5)
    marketing_angles: list[str] = Field(min_length=3, max_length=3)
    ad_script_frameworks: list[AdScriptFramework] = Field(min_length=5, max_length=5)
    targeting_stack: str = Field(min_length=1)
    influencer_dm_templates: list[str] = Field(min_length=3, max_length=3)


class SupplierRecommendation(BaseModel):
    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    price_signal: str = Field(min_length=1)
    moq_signal: str = Field(min_length=1)
    rating_signal: str = Field(min_length=1)


class FinancialVerdictPayload(BaseModel):
    """Section 3 CFO synthesis (Premium, Claude Opus)."""

    financial_verdict: Literal["GO", "NO-GO", "CONDITIONAL GO"]
    financial_verdict_headline: str = Field(min_length=1)
    cfo_summary: str = Field(min_length=1)
    financial_conditions: list[str] = Field(min_length=2, max_length=5)
    financial_key_risks: list[str] = Field(min_length=2, max_length=5)


class SentimentPainPoint(BaseModel):
    category: str = Field(min_length=1)
    negative_trend: str = Field(min_length=1)
    anger_frustration_index: int = Field(ge=0, le=100)
    review_evidence: str = Field(min_length=1)


class SentimentImprovement(BaseModel):
    linked_category: str = Field(min_length=1)
    engineering_directive: str = Field(min_length=1)
    roi_badge: Literal["High ROI Improvement", "Low-Cost / High-Value"]


class SentimentShopifyHook(BaseModel):
    angle: str = Field(min_length=1)
    copy_block: str = Field(min_length=1)


class ProductEvaluationResponse(FreeCorePayload):
    """Full evaluation report — sections 1–3 free; 4–6 unlock by tier."""

    marketing_primary_channel: str | None = None
    scroll_stopping_hook_index: int | None = Field(default=None, ge=1, le=10)
    buyer_persona_hint: str | None = None
    marketing_teaser: str | None = None
    competitor_ad_angles: list[str] | None = None
    marketing_angles: list[str] | None = None
    ad_script_frameworks: list[AdScriptFramework] | None = None
    targeting_stack: str | None = None
    influencer_dm_templates: list[str] | None = None

    financial_verdict: Literal["GO", "NO-GO", "CONDITIONAL GO"] | None = None
    financial_verdict_headline: str | None = None
    cfo_summary: str | None = None
    financial_conditions: list[str] | None = None
    financial_key_risks: list[str] | None = None

    web_intelligence_summary: str | None = None
    web_amazon_snapshot: str | None = None
    web_aliexpress_sourcing: str | None = None
    web_competitor_tracking: str | None = None
    web_sourcing_links: str | None = None
    supplier_recommendations: list[SupplierRecommendation] | None = None
    competitor_price_range: str | None = None
    demand_trend: Literal["rising", "stable", "declining"] | None = None
    market_timing_assessment: str | None = None

    sentiment_executive_summary: str | None = None
    sentiment_pain_points: list[SentimentPainPoint] | None = None
    sentiment_improvement_directives: list[SentimentImprovement] | None = None
    sentiment_shopify_hooks: list[SentimentShopifyHook] | None = None
    category_sentiment_score: int | None = Field(default=None, ge=0, le=100)
    praised_features: list[str] | None = None
    unmet_needs: list[str] | None = None

    def has_marketing_teaser(self) -> bool:
        return bool(self.marketing_primary_channel and self.marketing_teaser)

    def has_marketing_blueprint(self) -> bool:
        return self.has_marketing_teaser() and bool(self.marketing_angles)

    def has_financial_verdict(self) -> bool:
        return bool(self.financial_verdict and self.cfo_summary)

    def has_web_intelligence(self) -> bool:
        return bool(self.web_intelligence_summary)

    def has_competitor_sentiment(self) -> bool:
        return bool(self.sentiment_pain_points)


class WebIntelligencePayload(BaseModel):
    web_intelligence_summary: str = Field(min_length=1)
    web_amazon_snapshot: str = Field(min_length=1)
    web_aliexpress_sourcing: str = Field(min_length=1)
    web_competitor_tracking: str = Field(min_length=1)
    web_sourcing_links: str = Field(min_length=1)
    supplier_recommendations: list[SupplierRecommendation] = Field(min_length=2, max_length=3)
    competitor_price_range: str = Field(min_length=1)
    demand_trend: Literal["rising", "stable", "declining"]
    market_timing_assessment: str = Field(min_length=1)


class CompetitorSentimentPayload(BaseModel):
    sentiment_executive_summary: str = Field(min_length=1)
    category_sentiment_score: int = Field(ge=0, le=100)
    praised_features: list[str] = Field(min_length=3, max_length=5)
    unmet_needs: list[str] = Field(min_length=2, max_length=4)
    sentiment_pain_points: list[SentimentPainPoint] = Field(min_length=3, max_length=3)
    sentiment_improvement_directives: list[SentimentImprovement] = Field(min_length=3, max_length=3)
    sentiment_shopify_hooks: list[SentimentShopifyHook] = Field(min_length=2, max_length=3)


class MarketSearchHit(TypedDict):
    channel: str
    query: str
    title: str
    url: str
    snippet: str
