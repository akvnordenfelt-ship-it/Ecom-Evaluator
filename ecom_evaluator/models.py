"""Pydantic schemas — lightweight strings from LLM, strict types after normalization."""

from __future__ import annotations

from typing import TypedDict

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


class ProductEvaluationResponse(FreeCorePayload):
    """Full evaluation report — sections 1–3 free; 4–6 unlock by tier."""

    marketing_primary_channel: str | None = None
    scroll_stopping_hook_index: int | None = Field(default=None, ge=1, le=10)
    buyer_persona_hint: str | None = None
    marketing_teaser: str | None = None

    web_intelligence_summary: str | None = None
    web_amazon_snapshot: str | None = None
    web_aliexpress_sourcing: str | None = None
    web_competitor_tracking: str | None = None
    web_sourcing_links: str | None = None

    marketing_ad_scripts: str | None = None
    marketing_targeting_blueprint: str | None = None
    marketing_influencer_templates: str | None = None
    marketing_positioning_matrix: str | None = None

    def has_marketing_teaser(self) -> bool:
        return bool(self.marketing_primary_channel and self.marketing_teaser)

    def has_web_intelligence(self) -> bool:
        return bool(self.web_intelligence_summary)

    def has_marketing_deep_dive(self) -> bool:
        return bool(self.marketing_ad_scripts)


class WebIntelligencePayload(BaseModel):
    web_intelligence_summary: str = Field(min_length=1)
    web_amazon_snapshot: str = Field(min_length=1)
    web_aliexpress_sourcing: str = Field(min_length=1)
    web_competitor_tracking: str = Field(min_length=1)
    web_sourcing_links: str = Field(min_length=1)


class MarketingDeepDivePayload(BaseModel):
    marketing_ad_scripts: str = Field(min_length=1)
    marketing_targeting_blueprint: str = Field(min_length=1)
    marketing_influencer_templates: str = Field(min_length=1)
    marketing_positioning_matrix: str = Field(min_length=1)


class MarketSearchHit(TypedDict):
    channel: str
    query: str
    title: str
    url: str
    snippet: str
