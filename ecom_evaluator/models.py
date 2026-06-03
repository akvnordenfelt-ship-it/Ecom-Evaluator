"""Pydantic schemas for Gemini structured output."""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class ScoredDimension(BaseModel):
    score: int = Field(ge=0, le=100)
    motivation: str = Field(min_length=1)


class MarketSaturation(BaseModel):
    level: Literal["Low", "Medium", "High"]
    motivation: str = Field(min_length=1)


class TikTokHook(BaseModel):
    hook_text: str = Field(min_length=1)
    visuals: str = Field(min_length=1)
    voiceover: str = Field(min_length=1)


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
    key_competitors: list[CompetitorListing] = Field(default_factory=list, max_length=8)
    strategic_implications: str = Field(min_length=1)
    data_limitations: str = Field(min_length=1)


class ProductEvaluationResponse(BaseModel):
    final_score: int = Field(ge=0, le=100)
    market_research: MarketResearchAnalysis
    short_term_potential: ScoredDimension
    long_term_stability: ScoredDimension
    scalability: ScoredDimension
    marketing_suitability: ScoredDimension
    market_saturation: MarketSaturation
    estimated_shipping_category: str = Field(min_length=1)
    tiktok_hooks: list[TikTokHook] = Field(min_length=3, max_length=3)
    go_to_market_strategy: str = Field(min_length=1)


class MarketSearchHit(TypedDict):
    channel: str
    query: str
    title: str
    url: str
    snippet: str
