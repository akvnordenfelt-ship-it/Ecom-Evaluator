"""Deterministic unit economics from product form inputs."""

from __future__ import annotations

from dataclasses import dataclass

LIGHTWEIGHT_BASELINE_WEIGHT_KG = 0.15
LIGHTWEIGHT_BASELINE_LENGTH_CM = 15.0
LIGHTWEIGHT_BASELINE_WIDTH_CM = 10.0
LIGHTWEIGHT_BASELINE_HEIGHT_CM = 5.0
DEFAULT_SALES_PRICE_MULTIPLIER = 3.0


@dataclass(frozen=True)
class ResolvedProductInputs:
    purchase_price: float
    sales_price: float
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float
    used_physical_baseline: bool
    used_sales_price_estimate: bool


def resolve_product_inputs(
    *,
    purchase_price: float,
    sales_price: float,
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> ResolvedProductInputs:
    """Apply lightweight-package and selling-price defaults when inputs are missing."""
    used_physical_baseline = False
    resolved_weight = weight_kg
    resolved_length = length_cm
    resolved_width = width_cm
    resolved_height = height_cm

    if weight_kg <= 0 and length_cm <= 0 and width_cm <= 0 and height_cm <= 0:
        resolved_weight = LIGHTWEIGHT_BASELINE_WEIGHT_KG
        resolved_length = LIGHTWEIGHT_BASELINE_LENGTH_CM
        resolved_width = LIGHTWEIGHT_BASELINE_WIDTH_CM
        resolved_height = LIGHTWEIGHT_BASELINE_HEIGHT_CM
        used_physical_baseline = True

    used_sales_price_estimate = False
    resolved_sales_price = sales_price
    if sales_price <= 0 and purchase_price > 0:
        resolved_sales_price = round(purchase_price * DEFAULT_SALES_PRICE_MULTIPLIER, 2)
        used_sales_price_estimate = True

    return ResolvedProductInputs(
        purchase_price=purchase_price,
        sales_price=resolved_sales_price,
        weight_kg=resolved_weight,
        length_cm=resolved_length,
        width_cm=resolved_width,
        height_cm=resolved_height,
        used_physical_baseline=used_physical_baseline,
        used_sales_price_estimate=used_sales_price_estimate,
    )


@dataclass(frozen=True)
class EconomicsSnapshot:
    purchase_price: float
    sales_price: float
    gross_margin_usd: float
    gross_margin_pct: float
    volume_dm3: float
    actual_weight_kg: float
    dimensional_weight_kg: float
    billable_weight_kg: float
    shipping_band_usd: tuple[float, float]
    contribution_margin_usd: float
    contribution_margin_pct: float
    max_cac_30pct_margin: float
    max_cac_20pct_margin: float
    shipping_tier_label: str


def billable_weight_kg(
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> tuple[float, float, float]:
    volume_cm3 = length_cm * width_cm * height_cm
    volume_dm3 = volume_cm3 / 1000
    dimensional_weight_kg = volume_cm3 / 5000 if volume_cm3 > 0 else 0.0
    billable = max(weight_kg, dimensional_weight_kg)
    return volume_dm3, dimensional_weight_kg, billable


def estimate_shipping_band_usd(billable_kg: float, volume_dm3: float) -> tuple[float, float, str]:
    if billable_kg <= 0 and volume_dm3 <= 0:
        return (3.5, 6.5, "Light mail / small envelope (estimated baseline)")
    if billable_kg <= 0.2 and volume_dm3 <= 1.0:
        return (3.5, 6.5, "Light mail / small envelope")
    if billable_kg <= 0.5:
        return (4.5, 8.0, "Small parcel")
    if billable_kg <= 1.0:
        return (7.0, 12.0, "Standard parcel")
    if billable_kg <= 2.0:
        return (10.0, 16.0, "Mid-weight parcel")
    if billable_kg <= 5.0:
        return (14.0, 24.0, "Heavy parcel")
    return (22.0, 38.0, "Oversize / freight zone")


def compute_economics_snapshot(
    *,
    purchase_price: float,
    sales_price: float,
    weight_kg: float,
    length_cm: float,
    width_cm: float,
    height_cm: float,
) -> EconomicsSnapshot:
    gross_margin_usd = sales_price - purchase_price
    gross_margin_pct = (gross_margin_usd / sales_price * 100) if sales_price > 0 else 0.0
    volume_dm3, dimensional_weight_kg, billable = billable_weight_kg(
        weight_kg, length_cm, width_cm, height_cm
    )
    ship_low, ship_high, tier_label = estimate_shipping_band_usd(billable, volume_dm3)
    ship_mid = (ship_low + ship_high) / 2
    contribution = gross_margin_usd - ship_mid
    contribution_pct = (contribution / sales_price * 100) if sales_price > 0 else 0.0

    return EconomicsSnapshot(
        purchase_price=purchase_price,
        sales_price=sales_price,
        gross_margin_usd=gross_margin_usd,
        gross_margin_pct=gross_margin_pct,
        volume_dm3=volume_dm3,
        actual_weight_kg=weight_kg,
        dimensional_weight_kg=dimensional_weight_kg,
        billable_weight_kg=billable,
        shipping_band_usd=(ship_low, ship_high),
        contribution_margin_usd=contribution,
        contribution_margin_pct=contribution_pct,
        max_cac_30pct_margin=max(0.0, gross_margin_usd * 0.30),
        max_cac_20pct_margin=max(0.0, gross_margin_usd * 0.20),
        shipping_tier_label=tier_label,
    )


@dataclass(frozen=True)
class FinancialSummary:
    gross_margin_usd: float
    gross_margin_pct: float
    roi_pct: float
    break_even_cpa: float
    shipping_per_unit_usd: float


@dataclass(frozen=True)
class ScalingMatrixRow:
    units_per_month: int
    gross_revenue: float
    total_product_cost: float
    total_shipping: float
    net_profit: float
    net_profit_stressed: float


def compute_financial_summary(econ: EconomicsSnapshot) -> FinancialSummary:
    ship_mid = (econ.shipping_band_usd[0] + econ.shipping_band_usd[1]) / 2
    roi = (econ.gross_margin_usd / econ.purchase_price * 100) if econ.purchase_price > 0 else 0.0
    break_even_cpa = max(0.0, econ.contribution_margin_usd)
    return FinancialSummary(
        gross_margin_usd=econ.gross_margin_usd,
        gross_margin_pct=econ.gross_margin_pct,
        roi_pct=roi,
        break_even_cpa=break_even_cpa,
        shipping_per_unit_usd=ship_mid,
    )


def compute_scaling_matrix(econ: EconomicsSnapshot) -> list[ScalingMatrixRow]:
    ship_mid = (econ.shipping_band_usd[0] + econ.shipping_band_usd[1]) / 2
    stressed_ship = ship_mid * 1.2
    rows: list[ScalingMatrixRow] = []
    for units in (100, 500, 1000):
        gross = econ.sales_price * units
        cogs = econ.purchase_price * units
        shipping = ship_mid * units
        stressed_shipping = stressed_ship * units
        rows.append(
            ScalingMatrixRow(
                units_per_month=units,
                gross_revenue=gross,
                total_product_cost=cogs,
                total_shipping=shipping,
                net_profit=gross - cogs - shipping,
                net_profit_stressed=gross - cogs - stressed_shipping,
            )
        )
    return rows
