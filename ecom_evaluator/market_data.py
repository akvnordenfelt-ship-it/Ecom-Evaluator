"""Market data layer — web search today; optional scraper providers for Sections 5–6."""

from __future__ import annotations

from ecom_evaluator.config import APIFY_API_TOKEN, SCRAPERAPI_KEY, SCRAPER_PROVIDER
from ecom_evaluator.models import MarketSearchHit
from ecom_evaluator.web_search import format_web_research_for_prompt, run_web_market_research


def scraper_is_configured() -> bool:
    provider = SCRAPER_PROVIDER
    if provider == "apify":
        return bool(APIFY_API_TOKEN)
    if provider == "scraperapi":
        return bool(SCRAPERAPI_KEY)
    return False


def _scraper_disclaimer() -> str:
    if scraper_is_configured():
        return (
            f"Scraper provider `{SCRAPER_PROVIDER}` is configured but structured scraping "
            "is not yet wired — synthesis uses DuckDuckGo snippets only."
        )
    return (
        "No scraper API configured (set SCRAPER_PROVIDER + APIFY_API_TOKEN or SCRAPERAPI_KEY). "
        "Live intel uses DuckDuckGo search snippets — add Apify/ScraperAPI for Amazon review scraping."
    )


def run_market_research(
    *,
    product_name: str,
    description: str,
    max_results: int,
    product_url: str = "",
) -> tuple[list[MarketSearchHit], str]:
    """Return search hits plus formatted prompt block (with scraper status note)."""
    hits = run_web_market_research(
        product_name=product_name,
        description=description,
        max_results=max_results,
        product_url=product_url,
    )
    research_text = format_web_research_for_prompt(hits)
    disclaimer = _scraper_disclaimer()
    combined = f"{research_text}\n\n## Scraper infrastructure\n{disclaimer}"
    return hits, combined
