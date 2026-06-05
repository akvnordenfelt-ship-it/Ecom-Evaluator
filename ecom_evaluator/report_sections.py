"""Six fixed report sections and tier access rules."""

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
    free_tier: bool


REPORT_SECTIONS: tuple[ReportSection, ...] = (
    ReportSection(
        id="investment_verdict",
        number=1,
        title="Investment Verdict",
        eyebrow="Section 1 · Overview",
        subtitle="Final score, saturation, and go/no-go signal",
        free_tier=True,
    ),
    ReportSection(
        id="market_intelligence",
        number=2,
        title="Market Intelligence",
        eyebrow="Section 2 · Market",
        subtitle="Live competitor research across Amazon, AliExpress, and the web",
        free_tier=True,
    ),
    ReportSection(
        id="unit_economics",
        number=3,
        title="Unit Economics & Logistics",
        eyebrow="Section 3 · Economics",
        subtitle="Margin viability, billable weight, and shipping class",
        free_tier=True,
    ),
    ReportSection(
        id="scorecard",
        number=4,
        title="Dimension Scorecard",
        eyebrow="Section 4 · Scorecard",
        subtitle="Four Shark Tank-style dimensions with panel rationale",
        free_tier=True,
    ),
    ReportSection(
        id="marketing_playbook",
        number=5,
        title="Marketing Playbook",
        eyebrow="Section 5 · Marketing",
        subtitle="Audience, organic/paid mix, platforms, and creative concepts",
        free_tier=False,
    ),
    ReportSection(
        id="launch_strategy",
        number=6,
        title="Launch Strategy",
        eyebrow="Section 6 · Operations",
        subtitle="Phased go-to-market plan and priority playbook",
        free_tier=False,
    ),
)

SECTION_BY_ID: dict[str, ReportSection] = {section.id: section for section in REPORT_SECTIONS}

FREE_SECTION_IDS: frozenset[str] = frozenset(section.id for section in REPORT_SECTIONS if section.free_tier)
PREMIUM_SECTION_IDS: frozenset[str] = frozenset(section.id for section in REPORT_SECTIONS if not section.free_tier)


def section_by_id(section_id: str) -> ReportSection:
    return SECTION_BY_ID[section_id]


def has_section_access(section_id: str, tier: PlanTier | str) -> bool:
    section = section_by_id(section_id)
    if section.free_tier:
        return True
    if isinstance(tier, str):
        tier = PlanTier(tier)
    return tier in (PlanTier.PREMIUM, PlanTier.PRO)


def accessible_section_count(tier: PlanTier | str) -> int:
    return sum(1 for section in REPORT_SECTIONS if has_section_access(section.id, tier))
