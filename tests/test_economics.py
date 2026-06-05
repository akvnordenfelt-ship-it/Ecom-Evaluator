"""Tests for economics calculations."""

from ecom_evaluator.economics import compute_economics_snapshot


def test_compute_economics_snapshot_margin():
    snap = compute_economics_snapshot(
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
    )
    assert snap.gross_margin_usd == 15.0
    assert snap.gross_margin_pct == 75.0
    assert snap.billable_weight_kg >= 0.4


def test_dimensional_weight_can_exceed_actual():
    snap = compute_economics_snapshot(
        purchase_price=3.0,
        sales_price=15.0,
        weight_kg=0.2,
        length_cm=40,
        width_cm=30,
        height_cm=20,
    )
    assert snap.dimensional_weight_kg > snap.actual_weight_kg
    assert snap.billable_weight_kg == snap.dimensional_weight_kg
