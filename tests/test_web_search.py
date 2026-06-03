"""Tests for DuckDuckGo web research helpers."""

from ecom_evaluator.models import MarketSearchHit
from ecom_evaluator.web_search import dedupe_search_hits, format_web_research_for_prompt


def test_dedupe_search_hits_by_url():
    hits: list[MarketSearchHit] = [
        {
            "channel": "Amazon",
            "query": "q1",
            "title": "A",
            "url": "https://amazon.com/item/1",
            "snippet": "s1",
        },
        {
            "channel": "Amazon",
            "query": "q2",
            "title": "A duplicate",
            "url": "https://amazon.com/item/1/",
            "snippet": "s2",
        },
        {
            "channel": "AliExpress",
            "query": "q3",
            "title": "B",
            "url": "https://aliexpress.com/item/2",
            "snippet": "s3",
        },
    ]
    unique = dedupe_search_hits(hits)
    assert len(unique) == 2


def test_format_web_research_empty():
    text = format_web_research_for_prompt([])
    assert "No competitor listings" in text
    assert "market_research" in text


def test_format_web_research_includes_hits():
    hits: list[MarketSearchHit] = [
        {
            "channel": "Amazon",
            "query": "widget site:amazon.com",
            "title": "Widget Pro",
            "url": "https://amazon.com/widget",
            "snippet": "Best widget",
        }
    ]
    text = format_web_research_for_prompt(hits)
    assert "Widget Pro" in text
    assert "https://amazon.com/widget" in text
    assert "Amazon" in text
