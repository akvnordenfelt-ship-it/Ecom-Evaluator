"""Deterministic unit economics from product form inputs."""

from __future__ import annotations

from dataclasses import dataclass


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
        return (5.0, 9.0, "Unknown — confirm with carrier")
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
