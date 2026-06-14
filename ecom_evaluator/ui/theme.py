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
    --ps-nav-h: 72px;
    --ps-nav-accent: #7C3AED;
    --ps-nav-cta: #0F172A;
    --lp-panel-gradient: linear-gradient(135deg, #0B1F4B 0%, #1E40AF 48%, #4338CA 100%);
}

/* Global canvas */
.stApp {
    background-color: var(--ps-bg) !important;
    font-family: 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    overflow-y: auto !important;
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
.block-container { padding-top: 0 !important; max-width: 1180px; }
[data-testid="stMarkdownContainer"]:has(.site-header) {
    margin: 0 !important;
    padding: 0 !important;
}
[data-testid="stMarkdownContainer"]:has(.site-header) p {
    margin: 0 !important;
}

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

/* Site header — Jungle Scout-style fixed top bar */
.site-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 9999;
    overflow: visible;
}
.site-header__spacer {
    height: var(--ps-nav-h);
    width: 100%;
}
.site-header__bar {
    background: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
    box-shadow: 0 1px 0 rgba(15, 23, 42, 0.03);
    overflow: visible;
}
.site-header__inner {
    max-width: 1240px;
    margin: 0 auto;
    padding: 0 2rem;
    height: var(--ps-nav-h);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    overflow: visible;
}
.site-header__brand {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none !important;
    color: #000000;
    flex-shrink: 0;
    transition: opacity 0.15s ease;
}
.site-header__brand:hover {
    opacity: 0.85;
    text-decoration: none !important;
}
.site-header__mark {
    font-size: 1.2rem;
    line-height: 1;
}
.site-header__name {
    font-size: 1.125rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #000000;
}
.site-header__nav {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    margin-right: auto;
    margin-left: 2.5rem;
}
.site-header__link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.55rem 0.9rem;
    font-size: 0.9375rem;
    font-weight: 500;
    color: #000000;
    text-decoration: none !important;
    line-height: 1.2;
    white-space: nowrap;
    transition: color 0.15s ease;
}
.site-header__link:hover {
    color: var(--ps-blue-deep) !important;
    text-decoration: none !important;
}
.site-header__bar a.site-header__brand,
.site-header__bar a.site-header__link,
.site-header__bar a.site-header__login,
.site-header__bar a.site-header__text-action,
.site-header__bar .site-header__name,
.site-header__bar .site-header__user,
.site-header__bar .site-header__quota,
.site-header__bar .site-header__chevron,
[data-testid="stMarkdownContainer"]:has(.site-header) .site-header__bar a:not(.site-header__cta) {
    color: #000000 !important;
}
.site-header__dropdown:hover .site-header__dropdown-trigger,
.site-header__dropdown:focus-within .site-header__dropdown-trigger,
.site-header__dropdown:hover .site-header__chevron,
.site-header__dropdown:focus-within .site-header__chevron {
    color: var(--ps-blue-deep) !important;
}
.site-header__chevron {
    transition: transform 0.2s ease, color 0.15s ease;
}
.site-header__dropdown {
    position: relative;
}
.site-header__dropdown-trigger {
    position: relative;
    z-index: 10001;
}
.site-header__dropdown:hover .site-header__chevron,
.site-header__dropdown:focus-within .site-header__chevron {
    transform: rotate(180deg);
}
.site-header__dropdown-panel {
    position: absolute;
    top: 100%;
    left: 0;
    width: min(720px, calc(100vw - 2rem));
    padding-top: 10px;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transform: translateY(4px);
    transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s ease;
    z-index: 10000;
}
.site-header__dropdown:hover .site-header__dropdown-panel,
.site-header__dropdown:focus-within .site-header__dropdown-panel,
.site-header__dropdown-panel:hover {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateY(0);
}
.site-header__mega {
    display: grid;
    grid-template-columns: 1.05fr 1fr;
    gap: 0;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    box-shadow:
        0 4px 6px rgba(15, 23, 42, 0.04),
        0 24px 48px rgba(15, 23, 42, 0.12);
    overflow: hidden;
}
.site-header__mega-feature {
    padding: 1.75rem 1.6rem;
    background: #F9FAFB;
    border-right: 1px solid #EEF2F6;
}
.site-header__mega-kicker {
    margin: 0 0 0.65rem;
    font-size: 0.8125rem;
    font-style: italic;
    color: #6B7280;
}
.site-header__mega-title {
    margin: 0 0 0.55rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #111827;
    line-height: 1.3;
}
.site-header__mega-desc {
    margin: 0 0 1rem;
    font-size: 0.875rem;
    line-height: 1.55;
    color: #4B5563;
}
.site-header__mega-link {
    display: inline-flex;
    align-items: center;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--ps-blue-deep);
    text-decoration: none !important;
    transition: opacity 0.15s ease;
}
.site-header__mega-link:hover {
    opacity: 0.82;
    text-decoration: none !important;
}
.site-header__mega-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    padding: 1.35rem 1.5rem 1.5rem;
}
.site-header__mega-col {
    padding: 0 1rem;
}
.site-header__mega-col:first-child {
    border-right: 1px solid #EEF2F6;
}
.site-header__mega-heading {
    margin: 0 0 0.85rem;
    font-size: 0.8125rem;
    font-style: italic;
    font-weight: 500;
    color: #6B7280;
}
.site-header__mega-item {
    display: block;
    padding: 0.45rem 0;
    font-size: 0.9375rem;
    font-weight: 500;
    color: #111827;
    text-decoration: none !important;
    line-height: 1.4;
    transition: color 0.12s ease;
}
.site-header__mega-item:hover {
    color: var(--ps-blue-deep);
    text-decoration: none !important;
}
.site-header__actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.35rem;
    flex-shrink: 0;
}
.site-header__divider {
    display: none;
}
.site-header__login {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.55rem 0.85rem;
    font-size: 0.9375rem;
    font-weight: 500;
    color: #000000;
    text-decoration: underline !important;
    text-underline-offset: 3px;
    line-height: 1;
    white-space: nowrap;
    transition: color 0.15s ease;
}
.site-header__login:hover {
    color: var(--ps-blue-deep) !important;
    text-decoration: underline !important;
}
.site-header__text-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.55rem 0.85rem;
    font-size: 0.9375rem;
    font-weight: 500;
    color: #000000;
    text-decoration: none !important;
    line-height: 1;
    white-space: nowrap;
    transition: color 0.15s ease;
}
.site-header__text-action:hover {
    color: var(--ps-blue-deep) !important;
    text-decoration: none !important;
}
.site-header__cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.62rem 1.2rem;
    border-radius: 999px;
    font-size: 0.9375rem;
    font-weight: 600;
    color: #FFFFFF !important;
    text-decoration: none !important;
    line-height: 1;
    white-space: nowrap;
    background: linear-gradient(135deg, #2563EB 0%, #1E40AF 52%, #4338CA 100%);
    box-shadow: 0 1px 2px rgba(30, 64, 175, 0.2), 0 8px 20px rgba(37, 99, 235, 0.28);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
.site-header__cta:hover {
    filter: brightness(1.06);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(30, 64, 175, 0.22), 0 12px 28px rgba(37, 99, 235, 0.32);
    text-decoration: none !important;
}
.site-header__cta--compact {
    padding: 0.58rem 1rem;
    font-size: 0.875rem;
}
.site-header__user {
    font-size: 0.8125rem;
    color: #000000;
    max-width: 11rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.site-header__quota {
    font-size: 0.74rem !important;
    margin: 0 !important;
    color: #000000 !important;
}
.site-header__bar .check-row {
    color: #000000 !important;
}
@media (max-width: 960px) {
    .site-header__nav { margin-left: 1rem; gap: 0; }
    .site-header__inner { padding: 0 1.25rem; }
    .site-header__mega { grid-template-columns: 1fr; }
    .site-header__mega-feature { border-right: none; border-bottom: 1px solid #EEF2F6; }
    .site-header__user { display: none; }
}
@media (max-width: 640px) {
    .site-header__inner { padding: 0 1rem; gap: 1rem; }
    .site-header__quota { display: none; }
    .site-header__mega-grid { grid-template-columns: 1fr; padding: 1rem; }
    .site-header__mega-col:first-child { border-right: none; border-bottom: 1px solid #EEF2F6; padding-bottom: 1rem; margin-bottom: 0.5rem; }
}
.auth-card--standalone {
    max-width: 520px;
    margin: 1rem auto 2rem;
}

/* Auth screen — centered Superhuman-style layout */
.auth-screen {
    max-width: 400px;
    margin: 2.5rem auto 2rem;
    padding: 0 0.25rem;
}
.auth-screen-header {
    text-align: center;
    margin-bottom: 1.75rem;
}
.auth-screen-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    margin: 0 auto 1.1rem;
    border-radius: 12px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    font-size: 1.45rem;
    line-height: 1;
    box-shadow: inset 0 0 0 1px rgba(59, 130, 246, 0.12);
}
.auth-screen-title {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #000000;
    line-height: 1.25;
}
.auth-oauth-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.65rem;
    width: 100%;
    min-height: 3rem;
    padding: 0.7rem 1rem;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    background: #FFFFFF;
    color: #111827;
    font-size: 0.9375rem;
    font-weight: 500;
    text-decoration: none !important;
    transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    box-sizing: border-box;
}
.auth-oauth-btn:hover {
    background: #F9FAFB;
    border-color: #D1D5DB;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    text-decoration: none !important;
}
.auth-oauth-icon {
    flex-shrink: 0;
}
.auth-screen-divider {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin: 1.35rem 0 1.25rem;
}
.auth-field-label {
    margin: 0 0 0.4rem;
    font-size: 0.8125rem;
    font-weight: 500;
    color: #6B7280;
}
.auth-field-optional {
    font-weight: 400;
    color: #9CA3AF;
}
.auth-screen [data-testid="stForm"] {
    margin: 0;
    padding: 0;
    border: none;
    background: transparent;
}
.auth-screen [data-testid="stForm"] [data-testid="InputInstructions"],
.auth-screen [data-testid="stForm"] [data-testid="stCaptionContainer"] {
    display: none;
}
.auth-screen [data-testid="stForm"] [data-testid="stTextInput"] {
    margin-bottom: 0.85rem;
}
.auth-screen [data-testid="stForm"] input {
    min-height: 3rem;
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    font-size: 0.9375rem !important;
    color: #111827 !important;
    background: #FFFFFF !important;
    box-shadow: none !important;
}
.auth-screen [data-testid="stForm"] input:focus {
    border-color: #93C5FD !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}
.auth-screen [data-testid="stForm"] .stButton {
    margin-top: 0.35rem;
}
.auth-screen [data-testid="stForm"] .stButton > button[kind="primary"] {
    min-height: 3rem;
    border-radius: 10px !important;
    font-size: 0.9375rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #2563EB 0%, #1E40AF 52%, #4338CA 100%) !important;
    border: none !important;
    box-shadow: 0 1px 2px rgba(30, 64, 175, 0.2), 0 8px 20px rgba(37, 99, 235, 0.22) !important;
}
.auth-screen [data-testid="stForm"] .stButton > button[kind="primary"]:hover {
    filter: brightness(1.05);
    transform: translateY(-1px);
}
.auth-screen > .stButton > button,
.auth-screen .stButton:not([data-testid="stForm"] .stButton) > button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #374151 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 0 !important;
    margin-top: 0.75rem;
}
.auth-screen > .stButton > button:hover,
.auth-screen .stButton:not([data-testid="stForm"] .stButton) > button:hover {
    color: var(--ps-blue-deep) !important;
    background: transparent !important;
}
.auth-screen-footer {
    margin-top: 1.75rem;
    text-align: center;
}
.auth-screen-footer p {
    margin: 0 0 0.45rem;
    font-size: 0.75rem;
    line-height: 1.55;
    color: #6B7280;
}
.auth-screen-footer-muted {
    color: #9CA3AF !important;
    font-size: 0.72rem !important;
}
.auth-screen [data-testid="stAlert"] {
    margin: 0 0 1rem;
    border-radius: 10px;
}

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
.stLinkButton > a {
    border-radius: 8px !important;
    font-weight: 700 !important;
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
.cliffhanger-banner {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    color: #F8FAFC;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 16px 40px rgba(49, 46, 129, 0.25);
    margin: 0.25rem 0;
}
.cliffhanger-kicker {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #C4B5FD;
    margin: 0 0 0.4rem;
}
.cliffhanger-title {
    font-size: 1.15rem;
    font-weight: 800;
    margin: 0 0 0.45rem;
    letter-spacing: -0.02em;
}
.cliffhanger-copy {
    font-size: 0.88rem;
    color: #CBD5E1;
    margin: 0;
    line-height: 1.55;
    max-width: 720px;
}
.verdict-banner {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.25rem 1.35rem;
    border-radius: 14px;
    margin: 1.5rem 0 0.65rem;
    border: 2px solid transparent;
}
.verdict-banner--go {
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border-color: #6EE7B7;
}
.verdict-banner--caution {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
    border-color: #FCD34D;
}
.verdict-banner--nogo {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
    border-color: #FCA5A5;
}
.verdict-banner-emoji { font-size: 2rem; margin: 0; line-height: 1; }
.verdict-banner-copy { flex: 1; }
.verdict-banner-label {
    font-size: 1.05rem;
    font-weight: 800;
    margin: 0 0 0.2rem;
    color: var(--ps-text);
    letter-spacing: 0.02em;
}
.verdict-banner-subtitle {
    font-size: 0.88rem;
    margin: 0;
    color: var(--ps-muted);
}
.verdict-banner-score {
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    color: var(--ps-blue-deep);
    line-height: 1;
}
.verdict-banner-score span { font-size: 0.95rem; color: var(--ps-muted); font-weight: 600; }
.verdict-banner-context {
    font-size: 0.82rem;
    color: var(--ps-muted);
    margin: 0 0 0.5rem;
    font-style: italic;
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
.landing-wrap { margin: 0.5rem 0 0; }
/* Landing page — clean white canvas; checkered pattern only on Compare band */
.block-container:has(.landing-hero) {
    background-color: #FFFFFF;
}
.stApp:has(.landing-hero) {
    background-color: #FFFFFF !important;
}
.lp-hero-cta-gap {
    height: 2rem;
    width: 100%;
    margin-bottom: 0.35rem;
}

/* Landing product carousel */
.lp-carousel-section {
    margin: 1.75rem 0 0.5rem;
    padding: 0 0 0.25rem;
}
.lp-carousel-header {
    text-align: center;
    max-width: 640px;
    margin: 0 auto 1.5rem;
    padding: 0 0.25rem;
}
.lp-carousel-title {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0F172A;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.lp-carousel-lead {
    font-size: 0.92rem;
    color: #64748B;
    margin: 0;
    line-height: 1.55;
}
.lp-carousel-shell {
    position: relative;
    width: 100%;
}
.lp-carousel-shell::before,
.lp-carousel-shell::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    width: 72px;
    z-index: 2;
    pointer-events: none;
}
.lp-carousel-shell::before {
    left: 0;
    background: linear-gradient(90deg, #FFFFFF 0%, rgba(255, 255, 255, 0.92) 35%, transparent 100%);
}
.lp-carousel-shell::after {
    right: 0;
    background: linear-gradient(270deg, #FFFFFF 0%, rgba(255, 255, 255, 0.92) 35%, transparent 100%);
}
.lp-carousel-viewport {
    position: relative;
    overflow: hidden;
    width: 100%;
    padding: 0.85rem 0.5rem 1.15rem;
    cursor: grab;
    touch-action: pan-y;
    user-select: none;
    -webkit-user-select: none;
}
.lp-carousel-viewport.is-grabbing {
    cursor: grabbing;
}
.lp-carousel-viewport.is-grabbing .lp-carousel-card {
    pointer-events: none;
}
.lp-carousel-viewport.is-grabbing .lp-carousel-card:hover {
    transform: none;
    box-shadow: 0 4px 6px rgba(15, 23, 42, 0.05), 0 16px 32px rgba(15, 23, 42, 0.08);
}
.lp-carousel-track {
    display: flex;
    gap: 1.75rem;
    width: max-content;
    will-change: transform;
    transform: translate3d(0, 0, 0);
    padding: 0.35rem 0.5rem;
}
.lp-carousel-card {
    flex: 0 0 320px;
    width: 320px;
    min-height: 470px;
    display: flex;
    flex-direction: column;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(15, 23, 42, 0.05), 0 16px 32px rgba(15, 23, 42, 0.08);
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.28s ease;
}
.lp-carousel-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 10px 15px rgba(15, 23, 42, 0.06), 0 24px 48px rgba(15, 23, 42, 0.12);
}
.lp-carousel-card-media {
    position: relative;
    aspect-ratio: 4 / 3;
    overflow: hidden;
    flex-shrink: 0;
}
.lp-carousel-media-fallback {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 0;
}
.lp-carousel-media-icon {
    font-size: 3.25rem;
    line-height: 1;
    filter: drop-shadow(0 8px 16px rgba(15, 23, 42, 0.12));
    opacity: 0.92;
}
.lp-carousel-card-media img {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    pointer-events: none;
    -webkit-user-drag: none;
    background: transparent;
}
.lp-carousel-card-media img.is-broken {
    opacity: 0;
    visibility: hidden;
}
.lp-carousel-card-body {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 1.15rem 1.25rem 1.25rem;
}
.lp-carousel-card-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    align-items: stretch;
}
.lp-carousel-card-footer {
    margin-top: auto;
    padding-top: 1rem;
    border-top: 1px solid #F1F5F9;
}
.lp-carousel-category {
    display: block;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748B;
    margin: 0 0 0.4rem;
}
.lp-carousel-name {
    font-size: 1rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 0.85rem;
    line-height: 1.3;
    min-height: 2.6rem;
}
.lp-carousel-score-row {
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    gap: 0.55rem;
    min-height: 2.1rem;
}
.lp-carousel-score {
    display: inline-flex;
    align-items: baseline;
    gap: 0.15rem;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    padding: 0.28rem 0.6rem;
    border-radius: 10px;
    flex-shrink: 0;
}
.lp-carousel-score span {
    font-size: 0.78rem;
    font-weight: 600;
    opacity: 0.72;
}
.lp-carousel-score--high {
    color: #047857;
    background: rgba(236, 253, 245, 0.95);
    border: 1px solid #A7F3D0;
}
.lp-carousel-score--mid {
    color: #B45309;
    background: rgba(255, 251, 235, 0.98);
    border: 1px solid #FDE68A;
}
.lp-carousel-score--low {
    color: #B91C1C;
    background: rgba(254, 242, 242, 0.98);
    border: 1px solid #FECACA;
}
.lp-carousel-trend {
    display: inline-flex;
    align-items: center;
    font-size: 0.68rem;
    font-weight: 700;
    color: #4338CA;
    background: #EEF2FF;
    border: 1px solid #C7D2FE;
    border-radius: 999px;
    padding: 0.28rem 0.55rem;
    line-height: 1.2;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 100%;
}
.lp-carousel-divider {
    height: 1px;
    background: #E2E8F0;
    margin: 0.9rem 0 0.8rem;
    width: 100%;
}
.lp-carousel-profit {
    font-size: 0.88rem;
    color: #475569;
    margin: 0 0 0.3rem;
    line-height: 1.45;
}
.lp-carousel-profit strong {
    color: #059669;
    font-weight: 800;
    font-size: 1rem;
}
.lp-carousel-margin {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    margin: 0;
    line-height: 1.45;
}
.lp-carousel-demo-link {
    display: inline-flex;
    align-items: center;
    font-size: 0.82rem;
    font-weight: 700;
    color: #1E40AF;
    text-decoration: none;
    opacity: 0.92;
    transition: opacity 0.15s ease, color 0.15s ease, transform 0.15s ease;
}
.lp-carousel-card:hover .lp-carousel-demo-link {
    opacity: 1;
    color: #4338CA;
    transform: translateX(2px);
}
@media (max-width: 1024px) {
    .lp-carousel-card {
        flex: 0 0 300px;
        width: 300px;
        min-height: 450px;
    }
    .lp-carousel-track {
        gap: 1.35rem;
    }
}
@media (max-width: 640px) {
    .lp-carousel-card {
        flex: 0 0 min(82vw, 320px);
        width: min(82vw, 320px);
    }
    .lp-carousel-shell::before,
    .lp-carousel-shell::after {
        width: 40px;
    }
}
@media (prefers-reduced-motion: reduce) {
    .lp-carousel-track {
        flex-wrap: wrap;
        width: 100%;
        justify-content: center;
        transform: none !important;
    }
    .lp-carousel-viewport {
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        cursor: default;
    }
    .lp-carousel-shell::before,
    .lp-carousel-shell::after {
        display: none;
    }
    .lp-carousel-card {
        scroll-snap-align: center;
    }
}

.landing-hero {
    background: var(--lp-panel-gradient);
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
    text-align: center !important;
    display: block;
}
.landing-hero .landing-kicker,
.landing-hero .landing-title,
.landing-hero .landing-lead {
    text-align: center !important;
}
[data-testid="stMarkdownContainer"]:has(.landing-hero) p.landing-lead {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
    max-width: 680px;
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

/* Scroll reveal — visible by default; animate in after JS binds observers */
.lp-reveal {
    opacity: 1;
    transform: none;
}
html.lp-reveal-ready .lp-reveal:not(.lp-reveal-hero):not(.is-visible) {
    opacity: 0;
    transform: translateY(28px);
}
html.lp-reveal-ready .lp-reveal-left:not(.is-visible) {
    opacity: 0;
    transform: translateX(-32px);
}
html.lp-reveal-ready .lp-reveal-right:not(.is-visible) {
    opacity: 0;
    transform: translateX(32px);
}
html.lp-reveal-ready .lp-reveal-scale:not(.is-visible) {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
}
@keyframes lp-rise {
    from { opacity: 0; transform: translateY(28px); }
    to { opacity: 1; transform: none; }
}
@keyframes lp-rise-left {
    from { opacity: 0; transform: translateX(-32px); }
    to { opacity: 1; transform: none; }
}
@keyframes lp-rise-right {
    from { opacity: 0; transform: translateX(32px); }
    to { opacity: 1; transform: none; }
}
@keyframes lp-rise-scale {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to { opacity: 1; transform: none; }
}
html.lp-reveal-ready .lp-reveal.is-visible {
    animation: lp-rise 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
html.lp-reveal-ready .lp-reveal-left.is-visible {
    animation: lp-rise-left 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
html.lp-reveal-ready .lp-reveal-right.is-visible {
    animation: lp-rise-right 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
html.lp-reveal-ready .lp-reveal-scale.is-visible {
    animation: lp-rise-scale 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
html.lp-reveal-ready .lp-reveal.is-visible.lp-reveal-delay-1,
html.lp-reveal-ready .lp-reveal-left.is-visible.lp-reveal-delay-1,
html.lp-reveal-ready .lp-reveal-right.is-visible.lp-reveal-delay-1,
html.lp-reveal-ready .lp-reveal-scale.is-visible.lp-reveal-delay-1 { animation-delay: 0.08s; }
html.lp-reveal-ready .lp-reveal.is-visible.lp-reveal-delay-2,
html.lp-reveal-ready .lp-reveal-left.is-visible.lp-reveal-delay-2,
html.lp-reveal-ready .lp-reveal-right.is-visible.lp-reveal-delay-2,
html.lp-reveal-ready .lp-reveal-scale.is-visible.lp-reveal-delay-2 { animation-delay: 0.16s; }
html.lp-reveal-ready .lp-reveal.is-visible.lp-reveal-delay-3,
html.lp-reveal-ready .lp-reveal-left.is-visible.lp-reveal-delay-3,
html.lp-reveal-ready .lp-reveal-right.is-visible.lp-reveal-delay-3,
html.lp-reveal-ready .lp-reveal-scale.is-visible.lp-reveal-delay-3 { animation-delay: 0.24s; }
html.lp-reveal-ready .lp-reveal.is-visible.lp-reveal-delay-4,
html.lp-reveal-ready .lp-reveal-left.is-visible.lp-reveal-delay-4,
html.lp-reveal-ready .lp-reveal-right.is-visible.lp-reveal-delay-4,
html.lp-reveal-ready .lp-reveal-scale.is-visible.lp-reveal-delay-4 { animation-delay: 0.32s; }
@keyframes lp-hero-rise {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: none; }
}
.landing-hero .lp-reveal-hero {
    opacity: 0;
    animation: lp-hero-rise 0.75s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.landing-hero .lp-reveal-hero.lp-reveal-delay-1 { animation-delay: 0.1s; }
.landing-hero .lp-reveal-hero.lp-reveal-delay-2 { animation-delay: 0.2s; }
.landing-hero .lp-reveal-hero.lp-reveal-delay-3 { animation-delay: 0.3s; }

/* Full-bleed landing bands — transparent shells on shared page gradient */
.lp-band {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 3.25rem 0;
    overflow: hidden;
    background: transparent;
}
.lp-band::after {
    display: none;
}
.lp-band-inner {
    position: relative;
    z-index: 1;
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.25rem;
}
.lp-band-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 1;
}
.lp-band-label {
    display: inline-block;
    margin-bottom: 0.85rem;
    padding: 0.28rem 0.7rem;
    border-radius: 999px;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    background: rgba(255, 255, 255, 0.88);
    color: #1E40AF;
    border: 1px solid rgba(147, 197, 253, 0.55);
    backdrop-filter: blur(8px);
}
.lp-band--glance {
    padding-top: 2.5rem;
}
.lp-band--glance .lp-band-bg,
.lp-band--premium .lp-band-bg,
.lp-band--process .lp-band-bg,
.lp-band--sample .lp-band-bg,
.lp-band--faq .lp-band-bg {
    display: none;
}
.lp-band--glance .lp-value-tile,
.lp-band--process .lp-step-card,
.lp-band--sample .lp-preview-card,
.lp-band--compare .lp-compare-wrap {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(6px);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}
.lp-band--glance .lp-value-tile {
    border-color: rgba(191, 219, 254, 0.7);
    border-left-color: #3B82F6;
}
.lp-band--process .lp-step-card {
    border-color: rgba(226, 232, 240, 0.9);
}
.lp-band--sample .lp-preview-card {
    border: 1px solid rgba(226, 232, 240, 0.9);
}
.lp-band--compare .lp-compare-wrap {
    border: 1px solid rgba(226, 232, 240, 0.9);
}
.lp-band--compare .lp-band-bg {
    background:
        linear-gradient(rgba(191, 219, 254, 0.42) 1px, transparent 1px),
        linear-gradient(90deg, rgba(191, 219, 254, 0.42) 1px, transparent 1px),
        #FFFFFF;
    background-size: 30px 30px, 30px 30px, 100% 100%;
}
.lp-band--compare .lp-compare-table th {
    background: rgba(248, 250, 252, 0.95);
    color: var(--ps-text);
}
.lp-band--process .lp-step-num {
    background: linear-gradient(135deg, #2563EB 0%, #4338CA 100%);
}
/* Section 2 — full-bleed panel blue (same as Premium pricing box) */
.lp-band--free {
    padding: 4.5rem 0;
}
.lp-band--free .lp-band-bg {
    background: var(--lp-panel-gradient);
}
.lp-band--free .lp-band-label {
    background: rgba(255, 255, 255, 0.12);
    color: #BFDBFE;
    border-color: rgba(255, 255, 255, 0.22);
}
.lp-band--free .lp-section-header-title { color: #F8FAFC; }
.lp-band--free .lp-section-header-lead { color: #CBD5E1; }
.lp-band--free .lp-section-card {
    background: rgba(255, 255, 255, 0.97);
    border-color: rgba(255, 255, 255, 0.35);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
}
/* Section 3 — pricing box keeps the panel blue; band stays on clean white canvas */
.lp-band--premium .lp-pricing-card--premium {
    background: var(--lp-panel-gradient);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 22px 55px rgba(30, 58, 138, 0.24);
    color: #F8FAFC;
}
.lp-band--premium .lp-pricing-tier,
.lp-band--premium .lp-pricing-blurb,
.lp-band--premium .lp-pricing-features li {
    color: #E2E8F0;
    border-top-color: rgba(255, 255, 255, 0.12);
}
.lp-band--premium .lp-pricing-price { color: #FFFFFF; }
.lp-band--premium .lp-popular-pill {
    background: rgba(255, 255, 255, 0.16);
    color: #E0E7FF;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: none;
}
.lp-band--final {
    padding: 0.5rem 0 0;
    background: transparent;
}
.lp-band--final .lp-band-inner {
    padding: 0 1.25rem;
}
.lp-band--final .lp-band-bg { display: none; }
.lp-faq-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-width: 760px;
    margin: 0 auto;
}
.lp-faq-item {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 14px;
    padding: 0.15rem 1rem;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    backdrop-filter: blur(6px);
}
.lp-faq-item summary {
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 700;
    color: #1E3A8A;
    padding: 0.85rem 0;
    list-style: none;
}
.lp-faq-item summary::-webkit-details-marker { display: none; }
.lp-faq-item summary::after {
    content: "+";
    float: right;
    font-weight: 400;
    color: #4338CA;
}
.lp-faq-item[open] summary::after { content: "−"; }
.lp-faq-answer {
    margin: 0 0 1rem;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #475569;
    border-top: 1px solid rgba(199, 210, 254, 0.45);
    padding-top: 0.75rem;
}
.lp-page-flow + .lp-page-flow,
.lp-hero-cta-gap + [data-testid="stVerticalBlock"] + [data-testid="stMarkdownContainer"] .lp-page-flow {
    margin-top: 0;
}

.lp-page-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 0 0 1.5rem;
}
.lp-page-divider::before,
.lp-page-divider::after {
    content: "";
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--ps-border) 20%, var(--ps-border) 80%, transparent);
}
.lp-page-divider span {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--ps-muted);
    white-space: nowrap;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
}
.lp-page-divider--band {
    margin-top: 2.75rem;
    padding: 2rem 1rem 0.5rem;
    background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    border: 1px solid var(--ps-border);
    border-bottom: none;
    border-radius: 20px 20px 0 0;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.85);
}
.lp-page-divider--band::before,
.lp-page-divider--band::after { background: linear-gradient(90deg, transparent, #CBD5E1 30%, #CBD5E1 70%, transparent); }
.lp-band-end {
    height: 1.75rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(180deg, #F1F5F9 0%, #F8FAFC 100%);
    border: 1px solid var(--ps-border);
    border-top: none;
    border-radius: 0 0 20px 20px;
}
.lp-value-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 0 0 1rem;
}
.lp-value-tile {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.35rem;
    padding: 1.15rem 1.1rem;
    background: var(--ps-surface);
    border: 1px solid var(--ps-border);
    border-radius: 14px;
    box-shadow: var(--ps-shadow);
    border-left: 4px solid var(--ps-blue);
    min-height: 118px;
}
.lp-value-icon {
    font-size: 1.35rem;
    line-height: 1;
    margin-bottom: 0.15rem;
}
.lp-value-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: var(--ps-text);
    margin: 0;
    line-height: 1.25;
}
.lp-value-desc {
    font-size: 0.8rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.45;
}
.lp-section-header {
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2rem;
}
.lp-section-header-kicker {
    display: none;
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
    .lp-value-grid { grid-template-columns: 1fr; }
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
.lp-premium-pill {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    background: #DBEAFE;
    color: #1E40AF;
    border: 1px solid #93C5FD;
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
.lp-pricing-card--solo { max-width: 640px; margin: 0 auto; }
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
    margin: 0;
    padding: 3.25rem 2rem;
    text-align: center;
    background: var(--lp-panel-gradient);
    border-radius: 20px;
    color: #F8FAFC;
    box-shadow: 0 24px 60px rgba(30, 64, 175, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.lp-final-cta .lp-final-kicker,
.lp-final-cta .lp-final-title,
.lp-final-cta .lp-final-lead {
    text-align: center !important;
}
[data-testid="stMarkdownContainer"]:has(.lp-final-cta) p,
[data-testid="stMarkdownContainer"]:has(.lp-final-cta) h2 {
    text-align: center !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
.lp-final-cta-gap {
    height: 2rem;
    width: 100%;
    margin-bottom: 0.35rem;
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
    margin: 0 auto;
    max-width: 520px;
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
    margin: 1.5rem 0 2.5rem;
}

/* Tool workspace (evaluation form) */
.auth-card {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #BFDBFE;
    border-radius: 16px;
    padding: 1.25rem 1.35rem;
    margin: 1.5rem 0 1rem;
    box-shadow: var(--ps-shadow);
}
.auth-card-kicker {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ps-blue);
    margin: 0 0 0.35rem;
}
.auth-card-title {
    font-size: 1.15rem;
    font-weight: 800;
    margin: 0 0 0.35rem;
    color: var(--ps-text);
}
.auth-card-copy {
    font-size: 0.88rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.5;
}
.auth-gate-panel { margin-bottom: 1rem; }
.auth-divider {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.25rem 0 1rem;
    color: var(--ps-muted);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.auth-divider::before,
.auth-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #E2E8F0;
}
.auth-divider span { white-space: nowrap; }
.tool-workspace-hero {
    background: linear-gradient(135deg, #0B1F4B 0%, #1E40AF 48%, #4338CA 100%);
    border-radius: 18px;
    padding: 2rem 2.1rem 1.85rem;
    color: #F8FAFC;
    margin-bottom: 1.75rem;
    box-shadow: 0 20px 50px rgba(30, 64, 175, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}
.tool-workspace-hero::before {
    content: "";
    position: absolute;
    top: -35%;
    right: -10%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.tool-workspace-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #BFDBFE;
    margin: 0 0 0.5rem;
    position: relative;
}
.tool-workspace-title {
    font-size: clamp(1.45rem, 3vw, 1.85rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 0.55rem;
    line-height: 1.15;
    position: relative;
}
.tool-workspace-copy {
    font-size: 0.92rem;
    color: #CBD5E1;
    margin: 0;
    max-width: 640px;
    line-height: 1.6;
    position: relative;
}
.tool-workspace-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 1rem;
    position: relative;
}
.tool-workspace-badge {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.16);
    color: #E2E8F0;
}
.tool-workspace-compact {
    background: linear-gradient(135deg, #EFF6FF 0%, #F8FAFC 100%);
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 1rem 1.15rem;
    margin-bottom: 1.25rem;
}
.tool-workspace-compact-title {
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.25rem;
    color: var(--ps-text);
}
.tool-workspace-compact-copy {
    font-size: 0.84rem;
    color: var(--ps-muted);
    margin: 0;
}
.form-section-header {
    margin: 1.35rem 0 0.75rem;
}
.form-section-header:first-of-type { margin-top: 0; }
.form-section-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    margin-bottom: 0.45rem;
}
.form-section-badge--required {
    background: #DBEAFE;
    color: #1E40AF;
    border: 1px solid #93C5FD;
}
.form-section-badge--optional {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #CBD5E1;
}
.form-section-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: var(--ps-text);
    margin: 0 0 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.form-section-subtitle {
    font-size: 0.84rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.45;
}
.form-subsection-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #64748B;
    margin: 0.75rem 0 0.35rem;
}
.form-field-hint {
    font-size: 0.78rem;
    color: var(--ps-muted);
    margin: 0.35rem 0 0.5rem;
    line-height: 1.45;
}
.form-action-intro {
    background: linear-gradient(160deg, #EFF6FF 0%, #FFFFFF 100%);
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.85rem;
}
.form-action-kicker {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ps-blue);
    margin: 0 0 0.25rem;
}
.form-action-title {
    font-size: 1.05rem;
    font-weight: 800;
    margin: 0 0 0.25rem;
    color: var(--ps-text);
}
.form-action-copy {
    font-size: 0.82rem;
    color: var(--ps-muted);
    margin: 0;
    line-height: 1.45;
}
.readiness-card--premium {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 1rem 1.05rem;
    box-shadow: var(--ps-shadow);
    margin-bottom: 1rem;
}
.readiness-quota {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.85rem;
    padding-top: 0.75rem;
    border-top: 1px dashed #CBD5E1;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--ps-blue-deep);
}
.readiness-quota-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: var(--ps-blue);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}
.form-run-footnote {
    text-align: center;
    font-size: 0.76rem;
    color: var(--ps-muted);
    margin: 0.65rem 0 0;
    line-height: 1.4;
}
div[data-testid="stExpander"] {
    background: var(--ps-surface) !important;
    border: 1px solid var(--ps-border) !important;
    border-radius: 14px !important;
    box-shadow: var(--ps-shadow) !important;
    overflow: hidden;
}
div[data-testid="stExpander"] details summary {
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    color: var(--ps-text) !important;
    padding: 0.85rem 1rem !important;
    background: linear-gradient(180deg, #FAFBFC 0%, #FFFFFF 100%) !important;
}
div[data-testid="stExpander"] details summary:hover {
    color: var(--ps-blue-deep) !important;
}
div[data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid var(--ps-border) !important;
}
.form-workspace-marker + div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
    border-top: 4px solid var(--ps-blue) !important;
}

/* Tool intro (legacy) */
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
.tool-intro-copy {
    font-size: 0.88rem;
    color: var(--ps-muted);
    margin: 0.35rem 0 0;
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

/* Section 6 — Competitor Review Sentiment dashboard */
.s6-dashboard {
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
    margin-top: 0.5rem;
}
.s6-header {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.35rem 1.4rem;
    box-shadow: var(--ps-shadow);
}
.s6-kicker {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #64748B;
    margin: 0 0 0.35rem;
}
.s6-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 0.35rem;
    letter-spacing: -0.02em;
}
.s6-subtitle {
    font-size: 0.92rem;
    color: #475569;
    margin: 0 0 0.85rem;
    line-height: 1.55;
}
.s6-summary {
    font-size: 0.9rem;
    color: #334155;
    margin: 0;
    line-height: 1.6;
    padding-top: 0.85rem;
    border-top: 1px solid #E2E8F0;
}
.s6-card {
    border-radius: 16px;
    border: 1px solid transparent;
    padding: 1.25rem 1.3rem;
    box-shadow: var(--ps-shadow);
}
.s6-card-title {
    font-size: 1rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0 0 0.25rem;
}
.s6-card-lead {
    font-size: 0.82rem;
    color: #64748B;
    margin: 0 0 1rem;
}
.s6-card--pain {
    background: rgba(254, 242, 242, 0.5);
    border-color: #FECACA;
}
.s6-card--win {
    background: rgba(236, 253, 245, 0.5);
    border-color: #A7F3D0;
}
.s6-card--hooks {
    background: #FFFFFF;
    border-color: #E2E8F0;
}
.s6-pain-grid,
.s6-win-grid,
.s6-hook-grid {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.s6-pain-row,
.s6-win-row,
.s6-hook-card {
    background: rgba(255, 255, 255, 0.88);
    border-radius: 12px;
    padding: 1rem 1.05rem;
    border: 1px solid rgba(255, 255, 255, 0.7);
}
.s6-pain-row {
    border-color: #FECACA;
}
.s6-win-row {
    border-color: #BBF7D0;
}
.s6-hook-card {
    border-color: #E2E8F0;
}
.s6-pain-row-head,
.s6-win-row-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.55rem;
}
.s6-pain-category,
.s6-win-category {
    font-size: 0.92rem;
    font-weight: 800;
    color: #991B1B;
    margin: 0;
}
.s6-win-category { color: #065F46; }
.s6-pain-trend,
.s6-win-directive,
.s6-hook-copy {
    font-size: 0.88rem;
    color: #334155;
    line-height: 1.55;
    margin: 0;
}
.s6-pain-evidence {
    font-size: 0.8rem;
    color: #64748B;
    margin: 0.65rem 0 0;
    line-height: 1.5;
}
.s6-pain-evidence span {
    font-weight: 700;
    color: #B91C1C;
}
.s6-anger-track {
    width: 140px;
    height: 8px;
    background: #FEE2E2;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.35rem;
}
.s6-anger-fill {
    height: 100%;
    background: linear-gradient(90deg, #F87171 0%, #DC2626 100%);
    border-radius: 999px;
}
.s6-anger-label {
    font-size: 0.72rem;
    color: #991B1B;
    margin: 0.35rem 0 0;
    white-space: nowrap;
}
.s6-roi-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;
}
.s6-roi-badge--high {
    background: #DCFCE7;
    color: #166534;
    border: 1px solid #86EFAC;
}
.s6-roi-badge--low {
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
}
.s6-hook-angle {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #4338CA;
    margin: 0 0 0.45rem;
}
@media (max-width: 768px) {
    .s6-pain-row-head,
    .s6-win-row-head {
        flex-direction: column;
        gap: 0.35rem;
    }
    .s6-anger-track { width: 100%; }
}

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


def tool_workspace_hero(*, kicker: str, title: str, copy: str) -> str:
    return (
        f'<div class="tool-workspace-hero">'
        f'<p class="tool-workspace-kicker">{html.escape(kicker)}</p>'
        f'<p class="tool-workspace-title">{html.escape(title)}</p>'
        f'<p class="tool-workspace-copy">{html.escape(copy)}</p>'
        f'<div class="tool-workspace-badges">'
        f'<span class="tool-workspace-badge">2 sections free</span>'
        f'<span class="tool-workspace-badge">~30 sec preview</span>'
        f'<span class="tool-workspace-badge">Premium unlocks all 6</span>'
        f"</div></div>"
    )


def form_section_header(
    *,
    badge: str,
    badge_class: str,
    icon: str,
    title: str,
    subtitle: str,
) -> str:
    return (
        f'<div class="form-section-header">'
        f'<span class="form-section-badge {badge_class}">{html.escape(badge)}</span>'
        f'<p class="form-section-title"><span>{icon}</span> {html.escape(title)}</p>'
        f'<p class="form-section-subtitle">{html.escape(subtitle)}</p>'
        f"</div>"
    )
