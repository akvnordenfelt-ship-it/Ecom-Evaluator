"""Tests for subscription plan configuration."""

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier, get_plan_config, includes_premium_sections


def test_plan_pricing_and_quotas():
    assert get_plan_config(PlanTier.PREMIUM).price_usd_monthly == 29
    assert get_plan_config(PlanTier.PREMIUM).monthly_evaluations == 20
    assert get_plan_config(PlanTier.PRO).price_usd_monthly == 79
    assert get_plan_config(PlanTier.PRO).monthly_evaluations == 100


def test_free_plan_is_cheap():
    free = PLAN_CONFIG[PlanTier.FREE]
    assert free.monthly_evaluations == 1
    assert not free.includes_premium_sections
    assert free.core_max_tokens >= 4096


def test_premium_sections_only_on_paid():
    assert not includes_premium_sections(PlanTier.FREE)
    assert includes_premium_sections(PlanTier.PREMIUM)
    assert includes_premium_sections(PlanTier.PRO)
