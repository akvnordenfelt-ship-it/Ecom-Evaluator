"""Tests for SaaS subscription helpers."""

from ecom_evaluator.plans import PlanTier
from ecom_evaluator.ui.subscription import can_run_evaluation, consume_evaluation


def test_can_run_evaluation_with_quota():
    assert can_run_evaluation(evaluations_left=1, tier=PlanTier.FREE)
    assert not can_run_evaluation(evaluations_left=0, tier=PlanTier.FREE)


def test_can_run_evaluation_premium_with_quota():
    assert can_run_evaluation(evaluations_left=5, tier=PlanTier.PREMIUM)
    assert not can_run_evaluation(evaluations_left=0, tier=PlanTier.PREMIUM)


def test_consume_evaluation():
    assert consume_evaluation(evaluations_left=1, tier=PlanTier.FREE) == 0
    assert consume_evaluation(evaluations_left=20, tier=PlanTier.PREMIUM) == 19
    assert consume_evaluation(evaluations_left=100, tier=PlanTier.PRO) == 99
