"""Web market research via DuckDuckGo (no Google Custom Search required)."""

from __future__ import annotations

import time

from ecom_evaluator.config import (
    WEB_SEARCH_MAX_RESULTS,
    WEB_SEARCH_PROMPT_MAX_HITS,
    WEB_SEARCH_PROMPT_SNIPPET_CHARS,
    WEB_SEARCH_QUERY_DELAY_SECONDS,
)
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.models import MarketSearchHit

MARKET_SEARCH_TEMPLATES: list[tuple[str, str]] = [
    ("Amazon", "{name} site:amazon.com"),
    ("AliExpress", "{name} site:aliexpress.com"),
    ("Independent stores", "{name} buy shop -site:amazon.com -site:aliexpress.com"),
    ("Demand signals", "{name} product reviews bestseller demand"),
]


def _get_ddgs_client():
    try:
        from ddgs import DDGS

        return DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS

            return DDGS
        except ImportError as exc:
            raise AnalysisError("Web search library not installed. Run: pip install ddgs") from exc


def dedupe_search_hits(hits: list[MarketSearchHit]) -> list[MarketSearchHit]:
    seen: set[str] = set()
    unique: list[MarketSearchHit] = []
    for hit in hits:
        key = hit["url"].lower().rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        unique.append(hit)
    return unique


def run_web_market_research(
    *,
    product_name: str,
    description: str,
    max_results: int | None = None,
) -> list[MarketSearchHit]:
    DDGS = _get_ddgs_client()
    hits: list[MarketSearchHit] = []
    keywords = product_name.strip()
    desc_hint = " ".join(description.split()[:8])
    search_name = f"{keywords} {desc_hint}".strip() if desc_hint else keywords
    per_query_max = max_results if max_results is not None else WEB_SEARCH_MAX_RESULTS

    for channel, template in MARKET_SEARCH_TEMPLATES:
        query = template.format(name=search_name)
        try:
            raw_results = DDGS().text(query, max_results=per_query_max, region="wt-wt")
            for item in raw_results or []:
                url = (item.get("href") or item.get("link") or "").strip()
                title = (item.get("title") or "").strip()
                snippet = (item.get("body") or item.get("snippet") or "").strip()
                if not url or not title:
                    continue
                hits.append(
                    MarketSearchHit(
                        channel=channel,
                        query=query,
                        title=title,
                        url=url,
                        snippet=snippet[:WEB_SEARCH_PROMPT_SNIPPET_CHARS],
                    )
                )
        except Exception:
            continue
        time.sleep(WEB_SEARCH_QUERY_DELAY_SECONDS)

    return dedupe_search_hits(hits)


def format_web_research_for_prompt(hits: list[MarketSearchHit]) -> str:
    if not hits:
        return (
            "## Live web research (DuckDuckGo)\n"
            'No competitor listings were retrieved. In `market_research`, set competitor_count_signal '
            'and demand_estimate.level to "Unknown", explain the gap in data_limitations, and treat '
            "market_saturation as highly uncertain."
        )

    lines = [
        "## Live web research (DuckDuckGo)",
        "Analyze ALL results below and reflect your conclusions in the `market_research` JSON object.",
        "Only cite URLs and titles that appear here. Group findings by Amazon, AliExpress, and independent stores.",
        "",
    ]
    for index, hit in enumerate(hits[:WEB_SEARCH_PROMPT_MAX_HITS], start=1):
        lines.extend(
            [
                f"### Result {index} — {hit['channel']}",
                f"- Title: {hit['title']}",
                f"- URL: {hit['url']}",
                f"- Snippet: {hit['snippet'] or '(no snippet)'}",
                f"- Query used: `{hit['query']}`",
                "",
            ]
        )
    return "\n".join(lines)
