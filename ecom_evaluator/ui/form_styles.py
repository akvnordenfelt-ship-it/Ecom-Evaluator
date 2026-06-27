"""Premium workspace layout — form + evaluation report themes."""

TOOL_FORM_CSS = """
/* ── Theme tokens ─────────────────────────────────────────────────────────── */
.stApp:has(.cm-workspace-mode-dark),
.stApp:has(.cm-workspace-mode-original),
.stApp:has(.cm-workspace-mode-black) {
    --ws-app-bg:
        radial-gradient(ellipse 70% 45% at 10% -5%, rgba(43, 89, 255, 0.16) 0%, transparent 55%),
        radial-gradient(ellipse 55% 40% at 95% 0%, rgba(30, 58, 138, 0.14) 0%, transparent 50%),
        linear-gradient(180deg, #060B18 0%, #0A1128 42%, #0F172A 100%);
    --ws-text: #F5F5F7;
    --ws-text-muted: #86868B;
    --ws-text-faint: #636366;
    --ws-nav-bg: rgba(6, 11, 24, 0.82);
    --ws-nav-border: rgba(255, 255, 255, 0.08);
    --ws-nav-brand: #F5F5F7;
    --ws-nav-muted: #94A3B8;
    --ws-promo-bg: linear-gradient(160deg, rgba(43, 89, 255, 0.28) 0%, rgba(30, 58, 138, 0.16) 100%);
    --ws-promo-border: rgba(147, 197, 253, 0.22);
    --ws-surface: rgba(255, 255, 255, 0.04);
    --ws-surface-border: rgba(255, 255, 255, 0.08);
    --ws-card-bg: rgba(19, 29, 50, 0.92);
    --ws-card-border: rgba(147, 197, 253, 0.22);
    --ws-input-bg: #131D32;
    --ws-input-text: #F5F5F7;
    --ws-input-border: rgba(147, 197, 253, 0.28);
    --ws-input-focus: #5B8CFF;
    --ws-input-focus-ring: rgba(91, 140, 255, 0.22);
    --ws-divider: rgba(255, 255, 255, 0.08);
    --ws-tab-bg: rgba(255, 255, 255, 0.05);
    --ws-tab-text: #AEAEB2;
    --ws-tab-active: #F5F5F7;
    --ws-segment-track-bg: rgba(255, 255, 255, 0.06);
    --ws-segment-track-border: rgba(255, 255, 255, 0.1);
    --ws-segment-idle-text: #AEAEB2;
    --ws-segment-active-text: #F5F5F7;
    --ws-segment-active-bg: rgba(255, 255, 255, 0.1);
    --ws-segment-active-border: rgba(147, 197, 253, 0.35);
    --ws-status-bg: rgba(52, 211, 153, 0.12);
    --ws-status-border: rgba(52, 211, 153, 0.28);
    --ws-status-text: #6EE7B7;
    --ws-report-meta: #86868B;
    --ws-section-heading: #F5F5F7;
    --ws-stat-bg: rgba(255, 255, 255, 0.04);
    --ws-stat-border: rgba(255, 255, 255, 0.08);
    --ws-stat-text: #CBD5E1;
    --ws-locked-bg: rgba(255, 255, 255, 0.03);
    --ws-locked-border: rgba(255, 255, 255, 0.08);
}

.stApp:has(.cm-workspace-mode-bright),
.stApp:has(.cm-workspace-mode-white) {
    --ws-app-bg: #F5F5FA;
    --ws-text: #1D1D1F;
    --ws-text-muted: #48484A;
    --ws-text-faint: #636366;
    --ws-nav-bg: rgba(255, 255, 255, 0.92);
    --ws-nav-border: rgba(0, 0, 0, 0.1);
    --ws-nav-brand: #1D1D1F;
    --ws-nav-muted: #48484A;
    --ws-promo-bg: linear-gradient(160deg, #EFF6FF 0%, #F8FAFC 100%);
    --ws-promo-border: #93C5FD;
    --ws-surface: #FFFFFF;
    --ws-surface-border: #C7C7CC;
    --ws-card-bg: #FFFFFF;
    --ws-card-border: #C7C7CC;
    --ws-input-bg: #FFFFFF;
    --ws-input-text: #1D1D1F;
    --ws-input-border: #AEAEB2;
    --ws-input-focus: #2B59FF;
    --ws-input-focus-ring: rgba(43, 89, 255, 0.18);
    --ws-divider: #D1D1D6;
    --ws-tab-bg: #FFFFFF;
    --ws-tab-text: #48484A;
    --ws-tab-active: #1D1D1F;
    --ws-segment-track-bg: #E8E8ED;
    --ws-segment-track-border: #C7C7CC;
    --ws-segment-idle-text: #3A3A3C;
    --ws-segment-active-text: #1D1D1F;
    --ws-segment-active-bg: #FFFFFF;
    --ws-segment-active-border: #AEAEB2;
    --ws-status-bg: #ECFDF5;
    --ws-status-border: #6EE7B7;
    --ws-status-text: #065F46;
    --ws-report-meta: #48484A;
    --ws-section-heading: #1D1D1F;
    --ws-stat-bg: #FFFFFF;
    --ws-stat-border: #C7C7CC;
    --ws-stat-text: #334155;
    --ws-locked-bg: #F8FAFC;
    --ws-locked-border: #CBD5E1;
}

/* ── Canvas + nav ─────────────────────────────────────────────────────────── */
.stApp:has(.cm-workspace) {
    background: var(--ws-app-bg) !important;
    color: var(--ws-text) !important;
    overscroll-behavior-y: none;
}
html:has(.cm-workspace) {
    scroll-padding-top: 0 !important;
    overscroll-behavior-y: none;
}
.stApp:has(.cm-workspace) [data-testid="stAppViewContainer"],
.stApp:has(.cm-workspace) section[data-testid="stMain"],
.stApp:has(.cm-workspace) .stMainBlockContainer,
.stApp:has(.cm-workspace) [data-testid="stMainBlockContainer"],
.stApp:has(.cm-workspace) .block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
.stApp:has(.cm-workspace) section[data-testid="stMain"] {
    overscroll-behavior-y: none;
}
.form-workspace-marker,
.cm-tool-form-layout-marker {
    display: block;
    height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    border: none !important;
    pointer-events: none !important;
}
.stApp:has(.cm-workspace) [data-testid="stMarkdownContainer"]:has(.form-workspace-marker),
.stApp:has(.cm-workspace) [data-testid="stMarkdownContainer"]:has(.cm-tool-form-layout-marker) {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}
.stApp:has(.cm-workspace) section[data-testid="stMain"] > div {
    padding-top: 0 !important;
}
.stApp:has(.cm-workspace) [data-testid="stMarkdownContainer"]:has(.site-header),
.stApp:has(.cm-workspace) [data-testid="stMarkdownContainer"]:has(.site-header__spacer) {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}
.stApp:has(.cm-workspace) .site-header__spacer {
    height: var(--ps-nav-h, 76px) !important;
    margin: 0 !important;
    padding: 0 !important;
}
.stApp:has(.cm-workspace) .block-container > div > [data-testid="stVerticalBlock"] {
    gap: 0.35rem !important;
}
.stApp:has(.cm-workspace) [data-testid="element-container"]:has(div[class*="st-key-ps_nav_"]),
.stApp:has(.cm-workspace) [data-testid="element-container"]:has(div[class*="st-key-ps_sample_"]) {
    position: fixed !important;
    left: -10000px !important;
    top: 0 !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    visibility: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    z-index: -1 !important;
    border: none !important;
}
.stApp:has(.cm-workspace) [data-testid="element-container"]:has(iframe) {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    line-height: 0 !important;
    border: none !important;
}
.stApp:has(.cm-workspace) .cm-tool-form-layout-marker + [data-testid="stHorizontalBlock"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}
.stApp:has(.cm-workspace) .cm-tool-main-head {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
}
.stApp:has(.cm-workspace) .site-header__bar {
    background: var(--ws-nav-bg) !important;
    border-bottom-color: var(--ws-nav-border) !important;
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
}
.stApp:has(.cm-workspace) .site-header__bar a.site-header__brand,
.stApp:has(.cm-workspace) .site-header__bar a.site-header__link,
.stApp:has(.cm-workspace) .site-header__bar a.site-header__login,
.stApp:has(.cm-workspace) .site-header__bar .crow-wordmark__crow {
    color: var(--ws-nav-brand) !important;
}
.stApp:has(.cm-workspace) .site-header__bar .crow-wordmark__metrics {
    color: var(--ws-nav-muted) !important;
}

/* Theme switcher — compact pill strip (CSS only, no JS) */
.stApp:has(.cm-workspace) div[class*="st-key-workspace_theme_strip"] {
    display: flex;
    justify-content: flex-end;
    margin: 0 0 0.65rem !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-workspace_theme_strip"] [data-testid="stHorizontalBlock"] {
    gap: 0.2rem !important;
    max-width: 9.75rem;
    width: 9.75rem;
    margin-left: auto !important;
    margin-right: 0 !important;
    margin-bottom: 0 !important;
    background: var(--ws-segment-track-bg) !important;
    border: 1px solid var(--ws-segment-track-border) !important;
    border-radius: 999px !important;
    padding: 0.15rem !important;
    box-shadow: none !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-workspace_theme_strip"] [data-testid="column"] {
    min-width: 0 !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-ws_theme_pick_"] button[data-testid^="stBaseButton-"] {
    min-height: 1.75rem !important;
    height: 1.75rem !important;
    padding: 0.1rem 0.35rem !important;
    border-radius: 999px !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.2 !important;
    box-shadow: none !important;
    filter: none !important;
}
.stApp:has(.cm-workspace-mode-dark) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"],
.stApp:has(.cm-workspace-mode-original) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"],
.stApp:has(.cm-workspace-mode-black) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    background-color: transparent !important;
    background-image: none !important;
    color: var(--ws-segment-idle-text) !important;
    -webkit-text-fill-color: var(--ws-segment-idle-text) !important;
    border: 1px solid transparent !important;
}
.stApp:has(.cm-workspace-mode-bright) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"],
.stApp:has(.cm-workspace-mode-white) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    background-color: transparent !important;
    color: var(--ws-segment-idle-text) !important;
    -webkit-text-fill-color: var(--ws-segment-idle-text) !important;
    border: 1px solid transparent !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"] div,
.stApp:has(.cm-workspace) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-secondary"] span,
.stApp:has(.cm-workspace) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"] div,
.stApp:has(.cm-workspace) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"] span {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}
.stApp:has(.cm-workspace-mode-dark) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"],
.stApp:has(.cm-workspace-mode-original) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"],
.stApp:has(.cm-workspace-mode-black) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"] {
    background: var(--ws-segment-active-bg) !important;
    background-color: var(--ws-segment-active-bg) !important;
    background-image: none !important;
    color: var(--ws-segment-active-text) !important;
    -webkit-text-fill-color: var(--ws-segment-active-text) !important;
    border: 1px solid var(--ws-segment-active-border) !important;
}
.stApp:has(.cm-workspace-mode-bright) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"],
.stApp:has(.cm-workspace-mode-white) div[class*="st-key-ws_theme_pick_"] button[data-testid="stBaseButton-primary"] {
    background: var(--ws-segment-active-bg) !important;
    background-color: var(--ws-segment-active-bg) !important;
    background-image: none !important;
    color: var(--ws-segment-active-text) !important;
    -webkit-text-fill-color: var(--ws-segment-active-text) !important;
    border: 1px solid var(--ws-segment-active-border) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06) !important;
}

/* Tabs (report / inputs) */
.stApp:has(.cm-workspace) .stTabs [data-baseweb="tab-list"] {
    background: var(--ws-surface) !important;
    border-bottom-color: var(--ws-divider) !important;
    border-radius: 12px 12px 0 0 !important;
    gap: 0.25rem !important;
    padding: 0.35rem 0.35rem 0 !important;
}
.stApp:has(.cm-workspace) .stTabs [data-baseweb="tab"] {
    color: var(--ws-tab-text) !important;
    background: transparent !important;
}
.stApp:has(.cm-workspace) .stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--ws-tab-active) !important;
    background: var(--ws-card-bg) !important;
    border-radius: 10px 10px 0 0 !important;
}
.stApp:has(.cm-workspace) hr {
    border-color: var(--ws-divider) !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
.cm-tool-side-promo {
    border-radius: 20px;
    padding: 1.25rem 1.2rem;
    margin-bottom: 0.85rem;
    background: var(--ws-promo-bg);
    border: 1px solid var(--ws-promo-border);
}
.cm-tool-side-promo-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ws-text-muted);
}
.cm-tool-side-promo-title {
    margin: 0 0 0.35rem;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    line-height: 1.25;
    color: var(--ws-text);
}
.cm-tool-side-promo-copy {
    margin: 0 0 0.75rem;
    font-size: 0.8125rem;
    line-height: 1.45;
    color: var(--ws-text-muted);
}
.cm-tool-side-badges { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.cm-tool-side-badge {
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 500;
    color: var(--ws-text-muted);
    background: var(--ws-surface);
    border: 1px solid var(--ws-surface-border);
}
.cm-tool-checklist,
.cm-tool-score-guide {
    border-radius: 18px;
    padding: 1rem 1.05rem 0.9rem;
    margin-bottom: 0.85rem;
    background: var(--ws-surface);
    border: 1px solid var(--ws-surface-border);
}
.cm-tool-checklist-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.65rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--ws-divider);
}
.cm-tool-checklist-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ws-text-muted);
}
.cm-tool-checklist-score {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--ws-text);
}
.cm-tool-check-row {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.32rem 0;
    font-size: 0.78rem;
    line-height: 1.4;
    color: var(--ws-text-faint);
}
.cm-tool-check-row.is-done { color: var(--ws-text-muted); }
.cm-tool-check-dot {
    flex-shrink: 0;
    width: 0.45rem;
    height: 0.45rem;
    margin-top: 0.38rem;
    border-radius: 999px;
    border: 1.5px solid var(--ws-text-faint);
}
.cm-tool-check-row.is-done .cm-tool-check-dot {
    border-color: #30D158;
    background: #30D158;
}
.cm-tool-check-quota {
    margin-top: 0.65rem;
    padding-top: 0.65rem;
    border-top: 1px solid var(--ws-divider);
    font-size: 0.75rem;
    color: var(--ws-text-muted);
}
.cm-tool-score-guide-title {
    margin: 0 0 0.5rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ws-text-muted);
}
.cm-tool-score-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.22rem 0;
    font-size: 0.75rem;
    color: var(--ws-text-muted);
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
    color: var(--ws-text-faint);
}

/* ── Main form ────────────────────────────────────────────────────────────── */
.cm-tool-main-head {
    margin-bottom: 2rem;
    padding-top: 0;
}
.cm-tool-main-title {
    margin: 0 0 0.4rem;
    font-size: clamp(1.75rem, 4vw, 2.25rem);
    font-weight: 600;
    letter-spacing: -0.035em;
    line-height: 1.1;
    color: var(--ws-text);
}
.cm-tool-main-lead {
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
    color: var(--ws-text-muted);
}
.cm-tool-fields-label {
    margin: 0 0 0.55rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ws-text-faint);
}
.cm-tool-optional-marker { display: block; height: 1.5rem; }
.cm-tool-compact-banner {
    border-radius: 16px;
    padding: 0.9rem 1rem;
    margin-bottom: 1.25rem;
    background: var(--ws-surface);
    border: 1px solid var(--ws-surface-border);
}
.cm-tool-compact-banner strong {
    display: block;
    margin-bottom: 0.15rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--ws-text);
}
.cm-tool-compact-banner span {
    font-size: 0.8rem;
    color: var(--ws-text-muted);
}
.cm-tool-cta-marker { display: block; height: 2rem; }
.cm-tool-cta-footnote {
    margin: 0.65rem 0 0;
    text-align: center;
    font-size: 0.75rem;
    color: var(--ws-text-faint);
}

.stApp:has(.cm-workspace) div[class*="st-key-form_required_card"] {
    background: var(--ws-card-bg) !important;
    border: 1px solid var(--ws-card-border) !important;
    border-radius: 18px !important;
    box-shadow: none !important;
    padding: 1.15rem 1.2rem 0.85rem !important;
    margin-bottom: 0.25rem !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_required_card"] > div {
    gap: 1.1rem !important;
}
.stApp:has(.cm-workspace) div[data-testid="stVerticalBlockBorderWrapper"]:not([class*="st-key-form_required_card"]) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Widgets */
.stApp:has(.cm-workspace) [data-testid="stTextInput"] label,
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] label,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] label,
.stApp:has(.cm-workspace) [data-testid="stFileUploader"] label,
.stApp:has(.cm-workspace) [data-testid="stTextInput"] [data-testid="stWidgetLabel"],
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] [data-testid="stWidgetLabel"] {
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    color: var(--ws-text) !important;
    margin-bottom: 0.45rem !important;
}
.stApp:has(.cm-workspace) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] textarea {
    background-color: var(--ws-input-bg) !important;
    background: var(--ws-input-bg) !important;
    border: 1px solid var(--ws-input-border) !important;
    border-radius: 12px !important;
    color: var(--ws-input-text, var(--ws-text)) !important;
    -webkit-text-fill-color: var(--ws-input-text, var(--ws-text)) !important;
    caret-color: var(--ws-input-text, var(--ws-text)) !important;
    min-height: 2.85rem;
    font-size: 0.9375rem !important;
    box-shadow: none !important;
}
.stApp:has(.cm-workspace) [data-testid="stTextInput"] > div,
.stApp:has(.cm-workspace) [data-testid="stTextInput"] > div > div,
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] > div,
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] > div > div,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] > div,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] > div > div,
.stApp:has(.cm-workspace) [data-testid="stTextInput"] [data-baseweb="input"],
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] [data-baseweb="input"],
.stApp:has(.cm-workspace) [data-testid="stTextArea"] [data-baseweb="textarea"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.stApp:has(.cm-workspace-mode-dark) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace-mode-dark) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace-mode-dark) [data-testid="stTextArea"] textarea,
.stApp:has(.cm-workspace-mode-original) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace-mode-original) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace-mode-original) [data-testid="stTextArea"] textarea,
.stApp:has(.cm-workspace-mode-black) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace-mode-black) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace-mode-black) [data-testid="stTextArea"] textarea {
    background-color: #131D32 !important;
    background: #131D32 !important;
    color: #F5F5F7 !important;
    -webkit-text-fill-color: #F5F5F7 !important;
    caret-color: #F5F5F7 !important;
    border-color: rgba(147, 197, 253, 0.28) !important;
}
.stApp:has(.cm-workspace-mode-dark) [data-testid="stTextInput"] input:-webkit-autofill,
.stApp:has(.cm-workspace-mode-dark) [data-testid="stNumberInput"] input:-webkit-autofill,
.stApp:has(.cm-workspace-mode-original) [data-testid="stTextInput"] input:-webkit-autofill,
.stApp:has(.cm-workspace-mode-original) [data-testid="stNumberInput"] input:-webkit-autofill {
    -webkit-box-shadow: 0 0 0 1000px #131D32 inset !important;
    -webkit-text-fill-color: #F5F5F7 !important;
    caret-color: #F5F5F7 !important;
}
.stApp:has(.cm-workspace-mode-bright) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace-mode-bright) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace-mode-bright) [data-testid="stTextArea"] textarea,
.stApp:has(.cm-workspace-mode-white) [data-testid="stTextInput"] input,
.stApp:has(.cm-workspace-mode-white) [data-testid="stNumberInput"] input,
.stApp:has(.cm-workspace-mode-white) [data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #1D1D1F !important;
    -webkit-text-fill-color: #1D1D1F !important;
    caret-color: #1D1D1F !important;
    border-color: #AEAEB2 !important;
}
.stApp:has(.cm-workspace) [data-testid="stTextInput"] input::placeholder,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] textarea::placeholder {
    color: var(--ws-text-faint) !important;
}
.stApp:has(.cm-workspace) [data-testid="stTextInput"] input:focus,
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] input:focus,
.stApp:has(.cm-workspace) [data-testid="stTextArea"] textarea:focus {
    border-color: var(--ws-input-focus) !important;
    box-shadow: 0 0 0 4px var(--ws-input-focus-ring) !important;
    outline: none !important;
}
.stApp:has(.cm-workspace) [data-testid="stNumberInput"] button {
    color: var(--ws-text-muted) !important;
    background: transparent !important;
    border: none !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] {
    background: var(--ws-surface) !important;
    border: 1px solid var(--ws-surface-border) !important;
    border-radius: 14px !important;
    margin-bottom: 0.5rem !important;
    overflow: hidden;
    contain: layout style;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0.75rem 1rem 1rem !important;
    overflow: hidden;
    max-width: 100%;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    gap: 0.65rem !important;
    width: 100% !important;
    max-width: 100% !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="column"] {
    width: 100% !important;
    min-width: 0 !important;
    flex: 1 1 auto !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stNumberInput"],
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stTextInput"],
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stTextArea"] {
    max-width: 100% !important;
    width: 100% !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] [data-testid="stNumberInput"] > div {
    max-width: 100% !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] details summary {
    font-size: 0.9375rem !important;
    font-weight: 500 !important;
    color: var(--ws-text) !important;
    padding: 0.9rem 1rem !important;
    background: transparent !important;
}
.stApp:has(.cm-workspace) [data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px solid var(--ws-divider) !important;
}
.stApp:has(.cm-workspace) [data-testid="stFileUploader"] section {
    padding: 1rem !important;
    border-radius: 12px !important;
    border: 1px dashed var(--ws-input-border) !important;
    background: var(--ws-input-bg) !important;
}
.stApp:has(.cm-workspace) div[class*="st-key-form_run_analysis"] .stButton > button[kind="primary"] {
    width: 100% !important;
    min-height: 3rem !important;
    border-radius: 980px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    background: #2B59FF !important;
    border: none !important;
    box-shadow: none !important;
}
.stApp:has(.cm-workspace) .metric-hint {
    margin: 0.35rem 0 0;
    font-size: 0.8rem;
    color: var(--ws-text-muted);
}
.stApp:has(.cm-workspace) .metric-hint strong {
    color: var(--ws-text);
    font-weight: 600;
}

/* ── Evaluation report ──────────────────────────────────────────────────── */
.stApp:has(.cm-workspace) .status-banner--success {
    background: var(--ws-status-bg) !important;
    border: 1px solid var(--ws-status-border) !important;
    color: var(--ws-status-text) !important;
}
.stApp:has(.cm-workspace) .report-meta {
    color: var(--ws-report-meta) !important;
}
.stApp:has(.cm-workspace) .report-meta strong {
    color: var(--ws-text) !important;
}
.stApp:has(.cm-workspace) .section-eyebrow {
    color: var(--ws-text-muted) !important;
}
.stApp:has(.cm-workspace) h1,
.stApp:has(.cm-workspace) h2,
.stApp:has(.cm-workspace) h3,
.stApp:has(.cm-workspace) .form-card-title,
.stApp:has(.cm-workspace) .verdict-headline {
    color: var(--ws-section-heading) !important;
}
.stApp:has(.cm-workspace) .stat-tile,
.stApp:has(.cm-workspace) .stat-tile-body {
    background: var(--ws-stat-bg) !important;
    border-color: var(--ws-stat-border) !important;
    color: var(--ws-stat-text) !important;
}
.stApp:has(.cm-workspace) .stat-tile-value,
.stApp:has(.cm-workspace) .stat-tile-label {
    color: var(--ws-text) !important;
}
.stApp:has(.cm-workspace) .locked-section,
.stApp:has(.cm-workspace) .report-tier-banner {
    background: var(--ws-locked-bg) !important;
    border-color: var(--ws-locked-border) !important;
}
.stApp:has(.cm-workspace-mode-bright) .verdict-banner-label,
.stApp:has(.cm-workspace-mode-bright) .verdict-banner-subtitle,
.stApp:has(.cm-workspace-mode-bright) .verdict-banner-context {
    color: inherit;
}
.stApp:has(.cm-workspace-mode-dark) .verdict-banner {
    opacity: 0.98;
}
.stApp:has(.cm-workspace-mode-bright) [data-testid="stAlert"],
.stApp:has(.cm-workspace-mode-bright) [data-testid="stNotification"] {
    border: 1px solid #C7C7CC !important;
}
.stApp:has(.cm-workspace-mode-bright) .cm-tool-check-dot {
    border-color: #8E8E93 !important;
}
.stApp:has(.cm-workspace-mode-bright) .cm-tool-side-badge {
    background: #F2F2F7 !important;
    border-color: #C7C7CC !important;
    color: #3A3A3C !important;
}
.stApp:has(.cm-workspace) [data-testid="stCaption"] {
    color: var(--ws-text-muted) !important;
}

@media (max-width: 900px) {
    .cm-tool-main-head { margin-bottom: 1.5rem; }
    .stApp:has(.cm-workspace) div[class*="st-key-workspace_theme_strip"] [data-testid="stHorizontalBlock"] {
        max-width: 100%;
        width: 100%;
    }
}
"""
