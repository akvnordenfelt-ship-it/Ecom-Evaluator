# Crow Metrics

**E-commerce Product Evaluator & Go-To-Market Planner** — evaluate product ideas with AI-powered scoring, live competitor research, and a full go-to-market plan.

## Features

- **Shark Tank-style scoring** — investment score plus four dimension gauges
- **Live market research** — DuckDuckGo scans Amazon, AliExpress, and independent stores
- **Groq AI** — fast Llama models with JSON output and optional vision (product images)
- **Premium dashboard** — Plotly gauges, market intel, marketing playbook, GTM strategy
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

Copy the example env file and add your [Groq](https://console.groq.com/keys) key:

```powershell
copy .env.example .env
notepad .env
```

```env
GROQ_API_KEY=your_groq_key_here
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
│   ├── groq_client.py          # Groq API + retries
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

Crow Metrics is set up for **free public access** with your Groq key on the server and **per-session rate limits**.

**Defaults:** 3 evaluations per browser session, 45 seconds between runs.

1. Push this repo to GitHub (do not commit `.env`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → main file: `app.py`.
3. Open **App settings → Secrets** and paste:

```toml
GROQ_API_KEY = "your_groq_key_here"
MAX_ANALYSES_PER_SESSION = "3"
ANALYSIS_COOLDOWN_SECONDS = "45"
RATE_LIMIT_ENABLED = "true"
```

4. Deploy and share the public URL.

### Docker

```powershell
docker build -t crowmetrics .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key crowmetrics
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes* | API key from [console.groq.com](https://console.groq.com/keys) |
| `GROQ_MODEL` | No | Text model (default `llama-3.3-70b-versatile`) |
| `GROQ_VISION_MODEL` | No | Vision model when image uploaded (default `meta-llama/llama-4-scout-17b-16e-instruct`) |
| `MAX_ANALYSES_PER_SESSION` | No | Free runs per session (default `3`) |
| `ANALYSIS_COOLDOWN_SECONDS` | No | Cooldown between runs (default `45`) |
| `RATE_LIMIT_ENABLED` | No | `true` / `false` (default `true`) |

\* Not required for end users when the server secret is set.

## Notes

- Uses **JSON mode** + Pydantic validation (avoids Gemini-style strict schema limits)
- Web search uses **DuckDuckGo** (free)
- Never commit `.env` — it is listed in `.gitignore`

## License

Private / educational use — adjust as needed for your deployment.
