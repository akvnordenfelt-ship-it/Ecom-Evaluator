"""Subscription plans, evaluation quotas, and AI tier routing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ecom_evaluator.config import GEMINI_MODEL, GEMINI_PRO_MODEL


class PlanTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"


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
        ai_model_label="Gemini 2.5 Flash",
        gemini_model=GEMINI_MODEL,
        gemini_pro_model=GEMINI_PRO_MODEL,
        runs_web_search=False,
        runs_marketing_deep_dive=False,
        core_max_tokens=4096,
        premium_max_tokens=0,
        web_search_max_results=0,
    ),
    PlanTier.PREMIUM: PlanConfig(
        tier=PlanTier.PREMIUM,
        label="Premium",
        price_usd_monthly=29,
        monthly_evaluations=20,
        ai_model_label="Gemini 2.5 Flash + Live Web Search",
        gemini_model=GEMINI_MODEL,
        gemini_pro_model=GEMINI_PRO_MODEL,
        runs_web_search=True,
        runs_marketing_deep_dive=False,
        core_max_tokens=4096,
        premium_max_tokens=8192,
        web_search_max_results=4,
    ),
    PlanTier.PRO: PlanConfig(
        tier=PlanTier.PRO,
        label="Pro",
        price_usd_monthly=79,
        monthly_evaluations=100,
        ai_model_label="Gemini 2.5 Pro Marketing Engine",
        gemini_model=GEMINI_MODEL,
        gemini_pro_model=GEMINI_PRO_MODEL,
        runs_web_search=True,
        runs_marketing_deep_dive=True,
        core_max_tokens=4096,
        premium_max_tokens=8192,
        web_search_max_results=4,
    ),
}


def get_plan_config(tier: PlanTier | str) -> PlanConfig:
    if isinstance(tier, str):
        tier = PlanTier(tier)
    return PLAN_CONFIG[tier]
