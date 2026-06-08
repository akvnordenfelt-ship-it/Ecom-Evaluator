"""Subscription plans, evaluation quotas, and AI tier routing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ecom_evaluator.config import GEMINI_MODEL, GEMINI_PRO_MODEL

UNLIMITED_EVALUATIONS = 999_999


class PlanTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


@dataclass(frozen=True)
class PlanConfig:
    tier: PlanTier
    label: str
    price_usd_monthly: int
    monthly_evaluations: int
    ai_model_label: str
    gemini_model: str
    gemini_pro_model: str
    runs_web_search: bool
    runs_marketing_teaser: bool
    runs_marketing_deep_dive: bool
    core_max_tokens: int
    premium_max_tokens: int
    web_search_max_results: int


PLAN_CONFIG: dict[PlanTier, PlanConfig] = {
    PlanTier.FREE: PlanConfig(
        tier=PlanTier.FREE,
        label="Free",
        price_usd_monthly=0,
        monthly_evaluations=1,
        ai_model_label="Fast product analysis",
        gemini_model=GEMINI_MODEL,
        gemini_pro_model=GEMINI_PRO_MODEL,
        runs_web_search=False,
        runs_marketing_teaser=False,
        runs_marketing_deep_dive=False,
        core_max_tokens=4096,
        premium_max_tokens=0,
        web_search_max_results=0,
    ),
    PlanTier.PREMIUM: PlanConfig(
        tier=PlanTier.PREMIUM,
        label="Premium",
        price_usd_monthly=29,
        monthly_evaluations=UNLIMITED_EVALUATIONS,
        ai_model_label="Full platform · advanced commercial AI engine",
        gemini_model=GEMINI_MODEL,
        gemini_pro_model=GEMINI_PRO_MODEL,
        runs_web_search=True,
        runs_marketing_teaser=True,
        runs_marketing_deep_dive=True,
        core_max_tokens=4096,
        premium_max_tokens=8192,
        web_search_max_results=4,
    ),
}


def coerce_plan_tier(tier: PlanTier | str) -> PlanTier:
    if isinstance(tier, str):
        if tier == "pro":
            return PlanTier.PREMIUM
        return PlanTier(tier)
    return tier


def get_plan_config(tier: PlanTier | str) -> PlanConfig:
    return PLAN_CONFIG[coerce_plan_tier(tier)]


def plan_has_unlimited_evaluations(tier: PlanTier | str) -> bool:
    return get_plan_config(tier).monthly_evaluations >= UNLIMITED_EVALUATIONS
