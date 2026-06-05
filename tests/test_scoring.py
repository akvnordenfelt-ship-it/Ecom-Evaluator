"""Tests for score reconciliation."""

from ecom_evaluator.models import ScoredDimension
from ecom_evaluator.scoring import dimension_average, reconcile_final_score


def _dim(score: int) -> ScoredDimension:
    return ScoredDimension(score=score, motivation="test")


def test_reconcile_final_score_matches_dimension_average():
    final = reconcile_final_score(8, _dim(10), _dim(12), _dim(9), _dim(11))
    assert final == 10


def test_reconcile_ignores_mismatched_llm_final():
    final = reconcile_final_score(8, _dim(50), _dim(50), _dim(50), _dim(50))
    assert final == 50


def test_dimension_average():
    assert dimension_average(_dim(10), _dim(20), _dim(30), _dim(40)) == 25
