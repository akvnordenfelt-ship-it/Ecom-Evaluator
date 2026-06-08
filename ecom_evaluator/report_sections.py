"""Six report sections and tier access rules."""

from __future__ import annotations

from dataclasses import dataclass

from ecom_evaluator.plans import PlanTier


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
        title="Smart Margin & Scaling Matrix",
        eyebrow="Section 3 · Finance & Verdict",
        subtitle="Python-calculated margins, ROI, break-even CPA, volume projections, and go/no-go verdict",
        min_tier=PlanTier.FREE,
    ),
    ReportSection(
        id="marketing_teaser",
        number=4,
        title="Marketing Viability Teaser",
        eyebrow="Section 4 · Marketing",
        subtitle="Primary channel, hook index, and core buyer persona",
        min_tier=PlanTier.PREMIUM,
    ),
    ReportSection(
        id="web_intelligence",
        number=5,
        title="Live Web-Intelligence & Sourcing Links",
        eyebrow="Section 5 · Premium",
        subtitle="Real-time search, supplier matches, and live competitor tracking",
        min_tier=PlanTier.PREMIUM,
    ),
    ReportSection(
        id="marketing_deep_dive",
        number=6,
        title="Ultimate Marketing Deep-Dive & Content Engine",
        eyebrow="Section 6 · Pro",
        subtitle="Ad scripts, targeting blueprint, influencer DMs, and positioning matrix",
        min_tier=PlanTier.PRO,
    ),
)

SECTION_BY_ID: dict[str, ReportSection] = {s.id: s for s in REPORT_SECTIONS}


def section_by_id(section_id: str) -> ReportSection:
    return SECTION_BY_ID[section_id]


def _tier_rank(tier: PlanTier) -> int:
    return {PlanTier.FREE: 0, PlanTier.PREMIUM: 1, PlanTier.PRO: 2}[tier]


def has_section_access(section_id: str, tier: PlanTier | str) -> bool:
    if isinstance(tier, str):
        tier = PlanTier(tier)
    section = section_by_id(section_id)
    return _tier_rank(tier) >= _tier_rank(section.min_tier)


def accessible_section_count(tier: PlanTier | str) -> int:
    return sum(1 for s in REPORT_SECTIONS if has_section_access(s.id, tier))
