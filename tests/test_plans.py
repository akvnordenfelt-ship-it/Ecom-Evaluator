"""Tests for subscription plan configuration."""

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier, UNLIMITED_EVALUATIONS, coerce_plan_tier, get_plan_config, plan_has_unlimited_evaluations


def test_plan_pricing_and_quotas():
    assert get_plan_config(PlanTier.PREMIUM).price_usd_monthly == 29
    assert plan_has_unlimited_evaluations(PlanTier.PREMIUM)


def test_free_plan_has_no_premium_features():
    free = PLAN_CONFIG[PlanTier.FREE]
    assert free.monthly_evaluations == 1
    assert not free.runs_web_search
    assert not free.runs_marketing_teaser
    assert not free.runs_marketing_deep_dive


def test_premium_runs_all_features():
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    assert premium.runs_web_search
    assert premium.runs_marketing_teaser
    assert premium.runs_marketing_deep_dive
    assert premium.monthly_evaluations == UNLIMITED_EVALUATIONS


def test_legacy_pro_maps_to_premium():
    assert coerce_plan_tier("pro") == PlanTier.PREMIUM
