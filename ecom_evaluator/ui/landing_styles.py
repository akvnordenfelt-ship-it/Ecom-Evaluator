"""Crow Metrics landing page v2 — professional SaaS marketing styles."""

LANDING_V2_CSS = """
:root {
    --cm-navy: #0A1128;
    --cm-navy-soft: #111827;
    --cm-blue: #0052FF;
    --cm-blue-bright: #2B59FF;
    --cm-cyan: #06B6D4;
    --cm-green: #22C55E;
    --cm-green-soft: #DCFCE7;
    --cm-yellow: #FACC15;
    --cm-orange: #F97316;
    --cm-red: #EF4444;
    --cm-surface: #F8FAFC;
    --cm-border: #E2E8F0;
    --cm-muted: #64748B;
    --cm-radius: 16px;
    --cm-shadow: 0 4px 6px rgba(15, 23, 42, 0.04), 0 24px 48px rgba(15, 23, 42, 0.08);
    --cm-shadow-lg: 0 8px 16px rgba(15, 23, 42, 0.06), 0 32px 64px rgba(15, 23, 42, 0.12);
}

.cm-page {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 1.5rem;
}
.cm-section {
    padding: 4.5rem 0;
    position: relative;
}
.cm-section--tight { padding: 3rem 0; }
.cm-section--dark {
    background: linear-gradient(180deg, #0A1128 0%, #111827 100%);
    color: #F8FAFC;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding-left: max(1.5rem, calc(50vw - 590px));
    padding-right: max(1.5rem, calc(50vw - 590px));
}
.cm-section-head {
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2.5rem;
}
.cm-section-head--left { text-align: left; margin-left: 0; }
.cm-kicker {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    margin: 0 0 0.85rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--cm-blue);
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
}
.cm-kicker--dark {
    color: #93C5FD;
    background: rgba(255,255,255,0.06);
    border-color: rgba(255,255,255,0.12);
}
.cm-title {
    font-size: clamp(1.85rem, 3.5vw, 2.65rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 0.85rem;
    color: var(--cm-navy);
}
.cm-section--dark .cm-title { color: #FFFFFF; }
.cm-title em, .cm-title .cm-accent {
    font-style: normal;
    color: var(--cm-blue-bright);
}
.cm-title--hero {
    font-size: clamp(2.1rem, 4.5vw, 3rem);
    line-height: 1.06;
}
.cm-lead {
    font-size: 1.05rem;
    line-height: 1.65;
    color: var(--cm-muted);
    margin: 0;
}
.cm-section--dark .cm-lead { color: #94A3B8; }

/* Shared CTA */
.cm-cta, a.cm-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    padding: 0.85rem 1.5rem;
    border-radius: 14px;
    font-size: 0.98rem;
    font-weight: 600;
    color: #FFFFFF !important;
    text-decoration: none !important;
    background: linear-gradient(135deg, var(--cm-blue-bright) 0%, var(--cm-blue) 100%);
    border: 1px solid rgba(0, 82, 255, 0.15);
    box-shadow: 0 1px 2px rgba(0, 82, 255, 0.15), 0 12px 32px rgba(0, 82, 255, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}
.cm-cta:hover, a.cm-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 82, 255, 0.2), 0 16px 40px rgba(0, 82, 255, 0.3);
    text-decoration: none !important;
}
.cm-cta--lg { padding: 1rem 1.75rem; font-size: 1.02rem; min-width: min(100%, 16rem); }
.cm-cta-host,
div[class*="st-key-landing_hero_cta"] {
    position: fixed !important;
    left: -10000px !important;
    top: 0 !important;
    width: 1px !important;
    height: 1px !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: -1 !important;
}
.cm-cta-host [data-testid="stButton"],
.cm-cta-host [data-testid="stButton"] button {
    display: none !important;
}

/* Hero */
.cm-hero {
    padding: 0.35rem 0 0;
    overflow: hidden;
}
.cm-hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 2.5rem;
    align-items: center;
}
.cm-hero-copy { max-width: 34rem; }
.cm-hero-bullets {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
    margin: 1.35rem 0 1.5rem;
    padding: 0;
    list-style: none;
}
.cm-hero-bullets li {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.92rem;
    font-weight: 500;
    color: #334155;
}
.cm-hero-bullets span { font-size: 1rem; }
.cm-hero-social {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.65rem;
    margin-top: 1.25rem;
}
.cm-avatars { display: inline-flex; }
.cm-avatar {
    width: 2rem;
    height: 2rem;
    margin-left: -0.5rem;
    border-radius: 999px;
    border: 2px solid #FFFFFF;
    object-fit: cover;
    background: #E2E8F0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.12);
    flex-shrink: 0;
}
.cm-avatar:first-child { margin-left: 0; }
.cm-stars { color: #FBBF24; font-size: 0.85rem; letter-spacing: 0.05em; }
.cm-social-text { font-size: 0.84rem; color: var(--cm-muted); font-weight: 500; }

.cm-hero-card-wrap {
    position: relative;
    animation: cm-float 6s ease-in-out infinite;
}
@keyframes cm-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Hero evaluation preview card */
.cm-eval-wrap {
    position: relative;
    animation: cm-float 6s ease-in-out infinite;
    perspective: 1200px;
}
.cm-eval-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 1.15rem 1.15rem 1rem;
    box-shadow:
        0 1px 2px rgba(15, 23, 42, 0.04),
        0 16px 40px rgba(15, 23, 42, 0.08),
        0 0 0 1px rgba(255, 255, 255, 0.6) inset;
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease;
}
.cm-eval-card:hover {
    transform: translateY(-6px) rotateX(1deg);
    box-shadow:
        0 4px 8px rgba(15, 23, 42, 0.06),
        0 28px 56px rgba(15, 23, 42, 0.12);
}
.cm-eval-card.is-pressed {
    transform: translateY(-2px) scale(0.995);
}
.cm-eval-head {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    margin-bottom: 0.95rem;
    text-decoration: none !important;
    color: inherit;
    border-radius: 14px;
    padding: 0.15rem;
    margin-left: -0.15rem;
    margin-right: -0.15rem;
    transition: background 0.2s ease;
}
.cm-eval-head:hover {
    background: #F8FAFC;
}
.cm-eval-thumb {
    width: 5.25rem;
    height: 5.25rem;
    border-radius: 14px;
    object-fit: cover;
    background: #F8FAFC;
    flex-shrink: 0;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.1);
    transition: transform 0.25s ease;
}
.cm-eval-head:hover .cm-eval-thumb { transform: scale(1.04); }
.cm-eval-meta { flex: 1; min-width: 0; }
.cm-eval-name {
    margin: 0 0 0.5rem;
    font-size: 0.94rem;
    font-weight: 700;
    line-height: 1.35;
    color: #0F172A;
}
.cm-eval-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.cm-eval-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.24rem 0.58rem;
    border-radius: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    line-height: 1;
}
.cm-eval-badge--score {
    color: #047857;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
}
.cm-eval-badge--trend {
    color: #1E40AF;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    font-weight: 600;
}
.cm-eval-financials {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 0.85rem;
    align-items: stretch;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #EEF2F6;
}
.cm-eval-fin-divider {
    width: 1px;
    background: #E2E8F0;
    align-self: stretch;
}
.cm-eval-fin-label {
    display: block;
    margin-bottom: 0.2rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-eval-fin-value {
    font-size: 1.08rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
}
.cm-eval-fin-value--green { color: #059669; }
.cm-eval-score-panel {
    padding: 0.95rem 1rem;
    margin-bottom: 1rem;
    border-radius: 14px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
}
.cm-eval-score-kicker {
    margin: 0 0 0.75rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-eval-score-row {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1rem;
    align-items: center;
}
.cm-eval-ring {
    position: relative;
    width: 5.25rem;
    height: 5.25rem;
    flex-shrink: 0;
}
.cm-eval-ring-svg {
    width: 100%;
    height: 100%;
    transform: rotate(-90deg);
}
.cm-eval-ring-track {
    fill: none;
    stroke: #E2E8F0;
    stroke-width: 10;
}
.cm-eval-ring-fill {
    fill: none;
    stroke: #2B59FF;
    stroke-width: 10;
    stroke-linecap: round;
    stroke-dasharray: 326.73;
    stroke-dashoffset: 326.73;
}
.cm-eval-ring-value {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    font-size: 1.45rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1;
}
.cm-eval-verdict-title {
    margin: 0 0 0.35rem;
    font-size: 0.98rem;
    font-weight: 700;
    color: #2B59FF;
}
.cm-eval-verdict-copy {
    margin: 0 0 0.6rem;
    font-size: 0.78rem;
    line-height: 1.45;
    color: #64748B;
}
.cm-eval-go {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.22rem 0.65rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #047857 !important;
    text-decoration: none !important;
    background: #FFFFFF;
    border: 1px solid #A7F3D0;
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}
.cm-eval-go:hover {
    background: #ECFDF5;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.18);
    text-decoration: none !important;
}
.cm-eval-metrics {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    margin-bottom: 0.85rem;
}
.cm-eval-metric {
    display: grid;
    grid-template-columns: 2rem 1fr auto;
    gap: 0.6rem;
    align-items: center;
    width: 100%;
    padding: 0.45rem 0.5rem;
    border: 1px solid transparent;
    border-radius: 12px;
    background: transparent;
    cursor: pointer;
    text-align: left;
    font: inherit;
    color: inherit;
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}
.cm-eval-metric:hover {
    background: #F8FAFC;
    border-color: #E2E8F0;
    transform: translateX(3px);
}
.cm-eval-metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 10px;
    color: #2B59FF;
    background: #EFF6FF;
    flex-shrink: 0;
}
.cm-eval-metric-body { min-width: 0; }
.cm-eval-metric-label {
    display: block;
    margin-bottom: 0.28rem;
    font-size: 0.74rem;
    font-weight: 600;
    color: #475569;
}
.cm-eval-metric-bar {
    height: 0.38rem;
    border-radius: 999px;
    background: #E2E8F0;
    overflow: hidden;
}
.cm-eval-metric-bar i {
    display: block;
    height: 100%;
    width: 0%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2B59FF 0%, #3B82F6 100%);
    transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
}
.cm-eval-metric-bar i.is-warn {
    background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 100%);
}
.cm-eval-metric-score {
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748B;
    white-space: nowrap;
}
.cm-eval-metric-score span {
    font-weight: 600;
    color: #94A3B8;
}
.cm-eval-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 0.78rem 1rem;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: 600;
    color: #2B59FF !important;
    text-decoration: none !important;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.cm-eval-footer:hover {
    background: #DBEAFE;
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(43, 89, 255, 0.15);
    text-decoration: none !important;
}
.cm-eval-click:focus-visible {
    outline: 2px solid #2B59FF;
    outline-offset: 2px;
}

.cm-hero-card {
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    border-radius: 20px;
    padding: 1.25rem;
    box-shadow: var(--cm-shadow-lg);
}
.cm-hero-card-top {
    display: flex;
    gap: 0.85rem;
    margin-bottom: 1rem;
}
.cm-hero-card-img {
    width: 4.5rem;
    height: 4.5rem;
    border-radius: 14px;
    object-fit: cover;
    background: #F1F5F9;
}
.cm-hero-card-info { flex: 1; min-width: 0; }
.cm-hero-card-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    margin-bottom: 0.35rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #047857;
    background: var(--cm-green-soft);
}
.cm-hero-card-name {
    margin: 0 0 0.35rem;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--cm-navy);
    line-height: 1.3;
}
.cm-hero-verdict-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.85rem 1rem;
    margin-bottom: 0.85rem;
    border-radius: 14px;
    background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
    border: 1px solid #A7F3D0;
}
.cm-hero-verdict-score {
    font-size: 1.75rem;
    font-weight: 800;
    color: #047857;
    line-height: 1;
}
.cm-hero-verdict-score small {
    font-size: 0.75rem;
    font-weight: 600;
    color: #059669;
}
.cm-hero-verdict-label {
    text-align: right;
    font-size: 0.78rem;
    font-weight: 700;
    color: #047857;
    line-height: 1.35;
}
.cm-hero-dots {
    display: flex;
    gap: 0.25rem;
    margin: 0.5rem 0;
}
.cm-hero-dot {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 999px;
    background: #22C55E;
}
.cm-hero-dot.is-dim { background: #BBF7D0; }
.cm-hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-bottom: 0.85rem;
}
.cm-pill {
    display: inline-flex;
    padding: 0.22rem 0.55rem;
    border-radius: 8px;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--cm-blue-deep, #1E3A8A);
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
}
.cm-hero-stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.5rem;
    padding-top: 0.85rem;
    border-top: 1px solid #EEF2F6;
}
.cm-hero-stat-mini label {
    display: block;
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94A3B8;
    margin-bottom: 0.15rem;
}
.cm-hero-stat-mini strong {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--cm-navy);
}
.cm-hero-stat-mini strong.is-green { color: #059669; }

/* Live market — section 2 */
.cm-live-market {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 3.5rem max(1.5rem, calc(50vw - 590px)) 4rem;
    background:
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(43, 89, 255, 0.12) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
        linear-gradient(180deg, #F0F5FF 0%, #FFFFFF 42%, #F8FAFC 100%);
    border-top: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
    overflow: hidden;
}
.cm-live-market::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(43, 89, 255, 0.04) 1px, transparent 1px);
    background-size: 24px 24px;
    pointer-events: none;
    opacity: 0.6;
}
.cm-live-inner { position: relative; max-width: 1180px; margin: 0 auto; }
.cm-live-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1.5rem;
    margin-bottom: 1.75rem;
    flex-wrap: wrap;
}
.cm-live-head-main { max-width: 640px; }
.cm-live-pulse {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.35rem 0.85rem;
    margin-bottom: 0.85rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #1D4ED8;
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid #BFDBFE;
    box-shadow: 0 2px 8px rgba(43, 89, 255, 0.08);
}
.cm-live-pulse-dot {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 999px;
    background: #22C55E;
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.5);
    animation: cm-live-pulse 2s ease infinite;
}
@keyframes cm-live-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.45); }
    50% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
}
.cm-live-title {
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.08;
    margin: 0 0 0.65rem;
    color: #0A1128;
}
.cm-live-title span {
    color: var(--cm-blue-bright);
}
.cm-live-lead {
    margin: 0;
    font-size: 1.05rem;
    line-height: 1.6;
    color: #64748B;
}
.cm-live-cta-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.72rem 1.15rem;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: 600;
    color: #FFFFFF !important;
    text-decoration: none !important;
    background: linear-gradient(135deg, #2B59FF 0%, #0052FF 100%);
    border: 1px solid rgba(0, 82, 255, 0.15);
    box-shadow: 0 4px 14px rgba(43, 89, 255, 0.28);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    white-space: nowrap;
}
.cm-live-cta-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(43, 89, 255, 0.35);
    text-decoration: none !important;
}
.cm-live-stats {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.85rem;
    margin-bottom: 1.75rem;
}
.cm-live-stat {
    padding: 0.85rem 1rem;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(226, 232, 240, 0.9);
    backdrop-filter: blur(8px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.cm-live-stat:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}
.cm-live-stat strong {
    display: block;
    font-size: 1.15rem;
    font-weight: 800;
    color: #0A1128;
    margin-bottom: 0.15rem;
}
.cm-live-stat span {
    font-size: 0.72rem;
    font-weight: 500;
    color: #64748B;
}
.cm-scan-shell { position: relative; margin-bottom: 3rem; }
.cm-scan-shell::before,
.cm-scan-shell::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    width: 80px;
    z-index: 2;
    pointer-events: none;
}
.cm-scan-shell::before {
    left: 0;
    background: linear-gradient(90deg, #F4F7FF 0%, transparent 100%);
}
.cm-scan-shell::after {
    right: 0;
    background: linear-gradient(270deg, #FAFBFC 0%, transparent 100%);
}
.cm-scan-viewport {
    overflow: hidden;
    cursor: grab;
    touch-action: pan-y;
    padding: 0.5rem 0;
}
.cm-scan-viewport.is-grabbing { cursor: grabbing; }
.cm-scan-track {
    display: flex;
    gap: 1.25rem;
    width: max-content;
    will-change: transform;
}
.cm-live-card {
    flex: 0 0 260px;
    width: 260px;
    position: relative;
    display: block;
    text-align: left;
    text-decoration: none !important;
    color: inherit;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(15, 23, 42, 0.04), 0 16px 32px rgba(15, 23, 42, 0.06);
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.2s ease;
    cursor: pointer;
    font: inherit;
    padding: 0;
}
.cm-live-card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 12px 28px rgba(43, 89, 255, 0.12), 0 24px 48px rgba(15, 23, 42, 0.1);
    border-color: #BFDBFE;
    text-decoration: none !important;
}
.cm-live-card-score {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    z-index: 3;
    min-width: 2.5rem;
    padding: 0.3rem 0.5rem;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 800;
    text-align: center;
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.15);
}
.cm-live-card-score--strong { background: linear-gradient(135deg, #15803D, #22C55E); }
.cm-live-card-score--go { background: linear-gradient(135deg, #16A34A, #4ADE80); color: #052e16; }
.cm-live-card-score--caution { background: linear-gradient(135deg, #EAB308, #FACC15); color: #713F12; }
.cm-live-card-score--risk { background: linear-gradient(135deg, #EA580C, #FB923C); }
.cm-live-card-score--walk { background: linear-gradient(135deg, #DC2626, #F87171); }
.cm-live-card-img {
    position: relative;
    height: 140px;
    background: linear-gradient(135deg, #F1F5F9, #E2E8F0);
    overflow: hidden;
}
.cm-live-card-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}
.cm-live-card:hover .cm-live-card-img img { transform: scale(1.06); }
.cm-live-card-category {
    position: absolute;
    bottom: 0.65rem;
    left: 0.65rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #FFFFFF;
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(4px);
}
.cm-live-card-body { padding: 1rem 1rem 1.1rem; }
.cm-live-card-name {
    margin: 0 0 0.55rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.35;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.cm-live-card-verdict {
    display: inline-flex;
    margin-bottom: 0.65rem;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.cm-live-card-verdict--strong { color: #047857; background: #ECFDF5; border: 1px solid #A7F3D0; }
.cm-live-card-verdict--go { color: #15803D; background: #F0FDF4; border: 1px solid #BBF7D0; }
.cm-live-card-verdict--caution { color: #A16207; background: #FEFCE8; border: 1px solid #FDE68A; }
.cm-live-card-verdict--risk { color: #C2410C; background: #FFF7ED; border: 1px solid #FED7AA; }
.cm-live-card-verdict--walk { color: #B91C1C; background: #FEF2F2; border: 1px solid #FECACA; }
.cm-live-card-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    font-size: 0.72rem;
    color: #64748B;
}
.cm-live-card-meta strong { display: block; font-size: 0.82rem; color: #0F172A; margin-top: 0.1rem; }
.cm-live-card-meta strong.is-loss { color: #DC2626; }
.cm-live-card-action {
    display: block;
    margin-top: 0.75rem;
    padding-top: 0.75rem;
    border-top: 1px solid #F1F5F9;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--cm-blue-bright);
}

/* Live product catalog (grocery store) */
.cm-live-catalog {
    scroll-margin-top: calc(var(--ps-nav-h, 76px) + 1rem);
}
.cm-catalog-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.25rem;
}
.cm-catalog-title {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 800;
    color: #0A1128;
    letter-spacing: -0.02em;
}
.cm-catalog-title span { color: var(--cm-blue-bright); }
.cm-catalog-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}
.cm-catalog-filter {
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748B;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}
.cm-catalog-filter:hover {
    border-color: #BFDBFE;
    color: #1D4ED8;
}
.cm-catalog-filter.is-active {
    color: #FFFFFF;
    background: linear-gradient(135deg, #2B59FF, #0052FF);
    border-color: transparent;
    box-shadow: 0 4px 12px rgba(43, 89, 255, 0.25);
}
.cm-catalog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}
.cm-catalog-item {
    display: flex;
    flex-direction: column;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    overflow: hidden;
    text-decoration: none !important;
    color: inherit;
    cursor: pointer;
    font: inherit;
    padding: 0;
    text-align: left;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03);
    transition: transform 0.25s ease, box-shadow 0.25s ease, opacity 0.3s ease;
    animation: cm-shelf-in 0.5s ease backwards;
}
@keyframes cm-shelf-in {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
.cm-catalog-item:nth-child(1) { animation-delay: 0.02s; }
.cm-catalog-item:nth-child(2) { animation-delay: 0.04s; }
.cm-catalog-item:nth-child(3) { animation-delay: 0.06s; }
.cm-catalog-item:nth-child(4) { animation-delay: 0.08s; }
.cm-catalog-item:nth-child(5) { animation-delay: 0.1s; }
.cm-catalog-item:nth-child(6) { animation-delay: 0.12s; }
.cm-catalog-item:nth-child(7) { animation-delay: 0.14s; }
.cm-catalog-item:nth-child(8) { animation-delay: 0.16s; }
.cm-catalog-item:nth-child(9) { animation-delay: 0.18s; }
.cm-catalog-item:nth-child(10) { animation-delay: 0.2s; }
.cm-catalog-item:nth-child(11) { animation-delay: 0.22s; }
.cm-catalog-item:nth-child(12) { animation-delay: 0.24s; }
.cm-catalog-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
    border-color: #BFDBFE;
}
.cm-catalog-item.is-hidden { display: none; }
.cm-catalog-item-img {
    position: relative;
    height: 110px;
    background: #F1F5F9;
}
.cm-catalog-item-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.cm-catalog-item-score {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.2rem 0.45rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 800;
    color: #FFFFFF;
}
.cm-catalog-item-body { padding: 0.75rem 0.85rem 0.9rem; flex: 1; }
.cm-catalog-item-name {
    margin: 0 0 0.35rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.3;
}
.cm-catalog-item-tag {
    font-size: 0.65rem;
    font-weight: 600;
    color: #64748B;
}
.cm-catalog-aisle {
    grid-column: 1 / -1;
    margin: 1.25rem 0 0.35rem;
    padding: 0.35rem 0;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
    border-bottom: 1px dashed #E2E8F0;
}
.cm-catalog-aisle:first-child { margin-top: 0; }

/* Investigation engine */
.cm-engine-grid {
    display: grid;
    grid-template-columns: 1fr 1.2fr 0.85fr;
    gap: 2rem;
    align-items: center;
}
.cm-engine-diagram {
    position: relative;
    min-height: 320px;
    display: grid;
    place-items: center;
}
.cm-engine-core {
    width: 5rem;
    height: 5rem;
    border-radius: 999px;
    background: linear-gradient(135deg, var(--cm-blue-bright), var(--cm-blue));
    color: #FFFFFF;
    display: grid;
    place-items: center;
    font-size: 0.65rem;
    font-weight: 800;
    text-align: center;
    line-height: 1.2;
    box-shadow: 0 0 0 12px rgba(0, 82, 255, 0.12), 0 16px 40px rgba(0, 82, 255, 0.25);
    animation: cm-pulse 3s ease-in-out infinite;
    z-index: 2;
}
@keyframes cm-pulse {
    0%, 100% { box-shadow: 0 0 0 12px rgba(0, 82, 255, 0.12), 0 16px 40px rgba(0, 82, 255, 0.25); }
    50% { box-shadow: 0 0 0 20px rgba(0, 82, 255, 0.08), 0 20px 48px rgba(0, 82, 255, 0.35); }
}
.cm-engine-orbit {
    position: absolute;
    padding: 0.35rem 0.65rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #334155;
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
    white-space: nowrap;
    animation: cm-orbit-in 0.6s ease backwards;
}
.cm-engine-orbit:nth-child(2) { top: 8%; left: 18%; animation-delay: 0.1s; }
.cm-engine-orbit:nth-child(3) { top: 5%; right: 12%; animation-delay: 0.15s; }
.cm-engine-orbit:nth-child(4) { top: 38%; left: 2%; animation-delay: 0.2s; }
.cm-engine-orbit:nth-child(5) { top: 42%; right: 0; animation-delay: 0.25s; }
.cm-engine-orbit:nth-child(6) { bottom: 18%; left: 10%; animation-delay: 0.3s; }
.cm-engine-orbit:nth-child(7) { bottom: 12%; right: 8%; animation-delay: 0.35s; }
.cm-engine-orbit:nth-child(8) { bottom: 38%; left: 28%; animation-delay: 0.4s; }
@keyframes cm-orbit-in {
    from { opacity: 0; transform: scale(0.85); }
    to { opacity: 1; transform: scale(1); }
}
.cm-legend-card {
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    border-radius: var(--cm-radius);
    padding: 1.25rem;
    box-shadow: var(--cm-shadow);
}
.cm-legend-title {
    margin: 0 0 1rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-legend-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid #F1F5F9;
    font-size: 0.82rem;
}
.cm-legend-row:last-child { border-bottom: none; }
.cm-legend-swatch {
    width: 2.5rem;
    height: 0.45rem;
    border-radius: 999px;
    flex-shrink: 0;
}
.cm-legend-label { font-weight: 700; color: var(--cm-navy); min-width: 5.5rem; }
.cm-legend-desc { color: var(--cm-muted); font-size: 0.78rem; }

/* How it works */
.cm-steps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
}
.cm-step-card {
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    border-radius: var(--cm-radius);
    padding: 1.35rem;
    box-shadow: var(--cm-shadow);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.cm-step-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--cm-shadow-lg);
}
.cm-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.75rem;
    height: 1.75rem;
    margin-bottom: 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 800;
    color: #FFFFFF;
    background: var(--cm-blue);
}
.cm-step-title {
    margin: 0 0 0.35rem;
    font-size: 1rem;
    font-weight: 700;
    color: var(--cm-navy);
}
.cm-step-body {
    margin: 0 0 1rem;
    font-size: 0.84rem;
    line-height: 1.55;
    color: var(--cm-muted);
}
.cm-step-mock {
    border-radius: 12px;
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    padding: 1rem;
    min-height: 100px;
    display: grid;
    place-items: center;
    font-size: 0.78rem;
    color: #94A3B8;
    text-align: center;
}

/* Stats bar */
.cm-stats-bar {
    background: linear-gradient(135deg, #0A1128 0%, #1E293B 100%);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    flex-wrap: wrap;
    box-shadow: var(--cm-shadow-lg);
}
.cm-stats-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    max-width: 280px;
}
.cm-stats-brand-icon {
    font-size: 1.5rem;
}
.cm-stats-brand-text {
    margin: 0;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #E2E8F0;
    line-height: 1.4;
}
.cm-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1.5rem;
    flex: 1;
}
.cm-stat-item strong {
    display: block;
    font-size: 1.05rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0.15rem;
}
.cm-stat-item span {
    font-size: 0.72rem;
    color: #94A3B8;
    line-height: 1.35;
}

/* Report preview */
.cm-report-shell {
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: var(--cm-shadow-lg);
}
.cm-report-layout {
    display: grid;
    grid-template-columns: 200px 1fr;
    min-height: 420px;
}
.cm-report-nav {
    background: #F8FAFC;
    border-right: 1px solid var(--cm-border);
    padding: 1rem 0.75rem;
}
.cm-report-nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.55rem 0.65rem;
    margin-bottom: 0.25rem;
    border-radius: 10px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #64748B;
    line-height: 1.3;
}
.cm-report-nav-item.is-active {
    background: #EFF6FF;
    color: var(--cm-blue);
}
.cm-report-nav-item.is-locked { opacity: 0.55; }
.cm-report-main { padding: 1.25rem; }
.cm-report-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #EEF2F6;
}
.cm-report-product-img {
    width: 4rem;
    height: 4rem;
    border-radius: 12px;
    object-fit: cover;
}
.cm-report-kpis {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.65rem;
    margin-bottom: 1rem;
}
.cm-report-kpi {
    padding: 0.65rem;
    border-radius: 12px;
    background: #F8FAFC;
    border: 1px solid #EEF2F6;
}
.cm-report-kpi label {
    display: block;
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 0.2rem;
}
.cm-report-kpi strong { font-size: 0.88rem; color: var(--cm-navy); }
.cm-report-verdict {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 14px;
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border: 1px solid #A7F3D0;
}
.cm-report-verdict-score {
    font-size: 2rem;
    font-weight: 800;
    color: #047857;
}
.cm-report-charts {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 1rem;
}
.cm-chart-box {
    padding: 1rem;
    border-radius: 12px;
    background: #F8FAFC;
    border: 1px solid #EEF2F6;
    min-height: 120px;
}
.cm-chart-title {
    margin: 0 0 0.65rem;
    font-size: 0.72rem;
    font-weight: 700;
    color: #475569;
}
.cm-chart-bars {
    display: flex;
    align-items: flex-end;
    gap: 0.35rem;
    height: 70px;
}
.cm-chart-bar {
    flex: 1;
    border-radius: 4px 4px 0 0;
    background: linear-gradient(180deg, var(--cm-blue), #93C5FD);
    animation: cm-bar-grow 1s ease backwards;
}
@keyframes cm-bar-grow {
    from { transform: scaleY(0); transform-origin: bottom; }
    to { transform: scaleY(1); }
}
.cm-risk-list { list-style: none; padding: 0; margin: 0; }
.cm-risk-list li {
    display: flex;
    gap: 0.45rem;
    padding: 0.35rem 0;
    font-size: 0.78rem;
    color: #475569;
}
.cm-report-footer {
    padding: 0.85rem 1.25rem;
    border-top: 1px solid #EEF2F6;
    text-align: right;
}
.cm-report-footer a {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--cm-blue) !important;
    text-decoration: none !important;
}

/* Premium unlock */
.cm-premium-grid {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 2rem;
    align-items: start;
}
.cm-premium-checklist {
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    border-radius: var(--cm-radius);
    padding: 1.25rem;
}
.cm-premium-checklist h3 {
    margin: 0 0 1rem;
    font-size: 0.95rem;
    font-weight: 700;
}
.cm-check-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0;
    font-size: 0.82rem;
    color: #334155;
}
.cm-check-row.is-no { color: #94A3B8; }
.cm-section-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
}
.cm-section-mini {
    padding: 1rem;
    border-radius: 14px;
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    min-height: 140px;
    position: relative;
    overflow: hidden;
}
.cm-section-mini.is-locked {
    filter: blur(2px);
    opacity: 0.7;
}
.cm-section-mini.is-locked::after {
    content: "🔒 Premium";
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,0.75);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--cm-blue);
}
.cm-section-mini-num {
    font-size: 0.65rem;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
}
.cm-section-mini-title {
    margin: 0.25rem 0 0;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--cm-navy);
}
.cm-pricing-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 1.75rem;
    padding: 1.25rem 1.5rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid #BFDBFE;
}
.cm-pricing-points {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem 1.25rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: #1E40AF;
}
.cm-pricing-price {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--cm-navy);
}
.cm-pricing-price span { font-size: 0.85rem; font-weight: 600; color: var(--cm-muted); }

/* Score legend (dark) */
.cm-score-cards {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.85rem;
    margin-bottom: 2rem;
}
.cm-score-card {
    padding: 1rem 0.85rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.04);
    transition: transform 0.2s ease, background 0.2s ease;
}
.cm-score-card:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.07);
}
.cm-score-range {
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.cm-score-label {
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
}
.cm-score-desc {
    font-size: 0.72rem;
    color: #94A3B8;
    line-height: 1.4;
    margin: 0;
}
.cm-score-card--strong { border-top: 3px solid #15803D; }
.cm-score-card--go { border-top: 3px solid #22C55E; }
.cm-score-card--caution { border-top: 3px solid #FACC15; }
.cm-score-card--risk { border-top: 3px solid #F97316; }
.cm-score-card--walk { border-top: 3px solid #EF4444; }
.cm-brutal-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: start;
}
.cm-brutal-card {
    padding: 1.25rem;
    border-radius: 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
}
.cm-brutal-card h3 {
    margin: 0 0 0.65rem;
    font-size: 1rem;
    font-weight: 700;
}
.cm-brutal-card p {
    margin: 0;
    font-size: 0.84rem;
    line-height: 1.6;
    color: #94A3B8;
}
.cm-value-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 2rem;
    padding: 1.25rem;
    border-radius: 14px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
}
.cm-value-item {
    text-align: center;
    font-size: 0.78rem;
    color: #CBD5E1;
}
.cm-value-item strong {
    display: block;
    font-size: 0.92rem;
    color: #FFFFFF;
    margin-bottom: 0.2rem;
}
.cm-quote {
    margin: 2rem 0 0;
    text-align: center;
    font-size: 1.05rem;
    font-style: italic;
    color: #94A3B8;
}

/* Reviews */
.cm-reviews-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
}
.cm-review-card {
    padding: 1.35rem;
    border-radius: var(--cm-radius);
    background: #FFFFFF;
    border: 1px solid var(--cm-border);
    box-shadow: var(--cm-shadow);
    transition: transform 0.25s ease;
}
.cm-review-card:hover { transform: translateY(-4px); }
.cm-review-stars { color: #FBBF24; font-size: 0.85rem; margin-bottom: 0.65rem; }
.cm-review-text {
    margin: 0 0 1rem;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #334155;
}
.cm-review-author {
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.cm-review-author strong {
    display: block;
    font-size: 0.82rem;
    color: var(--cm-navy);
}
.cm-review-author span { font-size: 0.72rem; color: var(--cm-muted); }

/* FAQ */
.cm-faq-list { max-width: 760px; margin: 0 auto; }
.cm-faq-item {
    border: 1px solid var(--cm-border);
    border-radius: 12px;
    margin-bottom: 0.65rem;
    background: #FFFFFF;
    overflow: hidden;
    transition: box-shadow 0.2s ease;
}
.cm-faq-item[open] { box-shadow: var(--cm-shadow); }
.cm-faq-item summary {
    padding: 1rem 1.15rem;
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--cm-navy);
    cursor: pointer;
    list-style: none;
}
.cm-faq-item summary::-webkit-details-marker { display: none; }
.cm-faq-answer {
    padding: 0 1.15rem 1rem;
    margin: 0;
    font-size: 0.88rem;
    line-height: 1.6;
    color: var(--cm-muted);
}

/* Final CTA */
.cm-final {
    text-align: center;
    padding: 4rem 0 3rem;
}
.cm-final .cm-title { margin-bottom: 1.25rem; }
.cm-footer {
    text-align: center;
    padding: 1.5rem 0 2rem;
    font-size: 0.78rem;
    color: #94A3B8;
}

/* Animations / reveal */
@keyframes cm-hero-rise {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}
.cm-animate-in {
    opacity: 0;
    animation: cm-hero-rise 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.cm-animate-in-delay-1 { animation-delay: 0.1s; }
.cm-animate-in-delay-2 { animation-delay: 0.2s; }
.cm-animate-in-delay-3 { animation-delay: 0.3s; }
.cm-animate-in-delay-4 { animation-delay: 0.4s; }

html.cm-reveal-ready .cm-reveal:not(.is-visible) {
    opacity: 0;
    transform: translateY(28px);
}
.cm-reveal {
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}
.cm-reveal.is-visible {
    opacity: 1;
    transform: none;
}

@media (max-width: 960px) {
    .cm-hero-grid,
    .cm-engine-grid,
    .cm-premium-grid,
    .cm-brutal-grid,
    .cm-report-layout { grid-template-columns: 1fr; }
    .cm-eval-score-row { grid-template-columns: 1fr; justify-items: start; }
    .cm-eval-financials { grid-template-columns: 1fr 1fr; }
    .cm-eval-fin-divider { display: none; }
    .cm-steps-grid,
    .cm-reviews-grid,
    .cm-score-cards,
    .cm-section-cards { grid-template-columns: 1fr; }
    .cm-stats-grid { grid-template-columns: 1fr 1fr; }
    .cm-report-kpis { grid-template-columns: repeat(2, 1fr); }
    .cm-report-charts { grid-template-columns: 1fr; }
    .cm-hero-stats-row { grid-template-columns: repeat(2, 1fr); }
    .cm-value-bar { grid-template-columns: 1fr; }
    .cm-stats-bar { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 640px) {
    .cm-section { padding: 3rem 0; }
    .cm-page { padding: 0 1rem; }
    .cm-live-stats { grid-template-columns: 1fr 1fr; }
    .cm-live-head { flex-direction: column; align-items: flex-start; }
    .cm-catalog-grid { grid-template-columns: repeat(2, 1fr); }
}
"""
