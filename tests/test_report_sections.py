"""Tests for report section tier gating."""

from ecom_evaluator.plans import PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, accessible_section_count, has_section_access


def test_six_sections_defined():
    assert len(REPORT_SECTIONS) == 6


def test_free_gets_two_sections():
    assert accessible_section_count(PlanTier.FREE) == 2
    assert has_section_access("product_profile", PlanTier.FREE)
    assert has_section_access("red_flags", PlanTier.FREE)
    assert not has_section_access("margin_matrix", PlanTier.FREE)
    assert not has_section_access("marketing_teaser", PlanTier.FREE)
    assert not has_section_access("web_intelligence", PlanTier.FREE)
    assert not has_section_access("competitor_sentiment", PlanTier.FREE)


def test_premium_unlocks_all_sections():
    assert accessible_section_count(PlanTier.PREMIUM) == 6
    assert has_section_access("margin_matrix", PlanTier.PREMIUM)
    assert has_section_access("marketing_teaser", PlanTier.PREMIUM)
    assert has_section_access("web_intelligence", PlanTier.PREMIUM)
    assert has_section_access("competitor_sentiment", PlanTier.PREMIUM)
