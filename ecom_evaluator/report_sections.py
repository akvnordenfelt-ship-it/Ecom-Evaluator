"""Six report sections and tier access rules."""

from __future__ import annotations

from dataclasses import dataclass

from ecom_evaluator.plans import PlanTier, coerce_plan_tier


@dataclass(frozen=True)
class ReportSection:
    id: str
    number: int
    title: str
    eyebrow: str
    subtitle: str
    min_tier: PlanTier


REPORT_SECTIONS: tuple[ReportSection, ...] = (
    ReportSection(
        id="product_profile",
        number=1,
        title="Product Profile & Core Metrics",
        eyebrow="Section 1 · Profile",
        subtitle="Physical product map, overall score, and five e-commerce metrics",
        min_tier=PlanTier.FREE,
    ),
    ReportSection(
        id="red_flags",
        number=2,
        title="Red Flag & Risk Analysis",
        eyebrow="Section 2 · Risk",
        subtitle="Shark Tank-grade honesty on pitfalls and deal-breakers",
        min_tier=PlanTier.FREE,
    ),
    ReportSection(
        id="margin_matrix",
        number=3,
        title="Financial Matrix & Final GO/NO-GO Verdict",
        eyebrow="Section 3 · Premium",
        subtitle="Margin math, scaling stress-tests, and your final go/no-go decision",
        min_tier=PlanTier.PREMIUM,
    ),
    ReportSection(
        id="marketing_teaser",
        number=4,
        title="Marketing Viability & Targeting Blueprint",
        eyebrow="Section 4 · Premium",
        subtitle="Buyer personas, hook ratings, and primary ad channel maps",
        min_tier=PlanTier.PREMIUM,
    ),
    ReportSection(
        id="web_intelligence",
        number=5,
        title="Live Web-Intelligence & Active Sourcing Links",
        eyebrow="Section 5 · Premium",
        subtitle="Real-time competitor scans and direct supplier price-matches",
        min_tier=PlanTier.PREMIUM,
    ),
    ReportSection(
        id="marketing_deep_dive",
        number=6,
        title="Ultimate 5x Video Content Engine",
        eyebrow="Section 6 · Premium",
        subtitle="Five ready-to-shoot short-form scripts with hooks and angles",
        min_tier=PlanTier.PREMIUM,
    ),
)

SECTION_BY_ID: dict[str, ReportSection] = {s.id: s for s in REPORT_SECTIONS}

LOCKED_SECTION_COPY: dict[str, str] = {
    "margin_matrix": (
        "Upgrade to <strong>Premium</strong> to unlock the Financial Scaling Matrix and the "
        "Final GO/NO-GO Verdict. See if this product is mathematically viable after "
        "stress-testing logistics and shipping spikes."
    ),
    "marketing_teaser": (
        "Upgrade to <strong>Premium</strong> to unlock the Audience &amp; Marketing Blueprint. "
        "Discover your ideal buyer personas, scroll-stopping visual hook ratings, and "
        "primary ad channel scaling maps."
    ),
    "web_intelligence": (
        "Upgrade to <strong>Premium</strong> to unlock real-time web intelligence. Instantly scan "
        "active competitors on Amazon/Shopify and pull direct AliExpress/CJ Sourcing supplier "
        "price-matches."
    ),
    "marketing_deep_dive": (
        "Upgrade to <strong>Premium</strong> to unlock the 5x High-Conversion Ad Script Engine. "
        "Get 5 complete, ready-to-shoot short-form video scripts (TikTok/Reels) with precise "
        "visual hooks and copywriting angles."
    ),
}


def section_by_id(section_id: str) -> ReportSection:
    return SECTION_BY_ID[section_id]


def _tier_rank(tier: PlanTier) -> int:
    return {PlanTier.FREE: 0, PlanTier.PREMIUM: 1}[tier]


def has_section_access(section_id: str, tier: PlanTier | str) -> bool:
    tier = coerce_plan_tier(tier)
    section = section_by_id(section_id)
    return _tier_rank(tier) >= _tier_rank(section.min_tier)


def accessible_section_count(tier: PlanTier | str) -> int:
    return sum(1 for s in REPORT_SECTIONS if has_section_access(s.id, tier))
