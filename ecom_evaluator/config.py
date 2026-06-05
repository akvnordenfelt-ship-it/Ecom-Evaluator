"""Application configuration constants."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
GROQ_MAX_COMPLETION_TOKENS = int(os.getenv("GROQ_MAX_COMPLETION_TOKENS", "8192"))
MAX_API_ATTEMPTS = 4
MAX_PARSE_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = [2, 4, 8]
TRANSIENT_API_CODES = {429, 500, 502, 503, 504}
WEB_SEARCH_MAX_RESULTS = 4
WEB_SEARCH_QUERY_DELAY_SECONDS = 1.0
WEB_SEARCH_PROMPT_MAX_HITS = 14
WEB_SEARCH_PROMPT_SNIPPET_CHARS = 400

# Shared hosting: keep free-tier API usage under control
MAX_ANALYSES_PER_SESSION = 3
ANALYSIS_COOLDOWN_SECONDS = 45

# SaaS free tier (per browser session)
DEFAULT_FREE_EVALUATIONS = 1

# Set to true when Premium/Pro billing is ready
PAID_TIERS_ENABLED = os.getenv("PAID_TIERS_ENABLED", "false").lower() in ("1", "true", "yes")

# Stripe Checkout links (configure when billing is live)
STRIPE_PREMIUM_CHECKOUT_URL = os.getenv("STRIPE_PREMIUM_CHECKOUT_URL", os.getenv("STRIPE_CHECKOUT_URL", "")).strip()
STRIPE_PRO_CHECKOUT_URL = os.getenv("STRIPE_PRO_CHECKOUT_URL", "").strip()
STRIPE_CHECKOUT_URL = STRIPE_PREMIUM_CHECKOUT_URL

PLOTLY_CHART_CONFIG = {"displayModeBar": False, "staticPlot": False}
