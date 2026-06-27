"""Tests for economics calculations."""

from ecom_evaluator.economics import (
    compute_economics_snapshot,
    compute_financial_summary,
    compute_scaling_matrix,
    resolve_product_inputs,
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


def test_platform_economics_net_margin():
    from ecom_evaluator.economics import compute_all_platform_economics, compute_economics_snapshot

    snap = compute_economics_snapshot(
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
    )
    rows = compute_all_platform_economics(snap)
    assert len(rows) == 3
    amazon = next(row for row in rows if row.platform == "amazon")
    shopify = next(row for row in rows if row.platform == "shopify")
    assert amazon.net_margin_usd < shopify.net_margin_usd


def test_financial_summary_includes_net_margin():
    snap = compute_economics_snapshot(
        purchase_price=5.0,
        sales_price=20.0,
        weight_kg=0.4,
        length_cm=20,
        width_cm=10,
        height_cm=5,
    )
    fin = compute_financial_summary(snap)
    assert fin.net_margin_usd < fin.gross_margin_usd
    assert fin.break_even_cpa_net <= fin.break_even_cpa


def test_resolve_product_inputs_applies_baselines():
    resolved = resolve_product_inputs(
        purchase_price=2.0,
        sales_price=0.0,
        weight_kg=0.0,
        length_cm=0.0,
        width_cm=0.0,
        height_cm=0.0,
    )
    assert resolved.used_physical_baseline
    assert resolved.used_sales_price_estimate
    assert resolved.sales_price == 6.0
    assert resolved.weight_kg > 0
