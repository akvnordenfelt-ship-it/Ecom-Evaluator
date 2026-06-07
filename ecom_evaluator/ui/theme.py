"""Premium SaaS theme CSS and helpers."""

from __future__ import annotations

import html

import streamlit as st

PREMIUM_THEME_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --ps-bg: #F8F9FA;
    --ps-surface: #FFFFFF;
    --ps-border: #E9ECEF;
    --ps-text: #0F172A;
    --ps-muted: #64748B;
    --ps-blue: #3B82F6;
    --ps-blue-deep: #1E40AF;
    --ps-indigo: #4338CA;
    --ps-pill-bg: #E3F2FD;
    --ps-pill-text: #0D47A1;
    --ps-success: #10B981;
    --ps-radius: 12px;
    --ps-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.06);
}

/* Global canvas */
.stApp {
    background-color: var(--ps-bg) !important;
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
html, body, [class*="css"] {
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--ps-text);
}
section[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stMain"] > div {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.25rem 3rem;
}
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1.25rem; max-width: 1180px; }

/* Hide default Streamlit chrome for SaaS shell */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stAppDeployButton, [data-testid="stAppDeployButton"] { display: none !important; }
button[kind="header"] { display: none !important; }

/* Cards & bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--ps-surface) !important;
    border: 1px solid var(--ps-border) !important;
    border-radius: var(--ps-radius) !important;
    box-shadow: var(--ps-shadow) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    padding: 0.35rem 0.15rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
    border-bottom: 1px solid var(--ps-border);
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--ps-muted);
    border-radius: 8px 8px 0 0;
    padding: 0.6rem 1rem;
}
.stTabs [aria-selected="true"] {
    color: var(--ps-blue-deep) !important;
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-bottom-color: var(--ps-surface) !important;
}

/* App shell */
.app-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.25rem;
    border-bottom: 1px solid var(--ps-border);
    margin-bottom: 1.75rem;
}
.brand-lockup { display: flex; flex-direction: column; gap: 0.15rem; }
.brand-name {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--ps-text);
    margin: 0;
}
.brand-tagline { font-size: 0.82rem; color: var(--ps-muted); margin: 0; }

/* Hero banner */
.hero-block {
    background: linear-gradient(135deg, #0B1F4B 0%, #1E40AF 48%, #4338CA 100%);
    border-radius: var(--ps-radius);
    padding: 2rem 2.25rem;
    color: #F8FAFC;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 50px rgba(30, 64, 175, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.hero-kicker {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #BFDBFE;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 999px;
    padding: 0.35rem 0.75rem;
    margin: 0 0 0.85rem 0;
}
.hero-title {
    font-size: 1.85rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin: 0 0 0.65rem 0;
    color: #FFFFFF;
}
.hero-copy {
    font-size: 0.98rem;
    line-height: 1.65;
    color: #CBD5E1;
    margin: 0;
    max-width: 680px;
}

/* Step pills & card headers */
.form-card-header { margin-bottom: 1rem; }
.step-pill {
    display: inline-block;
    background: var(--ps-pill-bg);
    color: var(--ps-pill-text);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-radius: 999px;
    padding: 0.28rem 0.65rem;
    margin-bottom: 0.45rem;
}
.form-card-title {
    font-size: 1.08rem;
    font-weight: 600;
    color: var(--ps-text);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.45rem;
}
.form-card-label { display: none; }

/* Inputs */
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stFileUploader"] label {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #334155 !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--ps-surface) !important;
    border: 1px solid var(--ps-border) !important;
    border-radius: 8px !important;
    color: var(--ps-text) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    outline: none !important;
    border-color: var(--ps-blue) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.18) !important;
}

/* Primary CTA */
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, #1D4ED8 0%, #1E3A8A 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.78rem 1.25rem !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em;
    box-shadow: 0 10px 24px rgba(30, 64, 175, 0.22) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease !important;
}
.stButton > button[kind="primary"]:hover:not(:disabled) {
    transform: translateY(-1px) scale(1.01);
    filter: brightness(1.05);
    box-shadow: 0 14px 32px rgba(30, 64, 175, 0.28) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stButton > button[kind="primary"]:disabled {
    opacity: 0.55 !important;
    transform: none !important;
}
.stButton > button[kind="secondary"] {
    border-radius: 8px !important;
    border-color: var(--ps-border) !important;
    background: var(--ps-surface) !important;
}

/* Readiness checklist */
.readiness-card {
    background: linear-gradient(180deg, #FAFBFC 0%, #FFFFFF 100%);
    border: 1px solid var(--ps-border);
    border-radius: 10px;
    padding: 0.85rem 0.95rem;
}
.readiness-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid #F1F3F5;
}
.readiness-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ps-muted);
}
.readiness-score {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ps-blue-deep);
    background: var(--ps-pill-bg);
    border-radius: 999px;
    padding: 0.2rem 0.55rem;
}
.check-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.86rem;
    padding: 0.42rem 0;
    color: #94A3B8;
}
.check-dot {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    background: #D1D5DB;
    flex-shrink: 0;
    box-shadow: inset 0 0 0 1px rgba(0,0,0,0.04);
}
.check-row--done { color: var(--ps-text); font-weight: 500; }
.check-row--done .check-dot {
    background: var(--ps-success);
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

/* Utility & dashboard */
.section-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ps-muted);
    margin: 0 0 0.35rem 0;
}
.report-meta { font-size: 0.88rem; color: var(--ps-muted); margin: -0.5rem 0 1rem 0; }
.status-banner {
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    font-weight: 500;
    margin-bottom: 1rem;
}
.status-banner--success {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}
.metric-hint {
    background: #F8F9FA;
    border: 1px solid var(--ps-border);
    border-radius: 8px;
    padding: 0.75rem 0.9rem;
    font-size: 0.84rem;
    color: #475569;
    margin-top: 0.5rem;
}
.verdict-label {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--ps-text);
    margin: 0.5rem 0 1rem 0;
}
.saturation-badge {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
}
.insight-card {
    background: #FAFBFC;
    border: 1px solid var(--ps-border);
    border-left: 4px solid var(--ps-blue);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    color: #334155;
    font-size: 0.95rem;
    line-height: 1.55;
}
.hook-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: var(--ps-radius);
    padding: 1rem 1.1rem;
    min-height: 220px;
    box-shadow: var(--ps-shadow);
}
.hook-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--ps-muted);
    margin: 0.6rem 0 0.25rem 0;
}
.hook-label:first-child { margin-top: 0; }
.hook-text { font-size: 0.98rem; font-weight: 600; color: var(--ps-text); line-height: 1.4; margin: 0; }
.hook-body { font-size: 0.9rem; color: #475569; line-height: 1.45; margin: 0; }
.research-channel-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.5;
    min-height: 120px;
}

/* Landing page */
.landing-wrap { margin: 0.5rem 0 1.5rem; }
.landing-hero {
    background: linear-gradient(135deg, #0B1F4B 0%, #1E40AF 48%, #4338CA 100%);
    border-radius: 20px;
    padding: 3.25rem 2.5rem 2.75rem;
    text-align: center;
    color: #F8FAFC;
    box-shadow: 0 24px 60px rgba(30, 64, 175, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.12);
    position: relative;
    overflow: hidden;
}
.landing-hero::before {
    content: "";
    position: absolute;
    top: -40%;
    right: -15%;
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.landing-kicker {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #BFDBFE;
    margin: 0 0 1rem;
    position: relative;
}
.landing-title {
    font-size: clamp(1.85rem, 4vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 1rem;
    line-height: 1.12;
    position: relative;
}
.landing-lead {
    font-size: 1.05rem;
    color: #E2E8F0;
    max-width: 680px;
    margin: 0 auto 1.5rem;
    line-height: 1.65;
    position: relative;
}
.lp-hero-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    position: relative;
}
.lp-hero-badge {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #F1F5F9;
    backdrop-filter: blur(4px);
}
.lp-stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.75rem 0 2.5rem;
    padding: 1.25rem 1.5rem;
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 16px;
    box-shadow: var(--ps-shadow);
}
.lp-stat { text-align: center; }
.lp-stat-value {
    display: block;
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--ps-blue-deep);
    letter-spacing: -0.02em;
}
.lp-stat-label {
    display: block;
    font-size: 0.78rem;
    color: var(--ps-muted);
    font-weight: 600;
    margin-top: 0.15rem;
}
.lp-section-header {
    text-align: center;
    max-width: 720px;
    margin: 2.5rem auto 1.5rem;
}
.lp-section-header-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ps-blue);
    margin: 0 0 0.5rem;
}
.lp-section-header-title {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--ps-text);
    margin: 0 0 0.65rem;
    line-height: 1.2;
}
.lp-section-header-lead {
    font-size: 0.95rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.6;
}
.lp-section-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.1rem;
    margin-bottom: 0.5rem;
}
@media (max-width: 768px) {
    .lp-section-grid { grid-template-columns: 1fr; }
    .lp-stats-strip { grid-template-columns: repeat(2, 1fr); }
    .lp-steps-grid { grid-template-columns: 1fr !important; }
    .lp-pricing-grid { grid-template-columns: 1fr !important; }
    .lp-preview-card { flex-direction: column !important; }
}
.lp-section-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 16px;
    padding: 1.35rem 1.25rem 1.2rem;
    box-shadow: var(--ps-shadow);
    border-top: 4px solid var(--accent);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    min-height: 210px;
}
.lp-section-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.1);
}
.lp-section-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.65rem;
}
.lp-section-icon {
    font-size: 1.75rem;
    line-height: 1;
    background: var(--accent-soft);
    width: 2.75rem;
    height: 2.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
}
.lp-free-pill {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}
.lp-section-num {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 0.25rem;
}
.lp-section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: var(--ps-text);
    margin: 0 0 0.4rem;
    line-height: 1.25;
}
.lp-section-body {
    font-size: 0.86rem;
    color: var(--ps-muted);
    margin: 0 0 0.75rem;
    line-height: 1.5;
}
.lp-section-highlight {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--ps-text);
    margin: 0;
    padding: 0.5rem 0.65rem;
    background: var(--accent-soft);
    border-radius: 8px;
    border-left: 3px solid var(--accent);
}
.lp-pricing-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
    margin-bottom: 0.5rem;
}
.lp-pricing-card {
    border-radius: 18px;
    padding: 1.75rem 1.5rem;
    position: relative;
    overflow: hidden;
    min-height: 320px;
}
.lp-pricing-card--premium {
    background: linear-gradient(160deg, #EFF6FF 0%, #FFFFFF 55%, #F0F9FF 100%);
    border: 2px solid #93C5FD;
    box-shadow: 0 16px 40px rgba(59, 130, 246, 0.12);
}
.lp-pricing-card--pro {
    background: linear-gradient(160deg, #1E1B4B 0%, #312E81 45%, #4338CA 100%);
    border: 2px solid rgba(255,255,255,0.15);
    box-shadow: 0 16px 40px rgba(67, 56, 202, 0.25);
    color: #F8FAFC;
}
.lp-popular-pill, .lp-pro-pill {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
}
.lp-popular-pill { background: #3B82F6; color: #fff; }
.lp-pro-pill { background: rgba(255,255,255,0.15); color: #E0E7FF; border: 1px solid rgba(255,255,255,0.2); }
.lp-pricing-tier {
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0 0 0.25rem;
    opacity: 0.85;
}
.lp-pricing-price {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.65rem;
    line-height: 1;
}
.lp-pricing-price span {
    font-size: 1rem;
    font-weight: 600;
    opacity: 0.7;
}
.lp-pricing-card--pro .lp-pricing-price { color: #fff; }
.lp-pricing-blurb {
    font-size: 0.88rem;
    line-height: 1.55;
    margin: 0 0 1rem;
    opacity: 0.9;
}
.lp-pricing-features {
    margin: 0;
    padding-left: 0;
    list-style: none;
}
.lp-pricing-features li {
    font-size: 0.84rem;
    line-height: 1.5;
    padding: 0.4rem 0;
    border-top: 1px solid rgba(0,0,0,0.06);
}
.lp-pricing-card--pro .lp-pricing-features li { border-top-color: rgba(255,255,255,0.12); }
.lp-steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin-bottom: 0.5rem;
}
.lp-step-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 16px;
    padding: 1.5rem 1.25rem;
    box-shadow: var(--ps-shadow);
    text-align: center;
}
.lp-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2.25rem;
    height: 2.25rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #3B82F6, #4338CA);
    color: #fff;
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
}
.lp-step-title {
    font-size: 1rem;
    font-weight: 800;
    margin: 0 0 0.4rem;
    color: var(--ps-text);
}
.lp-step-body {
    font-size: 0.86rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.55;
}
.lp-preview-card {
    display: flex;
    gap: 2rem;
    background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
    border: 1px solid #BFDBFE;
    border-radius: 18px;
    padding: 2rem 2.25rem;
    margin-bottom: 0.5rem;
    box-shadow: var(--ps-shadow);
}
.lp-preview-left {
    flex: 0 0 200px;
    text-align: center;
    padding: 1rem;
    background: #fff;
    border-radius: 14px;
    border: 1px solid var(--ps-border);
}
.lp-preview-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--ps-muted);
    margin: 0 0 0.5rem;
}
.lp-preview-score {
    font-size: 3rem;
    font-weight: 800;
    color: var(--ps-blue-deep);
    margin: 0;
    line-height: 1;
}
.lp-preview-score span { font-size: 1.25rem; color: var(--ps-muted); font-weight: 600; }
.lp-preview-verdict {
    font-size: 0.82rem;
    font-weight: 700;
    color: #D97706;
    margin: 0.5rem 0 0;
}
.lp-preview-right { flex: 1; display: flex; flex-direction: column; gap: 0.65rem; justify-content: center; }
.lp-preview-metric {
    display: grid;
    grid-template-columns: 130px 1fr 36px;
    align-items: center;
    gap: 0.75rem;
    margin: 0;
    font-size: 0.82rem;
    color: var(--ps-text);
}
.lp-preview-metric span:first-child { font-weight: 600; color: var(--ps-muted); }
.lp-preview-metric strong { text-align: right; font-weight: 800; }
.lp-bar {
    display: block;
    height: 8px;
    background: #E2E8F0;
    border-radius: 999px;
    overflow: hidden;
}
.lp-bar i {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #3B82F6, #6366F1);
    border-radius: 999px;
}
.lp-compare-wrap {
    overflow-x: auto;
    margin-bottom: 1rem;
    border: 1px solid var(--ps-border);
    border-radius: 16px;
    background: var(--ps-surface);
    box-shadow: var(--ps-shadow);
}
.lp-compare-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.lp-compare-table th {
    background: #F1F5F9;
    padding: 0.85rem 1rem;
    text-align: left;
    font-weight: 700;
    color: var(--ps-text);
    border-bottom: 1px solid var(--ps-border);
}
.lp-compare-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--ps-border);
    color: #475569;
}
.lp-compare-table tr:last-child td { border-bottom: none; }
.lp-compare-table td:not(:first-child) { text-align: center; font-weight: 600; }
.lp-final-cta {
    margin: 2.5rem 0 1.25rem;
    padding: 2.75rem 2rem;
    text-align: center;
    background: linear-gradient(135deg, #0B1F4B 0%, #1E40AF 50%, #4338CA 100%);
    border-radius: 20px;
    color: #F8FAFC;
    box-shadow: 0 20px 50px rgba(30, 64, 175, 0.22);
}
.lp-final-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #93C5FD;
    margin: 0 0 0.5rem;
}
.lp-final-title {
    font-size: 1.65rem;
    font-weight: 800;
    margin: 0 0 0.65rem;
    letter-spacing: -0.02em;
}
.lp-final-lead {
    font-size: 0.95rem;
    color: #CBD5E1;
    margin: 0;
    max-width: 520px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.55;
}
.landing-feature {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: var(--ps-radius);
    padding: 1.25rem 1.1rem;
    min-height: 160px;
    box-shadow: var(--ps-shadow);
}
.landing-feature-icon { font-size: 1.5rem; display: block; margin-bottom: 0.5rem; }
.landing-feature-title { font-weight: 700; font-size: 1rem; margin: 0 0 0.35rem; color: var(--ps-text); }
.landing-feature-body { font-size: 0.88rem; color: var(--ps-muted); margin: 0; line-height: 1.5; }
.landing-cta-spacer { height: 1.5rem; }
.landing-footnote {
    text-align: center;
    font-size: 0.82rem;
    color: var(--ps-muted);
    margin: 1.5rem 0 2rem;
}

/* Tool intro (replaces in-tool hero) */
.tool-intro { margin-bottom: 1.25rem; }
.tool-intro-kicker {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ps-muted);
    margin: 0;
}
.tool-intro-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--ps-text);
    margin: 0.25rem 0 0;
}

/* Paywall */
.paywall-card {
    background: linear-gradient(160deg, #0F172A 0%, #1E3A8A 55%, #312E81 100%);
    border-radius: var(--ps-radius);
    padding: 1.5rem 1.35rem;
    color: #F8FAFC;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.2);
    margin-bottom: 0.75rem;
}
.paywall-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #93C5FD;
    margin: 0 0 0.5rem;
}
.paywall-title { font-size: 1.35rem; font-weight: 700; margin: 0 0 0.5rem; }
.paywall-copy { font-size: 0.92rem; color: #CBD5E1; line-height: 1.55; margin: 0 0 0.85rem; }
.paywall-list {
    margin: 0;
    padding-left: 1.1rem;
    font-size: 0.88rem;
    color: #E2E8F0;
    line-height: 1.7;
}

/* Pricing & locked sections */
.pricing-card, .landing-plan, .landing-section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.75rem;
}
.pricing-card--premium { border-color: #60A5FA; }
.pricing-card--pro { border-color: #A78BFA; }
.pricing-kicker, .landing-section-num {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #93C5FD;
    margin: 0 0 0.35rem;
}
.pricing-name, .landing-plan-name, .landing-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 0.25rem;
    color: #F8FAFC;
}
.pricing-price, .landing-plan-price {
    font-size: 1.75rem;
    font-weight: 800;
    margin: 0 0 0.5rem;
    color: #fff;
}
.pricing-price span, .landing-plan-price span { font-size: 0.9rem; font-weight: 600; color: #94A3B8; }
.pricing-list {
    margin: 0;
    padding-left: 1rem;
    font-size: 0.85rem;
    color: #CBD5E1;
    line-height: 1.65;
}
.landing-section-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    min-height: 140px;
}
.landing-section-body, .landing-plan-detail {
    font-size: 0.82rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.45;
}
.section-badge-free, .section-badge-premium {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.15rem 0.45rem;
    border-radius: 999px;
    margin-bottom: 0.35rem;
}
.section-badge-free { background: #D1FAE5; color: #065F46; }
.section-badge-premium { background: #DBEAFE; color: #1E40AF; }
.landing-plan--free { border-color: #CBD5E1; }
.landing-plan--premium { border-color: #93C5FD; }
.landing-plan--pro { border-color: #C4B5FD; }
.section-lock-badge {
    display: inline-block;
    margin-left: 0.35rem;
    padding: 0.1rem 0.45rem;
    border-radius: 999px;
    background: #DBEAFE;
    color: #1E40AF;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    vertical-align: middle;
}
.report-tier-banner {
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    color: #92400E;
    margin: 0.75rem 0 1rem;
}
.locked-section-blur {
    position: relative;
    background: linear-gradient(160deg, #1e293b 0%, #0f172a 100%);
    border-radius: var(--ps-radius);
    padding: 2rem 1.5rem;
    margin: 0.75rem 0 1rem;
    min-height: 220px;
    overflow: hidden;
}
.locked-section-blur::before {
    content: "";
    position: absolute;
    inset: 0;
    backdrop-filter: blur(6px);
    opacity: 0.35;
    pointer-events: none;
}
.locked-overlay {
    position: relative;
    z-index: 1;
    color: #E2E8F0;
    text-align: center;
}
.locked-icon { font-size: 2rem; margin: 0 0 0.5rem; }
.locked-section-card {
    background: linear-gradient(160deg, #0F172A 0%, #1E293B 100%);
    border: 1px solid #334155;
    border-radius: var(--ps-radius);
    padding: 1.25rem 1.35rem;
    color: #E2E8F0;
    margin: 0.5rem 0 1rem;
}
.locked-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #93C5FD;
    margin: 0 0 0.35rem;
}
.locked-title { font-size: 1.15rem; font-weight: 700; margin: 0 0 0.5rem; color: #F8FAFC; }
.locked-copy { font-size: 0.9rem; line-height: 1.55; margin: 0 0 0.75rem; color: #CBD5E1; }
.locked-list {
    margin: 0;
    padding-left: 1.1rem;
    font-size: 0.85rem;
    line-height: 1.65;
    color: #E2E8F0;
}
.verdict-headline {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--ps-text);
    line-height: 1.45;
    margin: 0 0 1rem;
    padding: 0.85rem 1rem;
    background: linear-gradient(135deg, #EFF6FF 0%, #F8FAFC 100%);
    border-left: 4px solid var(--ps-blue);
    border-radius: 8px;
}
.action-item {
    font-size: 0.9rem;
    line-height: 1.45;
    padding: 0.65rem 0.85rem;
    border-radius: 8px;
    margin-bottom: 0.45rem;
    border: 1px solid var(--ps-border);
}
.action-item--risk { background: #FEF2F2; border-color: #FECACA; color: #991B1B; }
.action-item--opp { background: #ECFDF5; border-color: #A7F3D0; color: #065F46; }
.coming-soon-card {
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: var(--ps-radius);
    padding: 1.1rem 1.2rem;
    margin: 0.5rem 0;
}
.coming-soon-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ps-muted);
    margin: 0 0 0.35rem;
}
.coming-soon-title { font-size: 1.05rem; font-weight: 700; margin: 0 0 0.35rem; }
.coming-soon-copy { font-size: 0.88rem; color: #64748B; margin: 0; line-height: 1.5; }
.landing-value-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem 1.25rem;
    justify-content: center;
    font-size: 0.88rem;
    color: var(--ps-muted);
    margin: 1.25rem 0 0;
}

/* Dashboard visuals */
.insight-card--hero { border-left: 4px solid var(--ps-blue); }
.insight-card--marketing { border-left: 4px solid var(--ps-indigo); }
.card-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ps-muted);
    margin: 0 0 0.5rem;
}
.stat-tile {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    box-shadow: var(--ps-shadow);
    min-height: 110px;
}
.stat-tile-label { font-size: 0.78rem; font-weight: 600; color: var(--ps-muted); margin: 0 0 0.35rem; }
.stat-tile-value { font-size: 1.25rem; font-weight: 700; color: var(--ps-text); margin: 0; }
.stat-tile-body { font-size: 0.9rem; color: #475569; margin: 0; line-height: 1.5; }
.channel-head { display: flex; align-items: center; gap: 0.45rem; margin-bottom: 0.5rem; }
.channel-logo, .platform-logo { width: 20px; height: 20px; object-fit: contain; }
.channel-name { font-weight: 700; color: var(--ps-text); }
.metric-pill {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
}
.competitor-row {
    background: #FAFBFC;
    border: 1px solid var(--ps-border);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
}
.competitor-meta { font-size: 0.85rem; color: #64748B; margin: 0.35rem 0 0; }
.persona-card {
    background: linear-gradient(160deg, #EFF6FF 0%, #FFFFFF 100%);
    border: 1px solid #BFDBFE;
    border-radius: var(--ps-radius);
    padding: 1.25rem;
    box-shadow: var(--ps-shadow);
}
.persona-icon { font-size: 1.75rem; margin: 0; }
.persona-name { font-size: 1.15rem; font-weight: 700; margin: 0.35rem 0 0.15rem; }
.persona-meta { font-size: 0.82rem; color: var(--ps-muted); margin: 0 0 0.5rem; }
.persona-body { font-size: 0.92rem; color: #475569; margin: 0; line-height: 1.55; }
.chip-row { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.platform-chip, .format-chip {
    display: inline-block;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-radius: 999px;
    padding: 0.25rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #334155;
    margin: 0.15rem 0.25rem 0.15rem 0;
}
.strategy-card {
    border-radius: var(--ps-radius);
    padding: 1rem 1.05rem;
    margin-bottom: 0.75rem;
    border: 1px solid var(--ps-border);
    font-size: 0.92rem;
    line-height: 1.55;
    color: #475569;
}
.strategy-card--organic { background: #ECFDF5; border-color: #A7F3D0; }
.strategy-card--paid { background: #EFF6FF; border-color: #BFDBFE; }
.strategy-card-title { font-weight: 700; color: var(--ps-text); margin: 0 0 0.45rem; }
.platform-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: var(--ps-radius);
    padding: 1rem;
    box-shadow: var(--ps-shadow);
    margin-bottom: 0.5rem;
}
.platform-card-head { display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.35rem; font-weight: 700; }
.platform-score { font-size: 0.82rem; color: var(--ps-muted); margin: 0.25rem 0 0.5rem; }
.platform-body, .platform-evidence { font-size: 0.88rem; color: #475569; line-height: 1.5; margin: 0.5rem 0 0; }
.platform-evidence { font-size: 0.82rem; color: #64748B; }
.creative-card {
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-left: 4px solid var(--ps-blue);
    border-radius: 10px;
    padding: 1rem 1.05rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--ps-shadow);
}
.creative-format { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; color: var(--ps-muted); margin: 0 0 0.35rem; }
.creative-title { font-size: 1rem; font-weight: 700; margin: 0 0 0.35rem; color: var(--ps-text); }
.creative-hook { font-size: 0.88rem; margin: 0 0 0.35rem; color: #334155; }
.creative-copy { font-size: 0.88rem; color: #64748B; margin: 0; line-height: 1.5; }
.playbook-step {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--ps-border);
    font-size: 0.95rem;
    color: #334155;
}
.playbook-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.65rem;
    height: 1.65rem;
    border-radius: 999px;
    background: var(--ps-blue-deep);
    color: #fff;
    font-size: 0.78rem;
    font-weight: 700;
    flex-shrink: 0;
}
"""

SAAS_CHROME_CSS = """
header[data-testid="stHeader"] { display: none !important; }
"""


def inject_custom_css(*, saas_mode: bool = False) -> None:
    """Inject premium theme — must run immediately after st.set_page_config()."""
    css = PREMIUM_THEME_CSS
    if saas_mode:
        css += SAAS_CHROME_CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def form_step_header(step: str, icon: str, title: str) -> str:
    return (
        f'<div class="form-card-header">'
        f'<span class="step-pill">{step}</span>'
        f'<p class="form-card-title"><span>{icon}</span> {html.escape(title)}</p>'
        f"</div>"
    )
