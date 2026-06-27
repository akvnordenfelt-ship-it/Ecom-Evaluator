"""Deterministic unit economics from product form inputs."""

from __future__ import annotations

from dataclasses import dataclass

LIGHTWEIGHT_BASELINE_WEIGHT_KG = 0.15
LIGHTWEIGHT_BASELINE_LENGTH_CM = 15.0
LIGHTWEIGHT_BASELINE_WIDTH_CM = 10.0
LIGHTWEIGHT_BASELINE_HEIGHT_CM = 5.0
DEFAULT_SALES_PRICE_MULTIPLIER = 3.0

SALES_PLATFORMS = ("shopify", "amazon", "tiktok")
PLATFORM_LABELS = {
    "shopify": "Shopify / DTC",
    "amazon": "Amazon FBA",
    "tiktok": "TikTok Shop",
}
# Simplified all-in fee rates (payment + platform referral). Tune per your actual fee stack.
PLATFORM_FEE_RATES: dict[str, float] = {
    "shopify": 0.029,
    "amazon": 0.15,
    "tiktok": 0.08,
}


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
    platform_fee_usd: float
    platform_fee_pct: float
    net_margin_usd: float
    net_margin_pct: float
    break_even_cpa_net: float


@dataclass(frozen=True)
class PlatformEconomicsRow:
    platform: str
    platform_label: str
    fee_rate_pct: float
    platform_fee_usd: float
    net_margin_usd: float
    net_margin_pct: float
    break_even_cpa: float


@dataclass(frozen=True)
class ScalingMatrixRow:
    units_per_month: int
    gross_revenue: float
    total_product_cost: float
    total_shipping: float
    net_profit: float
    net_profit_stressed: float


def compute_platform_economics(econ: EconomicsSnapshot, platform: str = "shopify") -> PlatformEconomicsRow:
    key = platform if platform in PLATFORM_FEE_RATES else "shopify"
    fee_rate = PLATFORM_FEE_RATES[key]
    ship_mid = (econ.shipping_band_usd[0] + econ.shipping_band_usd[1]) / 2
    platform_fee = econ.sales_price * fee_rate if econ.sales_price > 0 else 0.0
    net_margin = econ.gross_margin_usd - ship_mid - platform_fee
    net_pct = (net_margin / econ.sales_price * 100) if econ.sales_price > 0 else 0.0
    return PlatformEconomicsRow(
        platform=key,
        platform_label=PLATFORM_LABELS[key],
        fee_rate_pct=fee_rate * 100,
        platform_fee_usd=platform_fee,
        net_margin_usd=net_margin,
        net_margin_pct=net_pct,
        break_even_cpa=max(0.0, net_margin),
    )


def compute_all_platform_economics(econ: EconomicsSnapshot) -> list[PlatformEconomicsRow]:
    return [compute_platform_economics(econ, platform) for platform in SALES_PLATFORMS]


def format_economics_for_verdict(
    *,
    econ: EconomicsSnapshot,
    fin: FinancialSummary,
    matrix: list[ScalingMatrixRow],
    platform_rows: list[PlatformEconomicsRow],
) -> str:
    ship_low, ship_high = econ.shipping_band_usd
    lines = [
        "## Python-computed unit economics (authoritative — do not recalculate)",
        f"- Purchase: ${econ.purchase_price:.2f} | Sell: ${econ.sales_price:.2f}",
        f"- Gross margin: ${econ.gross_margin_usd:.2f} ({econ.gross_margin_pct:.1f}%)",
        f"- Est. shipping: ${ship_low:.2f}–${ship_high:.2f} (mid ${fin.shipping_per_unit_usd:.2f})",
        f"- Contribution after shipping: ${econ.contribution_margin_usd:.2f}",
        f"- ROI on product cost: {fin.roi_pct:.1f}%",
        f"- Break-even CPA (after shipping): ${fin.break_even_cpa:.2f}",
        "",
        "## Platform fees & net margin (Shopify default)",
        f"- Platform fee: ${fin.platform_fee_usd:.2f} ({fin.platform_fee_pct:.1f}%)",
        f"- Net margin after shipping + fees: ${fin.net_margin_usd:.2f} ({fin.net_margin_pct:.1f}%)",
        f"- Break-even CPA (net): ${fin.break_even_cpa_net:.2f}",
        "",
        "## All platforms",
    ]
    for row in platform_rows:
        lines.append(
            f"- {row.platform_label}: fee {row.fee_rate_pct:.1f}% → "
            f"net ${row.net_margin_usd:.2f}/unit ({row.net_margin_pct:.1f}%), "
            f"break-even CPA ${row.break_even_cpa:.2f}"
        )
    lines.append("")
    lines.append("## Volume scaling matrix (100 / 500 / 1000 units per month)")
    for row in matrix:
        lines.append(
            f"- {row.units_per_month} units: revenue ${row.gross_revenue:,.0f}, "
            f"net profit ${row.net_profit:,.0f} (stressed shipping +20%: ${row.net_profit_stressed:,.0f})"
        )
    return "\n".join(lines)


def compute_financial_summary(econ: EconomicsSnapshot, platform: str = "shopify") -> FinancialSummary:
    ship_mid = (econ.shipping_band_usd[0] + econ.shipping_band_usd[1]) / 2
    roi = (econ.gross_margin_usd / econ.purchase_price * 100) if econ.purchase_price > 0 else 0.0
    break_even_cpa = max(0.0, econ.contribution_margin_usd)
    platform_row = compute_platform_economics(econ, platform)
    return FinancialSummary(
        gross_margin_usd=econ.gross_margin_usd,
        gross_margin_pct=econ.gross_margin_pct,
        roi_pct=roi,
        break_even_cpa=break_even_cpa,
        shipping_per_unit_usd=ship_mid,
        platform_fee_usd=platform_row.platform_fee_usd,
        platform_fee_pct=platform_row.fee_rate_pct,
        net_margin_usd=platform_row.net_margin_usd,
        net_margin_pct=platform_row.net_margin_pct,
        break_even_cpa_net=platform_row.break_even_cpa,
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
