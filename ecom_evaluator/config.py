"""Application configuration constants."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-2.5-pro")
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "8192"))

# Premium paid sections — Claude Sonnet default, Opus for Section 3 CFO verdict only
CLAUDE_SONNET_MODEL = os.getenv("CLAUDE_SONNET_MODEL", "claude-sonnet-4-6")
CLAUDE_OPUS_MODEL = os.getenv("CLAUDE_OPUS_MODEL", "claude-opus-4-8")
CLAUDE_MAX_OUTPUT_TOKENS = int(os.getenv("CLAUDE_MAX_OUTPUT_TOKENS", "8192"))

# Optional scraping provider for Sections 5–6 (apify | scraperapi | none)
SCRAPER_PROVIDER = os.getenv("SCRAPER_PROVIDER", "none").strip().lower()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "").strip()
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY", "").strip()

# Legacy env names still supported
GROQ_MODEL = GEMINI_MODEL
GROQ_VISION_MODEL = GEMINI_MODEL
GROQ_MAX_COMPLETION_TOKENS = GEMINI_MAX_OUTPUT_TOKENS
MAX_API_ATTEMPTS = 4
MAX_PARSE_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = [2, 4, 8]
TRANSIENT_API_CODES = {429, 500, 502, 503, 504}
WEB_SEARCH_MAX_RESULTS = 4
WEB_SEARCH_QUERY_DELAY_SECONDS = 1.0
WEB_SEARCH_PROMPT_MAX_HITS = 14
WEB_SEARCH_PROMPT_SNIPPET_CHARS = 400

# Shared hosting: secondary guardrail (aligned with FREE_EVALUATIONS_PER_ACCOUNT)
MAX_ANALYSES_PER_SESSION = int(os.getenv("MAX_ANALYSES_PER_SESSION", "3"))
ANALYSIS_COOLDOWN_SECONDS = 45

# SaaS free tier (per authenticated account)
FREE_EVALUATIONS_PER_ACCOUNT = int(os.getenv("FREE_EVALUATIONS_PER_ACCOUNT", "3"))
DEFAULT_FREE_EVALUATIONS = FREE_EVALUATIONS_PER_ACCOUNT

# Authentication
AUTH_REQUIRED = os.getenv("AUTH_REQUIRED", "true").lower() in ("1", "true", "yes", "on")
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "dev").strip().lower()
QUOTA_STORE_PATH = PROJECT_ROOT / ".data" / "user_quota.json"

# Set to true when Premium/Pro billing is ready (locked sections always shown for free users)
PAID_TIERS_ENABLED = os.getenv("PAID_TIERS_ENABLED", "true").lower() in ("1", "true", "yes")

# Stripe Checkout links (configure when billing is live)
STRIPE_PREMIUM_CHECKOUT_URL = os.getenv("STRIPE_PREMIUM_CHECKOUT_URL", os.getenv("STRIPE_CHECKOUT_URL", "")).strip()
STRIPE_PRO_CHECKOUT_URL = os.getenv("STRIPE_PRO_CHECKOUT_URL", "").strip()
STRIPE_CHECKOUT_URL = STRIPE_PREMIUM_CHECKOUT_URL

PLOTLY_CHART_CONFIG = {"displayModeBar": False, "staticPlot": False}
