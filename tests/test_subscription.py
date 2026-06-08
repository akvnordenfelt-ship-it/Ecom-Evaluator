"""Tests for subscription helpers."""

from ecom_evaluator.plans import PlanTier
from ecom_evaluator.ui.subscription import can_run_evaluation, consume_evaluation


def test_free_user_blocked_at_zero():
    assert not can_run_evaluation(evaluations_left=0, tier=PlanTier.FREE)


def test_premium_unlimited_never_blocked():
    assert can_run_evaluation(evaluations_left=0, tier=PlanTier.PREMIUM)


def test_consume_evaluation_free():
    assert consume_evaluation(evaluations_left=1, tier=PlanTier.FREE) == 0


def test_consume_evaluation_premium_unlimited():
    assert consume_evaluation(evaluations_left=999_999, tier=PlanTier.PREMIUM) == 999_999
