"""Premium dark tool-form layout — Crow Metrics evaluation workspace."""

TOOL_FORM_CSS = """
/* ── Canvas ─────────────────────────────────────────────────────────────── */
.stApp:has(.cm-tool-form) {
    background: #000000 !important;
    color: #F5F5F7 !important;
}
.stApp:has(.cm-tool-form) .site-header__bar {
    background: rgba(0, 0, 0, 0.72) !important;
    border-bottom-color: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
}
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__brand,
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__link,
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__login,
.stApp:has(.cm-tool-form) .site-header__bar .crow-wordmark__crow {
    color: #F5F5F7 !important;
}
.stApp:has(.cm-tool-form) .site-header__bar .crow-wordmark__metrics {
    color: #86868B !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
.cm-tool-side-promo {
    border-radius: 20px;
    padding: 1.25rem 1.2rem;
    margin-bottom: 0.85rem;
    background: linear-gradient(160deg, rgba(43, 89, 255, 0.22) 0%, rgba(30, 58, 138, 0.12) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.cm-tool-side-promo-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-tool-side-promo-title {
    margin: 0 0 0.35rem;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    line-height: 1.25;
    color: #F5F5F7;
}
.cm-tool-side-promo-copy {
    margin: 0 0 0.75rem;
    font-size: 0.8125rem;
    line-height: 1.45;
    color: #86868B;
}
.cm-tool-side-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
}
.cm-tool-side-badge {
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 500;
    color: #D2D2D7;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-tool-checklist {
    border-radius: 18px;
    padding: 1rem 1.05rem 0.9rem;
    margin-bottom: 0.85rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-tool-checklist-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.65rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}
.cm-tool-checklist-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-tool-checklist-score {
    font-size: 0.75rem;
    font-weight: 600;
    color: #F5F5F7;
}
.cm-tool-check-row {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.32rem 0;
    font-size: 0.78rem;
    line-height: 1.4;
    color: #636366;
}
.cm-tool-check-row.is-done { color: #AEAEB2; }
.cm-tool-check-dot {
    flex-shrink: 0;
    width: 0.45rem;
    height: 0.45rem;
    margin-top: 0.38rem;
    border-radius: 999px;
    border: 1.5px solid rgba(134, 134, 139, 0.5);
}
.cm-tool-check-row.is-done .cm-tool-check-dot {
    border-color: #30D158;
    background: #30D158;
}
.cm-tool-check-quota {
    margin-top: 0.65rem;
    padding-top: 0.65rem;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    font-size: 0.75rem;
    color: #86868B;
}
.cm-tool-check-quota-dot { display: none; }
.cm-tool-score-guide {
    border-radius: 18px;
    padding: 0.9rem 1.05rem;
    margin-bottom: 0.85rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
}
.cm-tool-score-guide-title {
    margin: 0 0 0.5rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-tool-score-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.22rem 0;
    font-size: 0.75rem;
    color: #86868B;
}
.cm-tool-score-swatch {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 2px;
    flex-shrink: 0;
}
.cm-tool-privacy {
    font-size: 0.72rem;
    line-height: 1.45;
    color: #636366;
}

/* ── Main form ────────────────────────────────────────────────────────────── */
.cm-tool-main-head {
    margin-bottom: 2rem;
    padding-top: 0.25rem;
}
.cm-tool-main-title {
    margin: 0 0 0.4rem;
    font-size: clamp(1.75rem, 4vw, 2.25rem);
    font-weight: 600;
    letter-spacing: -0.035em;
    line-height: 1.1;
    color: #F5F5F7;
}
.cm-tool-main-lead {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
    color: #86868B;
    font-weight: 400;
}
.cm-tool-fields-label {
    margin: 0 0 0.55rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #636366;
}
.cm-tool-required-marker + p.cm-tool-fields-label {
    margin-top: 0;
}
.cm-tool-optional-marker {
    display: block;
    height: 1.5rem;
}
.cm-tool-compact-banner {
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-bottom: 1.25rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-tool-compact-banner strong {
    display: block;
    margin-bottom: 0.15rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #F5F5F7;
}
.cm-tool-compact-banner span {
    font-size: 0.8rem;
    color: #86868B;
}
.cm-tool-cta-marker {
    display: block;
    height: 2rem;
}
.cm-tool-cta-footnote {
    margin: 0.65rem 0 0;
    text-align: center;
    font-size: 0.75rem;
    color: #636366;
}

/* Required fields — single glass card */
.stApp:has(.cm-tool-form) div[class*="st-key-form_required_card"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 18px !important;
    box-shadow: none !important;
    padding: 1.15rem 1.2rem 0.85rem !important;
    margin-bottom: 0.25rem !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_required_card"] > div {
    gap: 1.1rem !important;
}

/* Hide default bordered chrome elsewhere */
.stApp:has(.cm-tool-form) div[data-testid="stVerticalBlockBorderWrapper"]:not([class*="st-key-form_required_card"]) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── Widgets ──────────────────────────────────────────────────────────────── */
.stApp:has(.cm-tool-form) [data-testid="stTextInput"],
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"],
.stApp:has(.cm-tool-form) [data-testid="stTextArea"],
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] {
    margin-bottom: 0 !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] label,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] label,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] label,
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] label,
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] [data-testid="stWidgetLabel"],
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] [data-testid="stWidgetLabel"] {
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em !important;
    color: #F5F5F7 !important;
    margin-bottom: 0.45rem !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] input,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea {
    background: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 12px !important;
    color: #F5F5F7 !important;
    min-height: 2.85rem;
    font-size: 0.9375rem !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, background 0.2s ease !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input::placeholder,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea::placeholder {
    color: #636366 !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input:focus,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] input:focus,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea:focus {
    background: rgba(255, 255, 255, 0.09) !important;
    border-color: rgba(43, 89, 255, 0.65) !important;
    box-shadow: 0 0 0 4px rgba(43, 89, 255, 0.15) !important;
    outline: none !important;
}
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] button {
    color: #86868B !important;
    background: transparent !important;
    border: none !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    margin-bottom: 0.5rem !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] details summary {
    font-size: 0.9375rem !important;
    font-weight: 500 !important;
    color: #F5F5F7 !important;
    padding: 0.9rem 1rem !important;
    background: transparent !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0.75rem 1rem 1rem !important;
}
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] section {
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 1px dashed rgba(255, 255, 255, 0.14) !important;
    background: rgba(255, 255, 255, 0.03) !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] {
    margin-top: 0.25rem !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"] {
    width: 100% !important;
    min-height: 3rem !important;
    border-radius: 980px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    color: #FFFFFF !important;
    background: #2B59FF !important;
    border: none !important;
    box-shadow: none !important;
    transition: background 0.2s ease, transform 0.2s ease !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]:hover:not(:disabled) {
    background: #1a4ae8 !important;
    transform: scale(1.01);
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]:disabled {
    opacity: 0.4 !important;
}
.stApp:has(.cm-tool-form) .metric-hint {
    margin: 0.35rem 0 0;
    font-size: 0.8rem;
    color: #86868B;
}
.stApp:has(.cm-tool-form) .metric-hint strong {
    color: #F5F5F7;
    font-weight: 600;
}

/* Vertical rhythm in main column */
.stApp:has(.cm-tool-form) [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}

/* Mobile — form before sidebar */
@media (max-width: 900px) {
    .cm-tool-form-layout-marker + [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    .cm-tool-form-layout-marker + [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
        order: 2;
    }
    .cm-tool-form-layout-marker + [data-testid="stHorizontalBlock"] > [data-testid="column"]:last-child {
        order: 1;
    }
    .cm-tool-main-head {
        margin-bottom: 1.5rem;
    }
}
"""
