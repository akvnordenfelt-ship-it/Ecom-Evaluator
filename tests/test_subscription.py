"""Tests for SaaS subscription helpers."""

from ecom_evaluator.ui.subscription import can_run_evaluation, consume_evaluation


def test_can_run_evaluation_free_tier():
    assert can_run_evaluation(evaluations_left=1, is_premium=False)
    assert not can_run_evaluation(evaluations_left=0, is_premium=False)


def test_can_run_evaluation_premium():
    assert can_run_evaluation(evaluations_left=0, is_premium=True)


def test_consume_evaluation():
    assert consume_evaluation(evaluations_left=1, is_premium=False) == 0
    assert consume_evaluation(evaluations_left=2, is_premium=True) == 2
