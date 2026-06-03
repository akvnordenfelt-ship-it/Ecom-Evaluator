# ProductScore

**E-commerce Product Evaluator & Go-To-Market Planner** — evaluate product ideas with AI-powered scoring, live competitor research, and a full go-to-market plan.

## Features

- **Shark Tank-style scoring** — investment score plus four dimension gauges
- **Live market research** — DuckDuckGo scans Amazon, AliExpress, and independent stores
- **Gemini 2.5 Flash** — structured JSON analysis with multimodal product images
- **Premium dashboard** — Plotly gauges, market intel, TikTok hooks, GTM strategy
- **Exports** — download JSON or Markdown reports

## Quick start

### 1. Clone and install

```powershell
cd C:\Users\akvno\Ecom-Evaluator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure API key

Copy the example env file and add your [Google AI Studio](https://aistudio.google.com/apikey) key:

```powershell
copy .env.example .env
notepad .env
```

```env
GOOGLE_AI_API_KEY=your_key_here
```

You can also paste a key in **Settings** (top right) in the app.

### 3. Run the app

```powershell
streamlit run app.py
```

Open http://localhost:8501

## Project structure

```
Ecom-Evaluator/
├── app.py                      # Streamlit entry point
├── ecom_evaluator/
│   ├── config.py               # Constants
│   ├── models.py               # Pydantic schemas
│   ├── gemini_client.py        # Gemini API + retries
│   ├── web_search.py           # DuckDuckGo market research
│   ├── reports.py              # Markdown export
│   ├── settings.py             # .env / API key
│   ├── main.py                 # App orchestration
│   └── ui/
│       ├── theme.py            # Premium CSS theme
│       ├── form.py             # Product input form
│       ├── dashboard.py        # Results dashboard
│       └── session.py          # Session state & validation
├── tests/                      # Unit tests
├── .streamlit/config.toml      # Streamlit theme
├── Dockerfile                  # Container deploy
└── requirements.txt
```

## Running tests

```powershell
pip install -r requirements-dev.txt
pytest
```

## Deploy

### Public hosting (shared API key + rate limits)

ProductScore is set up for **free public access** with your Gemini key on the server and **per-session rate limits** so you stay within free-tier quotas.

**Defaults:** 3 evaluations per browser session, 45 seconds between runs.

1. Push this repo to GitHub (do not commit `.env`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → main file: `app.py`.
3. Open **App settings → Secrets** and paste:

```toml
GOOGLE_AI_API_KEY = "your_key_here"
MAX_ANALYSES_PER_SESSION = "3"
ANALYSIS_COOLDOWN_SECONDS = "45"
RATE_LIMIT_ENABLED = "true"
```

4. Deploy and share the public URL. Users can run evaluations without their own key.

**Optional:** Users can paste their own key in **Settings** to bypass session limits (they use their quota, not yours).

**Tune limits** via secrets or environment:

| Variable | Default | Purpose |
|----------|---------|---------|
| `MAX_ANALYSES_PER_SESSION` | `3` | Free runs per browser session |
| `ANALYSIS_COOLDOWN_SECONDS` | `45` | Minimum wait between runs |
| `RATE_LIMIT_ENABLED` | `true` | Set `false` to disable limits (local dev only) |

See `.streamlit/secrets.toml.example` for a local copy.

### Streamlit Community Cloud (quick reference)

1. Push repo to GitHub
2. [share.streamlit.io](https://share.streamlit.io) → New app → `app.py`
3. Add `GOOGLE_AI_API_KEY` in Secrets

### Docker

```powershell
docker build -t productscore .
docker run -p 8501:8501 -e GOOGLE_AI_API_KEY=your_key productscore
```

Or mount a local `.env` file (development only).

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_AI_API_KEY` | Yes* | Gemini API key from Google AI Studio |
| `GEMINI_API_KEY` | Alt | Alias for the same key |
| `MAX_ANALYSES_PER_SESSION` | No | Free runs per session when using hosted key (default `3`) |
| `ANALYSIS_COOLDOWN_SECONDS` | No | Cooldown between runs (default `45`) |
| `RATE_LIMIT_ENABLED` | No | `true` / `false` (default `true`) |

\* Not required for end users when the server secret is set.

## Notes

- Web search uses **DuckDuckGo** (free) — no Google Custom Search CX needed
- Sales figures are **estimated qualitatively** from search snippets, not exact unit data
- Never commit `.env` — it is listed in `.gitignore`

## License

Private / educational use — adjust as needed for your deployment.
