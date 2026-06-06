"""Tests for economics calculations."""

from ecom_evaluator.economics import (
    compute_economics_snapshot,
    compute_financial_summary,
    compute_scaling_matrix,
)


def test_high_markup_light_product():
    snap = compute_economics_snapshot(
        purchase_price=0.10,
        sales_price=10.0,
        weight_kg=0.05,
        length_cm=10,
        width_cm=8,
        height_cm=3,
    )
    assert snap.gross_margin_pct > 90


def test_scaling_matrix_stress_test():
    snap = compute_economics_snapshot(
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
    )
    rows = compute_scaling_matrix(snap)
    assert len(rows) == 3
    assert rows[0].net_profit_stressed < rows[0].net_profit


def test_financial_summary_break_even_cpa():
    snap = compute_economics_snapshot(
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
    )
    fin = compute_financial_summary(snap)
    assert fin.break_even_cpa >= 0
