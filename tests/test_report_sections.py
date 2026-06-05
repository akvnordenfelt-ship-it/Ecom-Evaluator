"""Tests for report section tier gating."""

from ecom_evaluator.plans import PlanTier
from ecom_evaluator.report_sections import (
    FREE_SECTION_IDS,
    PREMIUM_SECTION_IDS,
    REPORT_SECTIONS,
    accessible_section_count,
    has_section_access,
)


def test_six_sections_defined():
    assert len(REPORT_SECTIONS) == 6


def test_four_free_two_premium():
    assert len(FREE_SECTION_IDS) == 4
    assert len(PREMIUM_SECTION_IDS) == 2
    assert PREMIUM_SECTION_IDS == frozenset({"marketing_playbook", "launch_strategy"})


def test_free_tier_section_access():
    assert accessible_section_count(PlanTier.FREE) == 4
    assert has_section_access("investment_verdict", PlanTier.FREE)
    assert not has_section_access("marketing_playbook", PlanTier.FREE)


def test_paid_tiers_unlock_all_sections():
    for tier in (PlanTier.PREMIUM, PlanTier.PRO):
        assert accessible_section_count(tier) == 6
        assert has_section_access("launch_strategy", tier)
