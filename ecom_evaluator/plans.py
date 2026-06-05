"""Subscription plans, evaluation quotas, and AI tier routing."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ecom_evaluator.config import GEMINI_MODEL


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
    includes_premium_sections: bool
    web_search_max_results: int
    core_max_tokens: int
    marketing_max_tokens: int
    extra_eval_note: str


PLAN_CONFIG: dict[PlanTier, PlanConfig] = {
    PlanTier.FREE: PlanConfig(
        tier=PlanTier.FREE,
        label="Free",
        price_usd_monthly=0,
        monthly_evaluations=1,
        ai_model_label="Gemini 2.5 Flash",
        gemini_model=GEMINI_MODEL,
        includes_premium_sections=False,
        web_search_max_results=3,
        core_max_tokens=8192,
        marketing_max_tokens=0,
        extra_eval_note="Upgrade for full reports",
    ),
    PlanTier.PREMIUM: PlanConfig(
        tier=PlanTier.PREMIUM,
        label="Premium",
        price_usd_monthly=29,
        monthly_evaluations=20,
        ai_model_label="Gemini 2.5 Flash",
        gemini_model=GEMINI_MODEL,
        includes_premium_sections=True,
        web_search_max_results=4,
        core_max_tokens=8192,
        marketing_max_tokens=8192,
        extra_eval_note="Add-on evaluations available (pricing TBD)",
    ),
    PlanTier.PRO: PlanConfig(
        tier=PlanTier.PRO,
        label="Pro",
        price_usd_monthly=79,
        monthly_evaluations=100,
        ai_model_label="Gemini 2.5 Flash",
        gemini_model=GEMINI_MODEL,
        includes_premium_sections=True,
        web_search_max_results=4,
        core_max_tokens=8192,
        marketing_max_tokens=8192,
        extra_eval_note="Lowest add-on eval pricing (TBD)",
    ),
}


def get_plan_config(tier: PlanTier | str) -> PlanConfig:
    if isinstance(tier, str):
        tier = PlanTier(tier)
    return PLAN_CONFIG[tier]


def includes_premium_sections(tier: PlanTier | str) -> bool:
    return get_plan_config(tier).includes_premium_sections
