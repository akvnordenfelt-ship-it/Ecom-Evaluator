"""Tests for subscription plan configuration."""

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier, get_plan_config


def test_plan_pricing_and_quotas():
    assert get_plan_config(PlanTier.PREMIUM).price_usd_monthly == 29
    assert get_plan_config(PlanTier.PREMIUM).monthly_evaluations == 20
    assert get_plan_config(PlanTier.PRO).price_usd_monthly == 79
    assert get_plan_config(PlanTier.PRO).monthly_evaluations == 100


def test_free_plan_has_no_web_search():
    free = PLAN_CONFIG[PlanTier.FREE]
    assert free.monthly_evaluations == 1
    assert not free.runs_web_search
    assert not free.runs_marketing_teaser
    assert not free.runs_marketing_deep_dive


def test_premium_runs_web_search_and_teaser():
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    assert premium.runs_web_search
    assert premium.runs_marketing_teaser
    assert not premium.runs_marketing_deep_dive


def test_pro_runs_all_premium_features():
    pro = PLAN_CONFIG[PlanTier.PRO]
    assert pro.runs_web_search
    assert pro.runs_marketing_teaser
    assert pro.runs_marketing_deep_dive
