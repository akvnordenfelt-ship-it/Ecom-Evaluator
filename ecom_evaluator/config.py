"""Application configuration constants."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GEMINI_MODEL = "gemini-2.5-flash"
MAX_API_ATTEMPTS = 4
RETRY_BACKOFF_SECONDS = [2, 4, 8]
TRANSIENT_API_CODES = {429, 500, 502, 503, 504}
WEB_SEARCH_MAX_RESULTS = 5
WEB_SEARCH_QUERY_DELAY_SECONDS = 1.0

# Shared hosting: keep free-tier API usage under control
MAX_ANALYSES_PER_SESSION = 3
ANALYSIS_COOLDOWN_SECONDS = 45

# SaaS free tier (per browser session)
DEFAULT_FREE_EVALUATIONS = 1

# Set in Streamlit secrets or .env when Stripe Checkout is ready
STRIPE_CHECKOUT_URL = os.getenv("STRIPE_CHECKOUT_URL", "").strip()

PLOTLY_CHART_CONFIG = {"displayModeBar": False, "staticPlot": False}
