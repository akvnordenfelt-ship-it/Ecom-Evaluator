"""Pydantic schemas for LLM structured output."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class ScoredDimension(BaseModel):
    score: int = Field(ge=0, le=100)
    motivation: str = Field(min_length=1)


class MarketSaturation(BaseModel):
    level: Literal["Low", "Medium", "High"]
    motivation: str = Field(min_length=1)


class CompetitorListing(BaseModel):
    platform: Literal["Amazon", "AliExpress", "Independent", "Other"]
    listing_title: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    price_signal: str = Field(min_length=1)
    similarity_note: str = Field(min_length=1)


class DemandEstimate(BaseModel):
    level: Literal["Low", "Medium", "High", "Unknown"]
    estimated_sales_note: str = Field(min_length=1)
    reasoning: str = Field(min_length=1)


class MarketResearchAnalysis(BaseModel):
    executive_summary: str = Field(min_length=1)
    competitor_count_signal: Literal["Few", "Moderate", "Many", "Unknown"]
    amazon_landscape: str = Field(min_length=1)
    aliexpress_landscape: str = Field(min_length=1)
    independent_stores_landscape: str = Field(min_length=1)
    price_range_observed: str = Field(min_length=1)
    demand_estimate: DemandEstimate
    key_competitors: list[CompetitorListing] = Field(default_factory=list, max_length=3)
    strategic_implications: str = Field(min_length=1)
    data_limitations: str = Field(min_length=1)


MarketingPlatform = Literal[
    "TikTok",
    "Instagram",
    "Facebook",
    "YouTube",
    "Google Ads",
    "Amazon Ads",
    "Pinterest",
    "Email/SMS",
    "Other",
]


class TargetAudienceProfile(BaseModel):
    persona_name: str = Field(min_length=1)
    age_range: str = Field(min_length=1)
    psychographics: str = Field(min_length=1)
    pain_points: list[str] = Field(min_length=2, max_length=5)
    platforms_they_use: list[str] = Field(min_length=2, max_length=6)


class OrganicMarketingStrategy(BaseModel):
    overview: str = Field(min_length=1)
    content_formats: list[str] = Field(min_length=2, max_length=5)
    posting_cadence: str = Field(min_length=1)
    creator_angles: list[str] = Field(min_length=2, max_length=4)


class PaidAdsStrategy(BaseModel):
    overview: str = Field(min_length=1)
    primary_channels: list[str] = Field(min_length=1, max_length=4)
    budget_starter_usd: str = Field(min_length=1)
    targeting_approach: str = Field(min_length=1)
    roi_outlook: Literal["Low", "Medium", "High"]


class PlatformRecommendation(BaseModel):
    platform: MarketingPlatform
    fit_score: int = Field(ge=0, le=100)
    roi_potential: Literal["Low", "Medium", "High"]
    organic_vs_paid: Literal["Organic-first", "Paid-first", "Balanced"]
    why_it_works: str = Field(min_length=1)
    competitor_success_signal: str = Field(min_length=1)


class CreativeConcept(BaseModel):
    title: str = Field(min_length=1)
    format: str = Field(min_length=1)
    hook_angle: str = Field(min_length=1)
    script_or_copy: str = Field(min_length=1)
    recommended_platform: str = Field(min_length=1)


class MarketingPlan(BaseModel):
    executive_summary: str = Field(min_length=1)
    target_audience: TargetAudienceProfile
    organic_strategy: OrganicMarketingStrategy
    paid_ads_strategy: PaidAdsStrategy
    platform_recommendations: list[PlatformRecommendation] = Field(min_length=3, max_length=3)
    competitor_marketing_insights: str = Field(min_length=1)
    creative_concepts: list[CreativeConcept] = Field(min_length=2, max_length=2)
    priority_playbook: list[str] = Field(min_length=3, max_length=3)


class ProductEvaluationResponse(BaseModel):
    final_score: int = Field(ge=0, le=100)
    market_research: MarketResearchAnalysis
    short_term_potential: ScoredDimension
    long_term_stability: ScoredDimension
    scalability: ScoredDimension
    marketing_suitability: ScoredDimension
    market_saturation: MarketSaturation
    estimated_shipping_category: str = Field(min_length=1)
    marketing_plan: MarketingPlan
    go_to_market_strategy: str = Field(min_length=1)


class ProductCoreResponse(BaseModel):
    """Phase 1 — scores, market research, logistics."""

    final_score: int = Field(ge=0, le=100)
    market_research: MarketResearchAnalysis
    short_term_potential: ScoredDimension
    long_term_stability: ScoredDimension
    scalability: ScoredDimension
    marketing_suitability: ScoredDimension
    market_saturation: MarketSaturation
    estimated_shipping_category: str = Field(min_length=1)


class MarketingPhaseResponse(BaseModel):
    """Phase 2 — marketing playbook and GTM."""

    marketing_plan: MarketingPlan
    go_to_market_strategy: str = Field(min_length=1)


class MarketSearchHit(TypedDict):
    channel: str
    query: str
    title: str
    url: str
    snippet: str
