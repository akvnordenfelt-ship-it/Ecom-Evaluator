"""Premium dark tool-form layout — Crow Metrics evaluation workspace."""

TOOL_FORM_CSS = """
/* ── Tool form canvas ───────────────────────────────────────────────────── */
.stApp:has(.cm-tool-form) {
    background:
        radial-gradient(ellipse 70% 45% at 10% -5%, rgba(43, 89, 255, 0.14) 0%, transparent 55%),
        radial-gradient(ellipse 55% 40% at 95% 0%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
        linear-gradient(180deg, #060B18 0%, #0A1128 38%, #0F172A 100%) !important;
    color: #E2E8F0 !important;
}
.stApp:has(.cm-tool-form) .site-header__bar {
    background: rgba(6, 11, 24, 0.82) !important;
    border-bottom-color: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__brand,
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__link,
.stApp:has(.cm-tool-form) .site-header__bar a.site-header__login,
.stApp:has(.cm-tool-form) .site-header__bar .crow-wordmark__crow {
    color: #F8FAFC !important;
}
.stApp:has(.cm-tool-form) .site-header__bar .crow-wordmark__metrics {
    color: #94A3B8 !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
.cm-tool-side-promo {
    border-radius: 18px;
    padding: 1.35rem 1.25rem 1.2rem;
    margin-bottom: 1rem;
    background: linear-gradient(145deg, rgba(67, 56, 202, 0.55) 0%, rgba(43, 89, 255, 0.35) 48%, rgba(6, 182, 212, 0.18) 100%);
    border: 1px solid rgba(147, 197, 253, 0.22);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
}
.cm-tool-side-promo-kicker {
    margin: 0 0 0.45rem;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #BFDBFE;
}
.cm-tool-side-promo-title {
    margin: 0 0 0.55rem;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.2;
    color: #FFFFFF;
}
.cm-tool-side-promo-copy {
    margin: 0 0 0.85rem;
    font-size: 0.8rem;
    line-height: 1.55;
    color: #CBD5E1;
}
.cm-tool-side-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.cm-tool-side-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.28rem 0.62rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #E2E8F0;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
}
.cm-tool-checklist {
    border-radius: 16px;
    padding: 1.1rem 1.1rem 1rem;
    margin-bottom: 1rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-tool-checklist-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-tool-checklist-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-tool-checklist-score {
    font-size: 0.82rem;
    font-weight: 700;
    color: #93C5FD;
    background: rgba(43, 89, 255, 0.14);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 999px;
    padding: 0.2rem 0.55rem;
}
.cm-tool-check-row {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.38rem 0;
    font-size: 0.8rem;
    line-height: 1.45;
    color: #64748B;
}
.cm-tool-check-row.is-done {
    color: #CBD5E1;
}
.cm-tool-check-dot {
    flex-shrink: 0;
    width: 0.55rem;
    height: 0.55rem;
    margin-top: 0.35rem;
    border-radius: 999px;
    border: 1.5px solid rgba(148, 163, 184, 0.45);
    background: transparent;
}
.cm-tool-check-row.is-done .cm-tool-check-dot {
    border-color: #34D399;
    background: #34D399;
    box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.15);
}
.cm-tool-check-quota {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.76rem;
    color: #94A3B8;
}
.cm-tool-check-quota-dot {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 999px;
    background: #2B59FF;
    box-shadow: 0 0 0 4px rgba(43, 89, 255, 0.2);
}
.cm-tool-score-guide {
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
}
.cm-tool-score-guide-title {
    margin: 0 0 0.65rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-tool-score-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.28rem 0;
    font-size: 0.76rem;
    color: #94A3B8;
}
.cm-tool-score-swatch {
    width: 0.55rem;
    height: 0.55rem;
    border-radius: 3px;
    flex-shrink: 0;
}
.cm-tool-privacy {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    padding: 0.85rem 0.95rem;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 0.74rem;
    line-height: 1.5;
    color: #64748B;
}
.cm-tool-privacy-icon {
    font-size: 0.95rem;
    line-height: 1;
    margin-top: 0.05rem;
}

/* ── Main form header ───────────────────────────────────────────────────── */
.cm-tool-main-head {
    margin-bottom: 1.5rem;
}
.cm-tool-main-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin: 0 0 0.55rem;
    font-size: clamp(1.35rem, 2.5vw, 1.65rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #FFFFFF;
}
.cm-tool-main-title-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 10px;
    background: rgba(43, 89, 255, 0.18);
    border: 1px solid rgba(96, 165, 250, 0.25);
    font-size: 1rem;
}
.cm-tool-main-lead {
    margin: 0;
    max-width: 38rem;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #94A3B8;
}
.cm-tool-hint {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    margin-top: 0.85rem;
    padding: 0.75rem 0.9rem;
    border-radius: 12px;
    background: rgba(43, 89, 255, 0.1);
    border: 1px solid rgba(96, 165, 250, 0.2);
    font-size: 0.8rem;
    line-height: 1.5;
    color: #BFDBFE;
}
.cm-tool-hint strong {
    color: #FFFFFF;
    font-weight: 600;
}

/* ── Section cards ──────────────────────────────────────────────────────── */
.cm-tool-section {
    margin-bottom: 1.15rem;
}
.cm-tool-section-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.cm-tool-section-title {
    margin: 0;
    font-size: 0.98rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.02em;
}
.cm-tool-section-sub {
    margin: 0.2rem 0 0;
    font-size: 0.78rem;
    line-height: 1.45;
    color: #64748B;
}
.cm-tool-pill {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.cm-tool-pill--required {
    color: #93C5FD;
    background: rgba(43, 89, 255, 0.14);
    border: 1px solid rgba(96, 165, 250, 0.28);
}
.cm-tool-pill--optional {
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.cm-tool-card {
    border-radius: 16px;
    padding: 1.1rem 1.15rem 1.05rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.09);
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.12);
}
.cm-tool-compact-banner {
    border-radius: 14px;
    padding: 0.95rem 1.1rem;
    margin-bottom: 1.15rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.cm-tool-compact-banner strong {
    display: block;
    margin-bottom: 0.2rem;
    font-size: 0.92rem;
    color: #F8FAFC;
}
.cm-tool-compact-banner span {
    font-size: 0.8rem;
    color: #94A3B8;
}

/* ── CTA footer ─────────────────────────────────────────────────────────── */
.cm-tool-cta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem 1.25rem;
    margin-top: 1.35rem;
    padding: 1.2rem 1.25rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(43, 89, 255, 0.16) 0%, rgba(15, 23, 42, 0.65) 100%);
    border: 1px solid rgba(96, 165, 250, 0.22);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.2);
}
.cm-tool-cta-copy {
    flex: 1 1 14rem;
    min-width: 0;
}
.cm-tool-cta-kicker {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin: 0 0 0.35rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #93C5FD;
}
.cm-tool-cta-title {
    margin: 0 0 0.25rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}
.cm-tool-cta-sub {
    margin: 0;
    font-size: 0.8rem;
    color: #94A3B8;
}
.cm-tool-cta-action {
    flex: 1 1 15rem;
    min-width: min(100%, 16rem);
}
.cm-tool-cta-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem 1rem;
    margin-top: 0.55rem;
    font-size: 0.7rem;
    color: #64748B;
}
.cm-tool-cta-meta span::before {
    content: "·";
    margin-right: 0.65rem;
    color: rgba(148, 163, 184, 0.45);
}
.cm-tool-cta-meta span:first-child::before {
    content: none;
    margin: 0;
}

/* ── Streamlit widget overrides (tool form only) ─────────────────────────── */
.stApp:has(.cm-tool-form) div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] label,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] label,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] label,
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] label,
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] [data-testid="stWidgetLabel"],
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] [data-testid="stWidgetLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    color: #94A3B8 !important;
    margin-bottom: 0.4rem !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] input,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
    min-height: 2.75rem;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input::placeholder,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea::placeholder {
    color: #64748B !important;
}
.stApp:has(.cm-tool-form) [data-testid="stTextInput"] input:focus,
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] input:focus,
.stApp:has(.cm-tool-form) [data-testid="stTextArea"] textarea:focus {
    border-color: rgba(96, 165, 250, 0.55) !important;
    box-shadow: 0 0 0 3px rgba(43, 89, 255, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.04) !important;
    outline: none !important;
}
.stApp:has(.cm-tool-form) [data-testid="stNumberInput"] button {
    color: #94A3B8 !important;
    background: rgba(255, 255, 255, 0.06) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.09) !important;
    border-radius: 14px !important;
    margin-bottom: 0.85rem !important;
    overflow: hidden;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] details summary {
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    padding: 0.85rem 1rem !important;
    background: transparent !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}
.stApp:has(.cm-tool-form) [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0.85rem 1rem 1rem !important;
}
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] section {
    padding: 1.1rem !important;
    border-radius: 12px !important;
    border: 1px dashed rgba(148, 163, 184, 0.35) !important;
    background: rgba(255, 255, 255, 0.02) !important;
}
.stApp:has(.cm-tool-form) [data-testid="stFileUploader"] section * {
    color: #94A3B8 !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"] {
    width: 100% !important;
    min-height: 2.9rem !important;
    border-radius: 14px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #2B59FF 0%, #1E40AF 100%) !important;
    border: 1px solid rgba(147, 197, 253, 0.35) !important;
    box-shadow: 0 8px 24px rgba(43, 89, 255, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
}
.stApp:has(.cm-tool-form) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"]:hover:not(:disabled) {
    filter: brightness(1.06);
    transform: translateY(-1px);
}
.stApp:has(.cm-tool-form) [data-testid="stAlert"] {
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
}
.stApp:has(.cm-tool-form) .metric-hint {
    margin: 0.5rem 0 0.25rem;
    padding: 0.55rem 0.7rem;
    border-radius: 10px;
    font-size: 0.78rem;
    color: #94A3B8;
    background: rgba(43, 89, 255, 0.1);
    border: 1px solid rgba(96, 165, 250, 0.18);
}
.stApp:has(.cm-tool-form) .metric-hint strong {
    color: #E2E8F0;
}
.stApp:has(.cm-tool-form) .form-field-hint {
    margin: 0.35rem 0 0;
    font-size: 0.74rem;
    line-height: 1.5;
    color: #64748B;
}

/* Layout marker — form first on mobile */
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
    .cm-tool-cta {
        flex-direction: column;
        align-items: stretch;
    }
    .cm-tool-side-promo-title {
        font-size: 1.05rem;
    }
}
"""
