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
.cm-hero-screen {
    min-height: max(
        calc(100dvh - var(--ps-nav-h, 76px)),
        calc(100svh - var(--ps-nav-h, 76px))
    );
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 5.5rem max(1.5rem, calc(50vw - 590px)) 6.5rem;
    box-sizing: border-box;
    background: #FFFFFF;
    overflow: hidden;
}
.cm-hero-screen .cm-page.cm-hero {
    width: 100%;
    max-width: 1180px;
    margin: 0 auto;
    padding: 0;
}
.cm-hero {
    padding: 0;
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
.cm-catalog-page {
    padding: 1.25rem 0 4.5rem;
    background: linear-gradient(180deg, #F8FAFF 0%, #FFFFFF 38%, #F8FAFC 100%);
}
.cm-catalog-back {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin-bottom: 1.5rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: #475569;
    text-decoration: none !important;
    transition: color 0.2s ease;
}
.cm-catalog-back:hover { color: var(--cm-blue-bright); }
.cm-catalog-page-hero {
    max-width: 720px;
    margin-bottom: 2rem;
}
.cm-catalog-page-title {
    margin: 0.75rem 0 0.65rem;
    font-size: clamp(1.85rem, 4vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #0A1128;
    line-height: 1.1;
}
.cm-catalog-page-title span { color: var(--cm-blue-bright); }
.cm-catalog-page-lead {
    margin: 0;
    font-size: 1.02rem;
    line-height: 1.65;
    color: #64748B;
}
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

/* Platform — engine + how it works + stats (combined) */
.cm-platform {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 3.75rem max(1.5rem, calc(50vw - 590px)) 3.5rem;
    background:
        radial-gradient(ellipse 70% 55% at 85% 5%, rgba(43, 89, 255, 0.1) 0%, transparent 58%),
        radial-gradient(ellipse 55% 45% at 5% 35%, rgba(6, 182, 212, 0.07) 0%, transparent 52%),
        linear-gradient(180deg, #FFFFFF 0%, #F4F8FF 38%, #F8FAFC 100%);
    border-top: 1px solid #E2E8F0;
    overflow: hidden;
}
.cm-platform::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(43, 89, 255, 0.035) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
    opacity: 0.55;
}
.cm-platform-inner {
    position: relative;
    max-width: 1180px;
    margin: 0 auto;
}
.cm-platform-head { max-width: 760px; margin-bottom: 2.25rem; }
.cm-platform-title {
    margin: 0 0 0.75rem;
    font-size: clamp(1.85rem, 3.8vw, 2.65rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: #0A1128;
}
.cm-platform-title span { color: var(--cm-blue-bright); }
.cm-platform-lead {
    margin: 0;
    font-size: 1.05rem;
    line-height: 1.65;
    color: #64748B;
}
.cm-platform-engine-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
    gap: 2rem;
    align-items: center;
    margin-bottom: 3rem;
}
.cm-platform-signals {
    display: grid;
    gap: 0.85rem;
}
.cm-platform-signal {
    display: flex;
    gap: 0.85rem;
    align-items: flex-start;
    padding: 1rem 1.1rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(226, 232, 240, 0.95);
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.cm-platform-signal:hover {
    transform: translateY(-3px);
    border-color: #BFDBFE;
    box-shadow: 0 12px 28px rgba(43, 89, 255, 0.08);
}
.cm-platform-signal-icon {
    flex-shrink: 0;
    width: 2.35rem;
    height: 2.35rem;
    display: grid;
    place-items: center;
    border-radius: 12px;
    font-size: 1.05rem;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid #BFDBFE;
}
.cm-platform-signal-title {
    margin: 0 0 0.25rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #0A1128;
}
.cm-platform-signal-body {
    margin: 0;
    font-size: 0.82rem;
    line-height: 1.55;
    color: #64748B;
}
.cm-platform-hub {
    position: relative;
    width: 100%;
    max-width: 420px;
    margin: 0 auto;
}
.cm-platform-hub-stage {
    position: relative;
    width: 100%;
    aspect-ratio: 1;
}
.cm-platform-hub-lines {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}
.cm-platform-hub-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    border-radius: 999px;
    border: 1px solid rgba(43, 89, 255, 0.14);
    pointer-events: none;
    transform: translate(-50%, -50%);
}
.cm-platform-hub-ring--outer {
    width: 72%;
    height: 72%;
    transform: translate(-50%, -50%);
}
.cm-platform-hub-ring--inner {
    width: 56%;
    height: 56%;
    border-color: rgba(43, 89, 255, 0.08);
    border-style: dashed;
}
.cm-platform-orbit-field {
    position: absolute;
    inset: 0;
    pointer-events: none;
}
.cm-platform-hub-core {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 4;
    width: 5.5rem;
    height: 5.5rem;
    margin: -2.75rem 0 0 -2.75rem;
    border-radius: 999px;
    background: linear-gradient(135deg, var(--cm-blue-bright), var(--cm-blue));
    color: #FFFFFF;
    display: grid;
    place-items: center;
    font-size: 0.68rem;
    font-weight: 800;
    text-align: center;
    line-height: 1.2;
    pointer-events: none;
    box-shadow: 0 0 0 14px rgba(0, 82, 255, 0.1), 0 20px 48px rgba(0, 82, 255, 0.28);
    animation: cm-platform-core-pulse 3.5s ease-in-out infinite;
}
@keyframes cm-platform-core-pulse {
    0%, 100% { box-shadow: 0 0 0 14px rgba(0, 82, 255, 0.1), 0 20px 48px rgba(0, 82, 255, 0.28); }
    50% { box-shadow: 0 0 0 22px rgba(0, 82, 255, 0.06), 0 24px 56px rgba(0, 82, 255, 0.38); }
}
.cm-platform-orbit {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 3;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.42rem 0.72rem 0.42rem 0.52rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #334155;
    background: rgba(255, 255, 255, 0.97);
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
    white-space: nowrap;
    pointer-events: none;
    will-change: transform;
    transform:
        rotate(var(--orbit-angle))
        translateX(var(--orbit-radius))
        rotate(calc(-1 * var(--orbit-angle)))
        translate(calc(-50% + var(--repel-x, 0px)), calc(-50% + var(--repel-y, 0px)));
    animation: cm-platform-orbit-in 0.65s ease backwards;
}
@keyframes cm-platform-orbit-in {
    from { opacity: 0; filter: blur(2px); }
    to { opacity: 1; filter: blur(0); }
}
.cm-platform-orbit:nth-child(1) { animation-delay: 0.05s; }
.cm-platform-orbit:nth-child(2) { animation-delay: 0.1s; }
.cm-platform-orbit:nth-child(3) { animation-delay: 0.15s; }
.cm-platform-orbit:nth-child(4) { animation-delay: 0.2s; }
.cm-platform-orbit:nth-child(5) { animation-delay: 0.25s; }
.cm-platform-orbit:nth-child(6) { animation-delay: 0.3s; }
.cm-platform-orbit:nth-child(7) { animation-delay: 0.35s; }
.cm-platform-orbit-logo {
    width: 1rem;
    height: 1rem;
    object-fit: contain;
    flex-shrink: 0;
}
.cm-platform-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 0 0 2rem;
    color: #94A3B8;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.cm-platform-divider::before,
.cm-platform-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
}
.cm-platform-divider span {
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    color: #1D4ED8;
}
.cm-platform-steps-block { margin-bottom: 0; }
.cm-platform-steps-head {
    text-align: center;
    max-width: 640px;
    margin: 0 auto 1.75rem;
}
.cm-platform-steps-title {
    margin: 0 0 0.55rem;
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0A1128;
}
.cm-platform-steps-title span { color: var(--cm-blue-bright); }
.cm-platform-steps-lead {
    margin: 0;
    font-size: 0.95rem;
    line-height: 1.6;
    color: #64748B;
}
.cm-platform-steps-track {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.15rem;
    position: relative;
}
.cm-platform-steps-track::before {
    content: "";
    position: absolute;
    top: 2.1rem;
    left: 12%;
    right: 12%;
    height: 2px;
    background: linear-gradient(90deg, #BFDBFE, #2B59FF, #BFDBFE);
    opacity: 0.45;
    z-index: 0;
}
.cm-platform-step {
    position: relative;
    z-index: 1;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 1.35rem 1.25rem 1.2rem;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.05);
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.25s ease;
}
.cm-platform-step:hover {
    transform: translateY(-6px);
    border-color: #BFDBFE;
    box-shadow: 0 16px 40px rgba(43, 89, 255, 0.1);
}
.cm-platform-step-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
}
.cm-platform-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    color: #FFFFFF;
    background: linear-gradient(135deg, #2B59FF, #0052FF);
    box-shadow: 0 4px 12px rgba(43, 89, 255, 0.35);
}
.cm-platform-step-time {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #64748B;
    padding: 0.25rem 0.55rem;
    border-radius: 999px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
}
.cm-platform-step-title {
    margin: 0 0 0.4rem;
    font-size: 1.02rem;
    font-weight: 700;
    color: #0A1128;
}
.cm-platform-step-body {
    margin: 0 0 1rem;
    font-size: 0.84rem;
    line-height: 1.55;
    color: #64748B;
}
.cm-platform-step-mock {
    border-radius: 14px;
    background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    border: 1px dashed #CBD5E1;
    padding: 1rem;
    min-height: 108px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.55rem;
    text-align: center;
}
.cm-step-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.45rem 0.7rem;
    border-radius: 10px;
    font-size: 0.74rem;
    font-weight: 600;
    color: #475569;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
}
.cm-step-scan {
    position: relative;
    overflow: hidden;
    width: 100%;
    font-size: 0.78rem;
    font-weight: 600;
    color: #334155;
}
.cm-step-scan-line {
    position: absolute;
    left: 0;
    top: 50%;
    width: 35%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #2B59FF, transparent);
    animation: cm-step-scan-sweep 2.2s ease-in-out infinite;
}
@keyframes cm-step-scan-sweep {
    0% { transform: translateX(-20%); opacity: 0; }
    20% { opacity: 1; }
    80% { opacity: 1; }
    100% { transform: translateX(320%); opacity: 0; }
}
.cm-step-scan-tags {
    font-size: 0.72rem;
    color: #94A3B8;
}
.cm-step-result {
    display: flex;
    align-items: baseline;
    gap: 0.15rem;
    justify-content: center;
}
.cm-step-result strong {
    font-size: 1.75rem;
    font-weight: 800;
    color: #059669;
    line-height: 1;
}
.cm-step-result span {
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748B;
}
.cm-step-result em {
    margin-left: 0.5rem;
    font-style: normal;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #047857;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
}
.cm-step-result-link {
    font-size: 0.74rem;
    font-weight: 600;
    color: var(--cm-blue-bright);
}
.cm-site-stats {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 2rem max(1.5rem, calc(50vw - 590px)) 1.25rem;
    background: linear-gradient(135deg, #0A1128 0%, #1E293B 55%, #0F172A 100%);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.cm-site-stats-inner {
    max-width: 1180px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.cm-site-stats-brand {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    max-width: 280px;
}
.cm-site-stats-icon { font-size: 1.6rem; }
.cm-site-stats-brand p {
    margin: 0;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #E2E8F0;
    line-height: 1.45;
}
.cm-site-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 1.25rem;
    flex: 1;
}
.cm-site-stat strong {
    display: block;
    font-size: 1.1rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0.15rem;
}
.cm-site-stat span {
    font-size: 0.72rem;
    color: #94A3B8;
    line-height: 1.4;
}
.cm-site-stats-foot {
    max-width: 1180px;
    margin: 1.25rem auto 0;
    text-align: center;
    font-size: 0.74rem;
    color: #64748B;
}

/* Report preview — Apple-inspired dashboard */
.cm-rpt {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 5rem max(1.5rem, calc(50vw - 590px)) 5.5rem;
    background:
        radial-gradient(ellipse 80% 55% at 20% 0%, rgba(43, 89, 255, 0.07) 0%, transparent 55%),
        radial-gradient(ellipse 60% 45% at 90% 30%, rgba(34, 197, 94, 0.05) 0%, transparent 50%),
        linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 50%, #F5F5F7 100%);
    overflow: hidden;
}
.cm-rpt-inner {
    position: relative;
    max-width: 1180px;
    margin: 0 auto;
}
.cm-rpt-head {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 3rem;
}
.cm-rpt-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.35rem 0.9rem;
    margin-bottom: 1rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #1D4ED8;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(191, 219, 254, 0.9);
    box-shadow: 0 2px 12px rgba(43, 89, 255, 0.08);
}
.cm-rpt-title {
    margin: 0 0 1rem;
    font-size: clamp(2.1rem, 4.5vw, 3.25rem);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.05;
    color: #1D1D1F;
}
.cm-rpt-title span {
    background: linear-gradient(135deg, #2B59FF 0%, #0052FF 50%, #06B6D4 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.cm-rpt-lead {
    margin: 0;
    font-size: 1.08rem;
    line-height: 1.65;
    color: #6E6E73;
}
.cm-rpt-device {
    perspective: 1200px;
}
.cm-rpt-window {
    border-radius: 24px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.95) inset,
        0 32px 80px rgba(15, 23, 42, 0.1),
        0 8px 24px rgba(15, 23, 42, 0.05);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.5s ease;
}
.cm-rpt-window:hover {
    transform: translateY(-4px);
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.95) inset,
        0 40px 96px rgba(15, 23, 42, 0.12),
        0 12px 32px rgba(43, 89, 255, 0.08);
}
.cm-rpt-toolbar {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.85rem 1.15rem;
    background: linear-gradient(180deg, #F5F5F7 0%, #EFEFF4 100%);
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.cm-rpt-dot {
    width: 0.62rem;
    height: 0.62rem;
    border-radius: 999px;
    flex-shrink: 0;
}
.cm-rpt-dot--red { background: #FF5F57; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08); }
.cm-rpt-dot--yellow { background: #FEBC2E; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08); }
.cm-rpt-dot--green { background: #28C840; box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08); }
.cm-rpt-toolbar-title {
    margin-left: 0.5rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #86868B;
}
.cm-rpt-layout {
    display: grid;
    grid-template-columns: 220px minmax(0, 1fr);
    min-height: 460px;
}
.cm-rpt-nav {
    padding: 1rem 0.85rem;
    background: rgba(245, 245, 247, 0.85);
    border-right: 1px solid rgba(0, 0, 0, 0.06);
}
.cm-rpt-nav-item {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.62rem 0.7rem;
    margin-bottom: 0.2rem;
    border-radius: 12px;
    font-size: 0.76rem;
    font-weight: 600;
    line-height: 1.35;
    color: #6E6E73;
    transition: background 0.2s ease, color 0.2s ease;
}
.cm-rpt-nav-item.is-active {
    background: rgba(255, 255, 255, 0.95);
    color: #2B59FF;
    box-shadow: 0 2px 10px rgba(43, 89, 255, 0.08);
}
.cm-rpt-nav-item.is-locked {
    color: #AEAEB2;
}
.cm-rpt-nav-dot {
    width: 0.45rem;
    height: 0.45rem;
    border-radius: 999px;
    border: 1.5px solid #C7C7CC;
    flex-shrink: 0;
}
.cm-rpt-nav-dot.is-active {
    border: none;
    background: #2B59FF;
    box-shadow: 0 0 0 3px rgba(43, 89, 255, 0.18);
}
.cm-rpt-nav-lock {
    width: 0.85rem;
    height: 0.85rem;
    flex-shrink: 0;
    color: #AEAEB2;
}
.cm-rpt-main {
    padding: 1.35rem 1.35rem 1.15rem;
    background: rgba(255, 255, 255, 0.55);
}
.cm-rpt-product {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.15rem;
    padding-bottom: 1.15rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}
.cm-rpt-product-img {
    width: 4.25rem;
    height: 4.25rem;
    border-radius: 16px;
    object-fit: cover;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.1);
    border: 1px solid rgba(0, 0, 0, 0.04);
}
.cm-rpt-product-name {
    margin: 0 0 0.25rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #1D1D1F;
}
.cm-rpt-product-meta {
    margin: 0;
    font-size: 0.78rem;
    color: #86868B;
}
.cm-rpt-verdict {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 1.15rem;
    padding: 1.1rem 1.2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(236, 253, 245, 0.95) 0%, rgba(209, 250, 229, 0.85) 100%);
    border: 1px solid rgba(167, 243, 208, 0.9);
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.08);
}
.cm-rpt-verdict-score {
    margin: 0;
    font-size: 2.15rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
    color: #047857;
}
.cm-rpt-verdict-score span {
    font-size: 1rem;
    font-weight: 600;
    color: #059669;
}
.cm-rpt-verdict-label {
    margin: 0.35rem 0 0;
    font-size: 0.88rem;
    font-weight: 700;
    color: #047857;
}
.cm-rpt-verdict-confidence {
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #047857;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(167, 243, 208, 0.9);
    white-space: nowrap;
}
.cm-rpt-metrics {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.65rem;
    margin-bottom: 1.15rem;
}
.cm-rpt-metric {
    padding: 0.75rem 0.7rem;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(0, 0, 0, 0.05);
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.cm-rpt-metric:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}
.cm-rpt-metric-label {
    display: block;
    margin-bottom: 0.25rem;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-rpt-metric strong {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1D1D1F;
    letter-spacing: -0.01em;
}
.cm-rpt-metric--up strong { color: #059669; }
.cm-rpt-panels {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 0.85rem;
}
.cm-rpt-panel {
    padding: 1rem 1rem 0.95rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(0, 0, 0, 0.05);
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.03);
}
.cm-rpt-panel-title {
    margin: 0 0 0.75rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #6E6E73;
}
.cm-rpt-bars {
    display: flex;
    align-items: flex-end;
    gap: 0.4rem;
    height: 88px;
    padding-top: 0.25rem;
}
.cm-rpt-bar {
    flex: 1;
    height: var(--bar-h, 50%);
    border-radius: 6px 6px 2px 2px;
    background: linear-gradient(180deg, #2B59FF 0%, #93C5FD 100%);
    transform-origin: bottom;
    animation: cm-rpt-bar-grow 0.9s cubic-bezier(0.22, 1, 0.36, 1) backwards;
}
.cm-rpt-bar:nth-child(1) { animation-delay: 0.05s; }
.cm-rpt-bar:nth-child(2) { animation-delay: 0.1s; }
.cm-rpt-bar:nth-child(3) { animation-delay: 0.15s; }
.cm-rpt-bar:nth-child(4) { animation-delay: 0.2s; }
.cm-rpt-bar:nth-child(5) { animation-delay: 0.25s; }
.cm-rpt-bar:nth-child(6) { animation-delay: 0.3s; }
@keyframes cm-rpt-bar-grow {
    from { transform: scaleY(0); opacity: 0.4; }
    to { transform: scaleY(1); opacity: 1; }
}
.cm-rpt-risks {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.55rem;
}
.cm-rpt-risk {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    font-size: 0.78rem;
    line-height: 1.45;
    color: #48484A;
}
.cm-rpt-risk-icon {
    width: 1rem;
    height: 1rem;
    flex-shrink: 0;
    margin-top: 0.05rem;
}
.cm-rpt-risk-icon--warn { color: #F59E0B; }
.cm-rpt-risk-icon--ok { color: #22C55E; }
.cm-rpt-footer {
    display: flex;
    justify-content: flex-end;
    padding: 0.95rem 1.35rem;
    background: rgba(245, 245, 247, 0.9);
    border-top: 1px solid rgba(0, 0, 0, 0.06);
}
.cm-rpt-sample-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.55rem 1rem;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 600;
    color: #2B59FF !important;
    text-decoration: none !important;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(191, 219, 254, 0.9);
    box-shadow: 0 4px 14px rgba(43, 89, 255, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.cm-rpt-sample-link::after {
    content: "→";
    transition: transform 0.2s ease;
}
.cm-rpt-sample-link:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(43, 89, 255, 0.16);
    text-decoration: none !important;
}
.cm-rpt-sample-link:hover::after {
    transform: translateX(3px);
}

/* Premium — Apple-inspired upgrade section */
.cm-pro {
    position: relative;
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    padding: 5rem max(1.5rem, calc(50vw - 590px)) 5.5rem;
    background:
        radial-gradient(ellipse 90% 60% at 50% -10%, rgba(43, 89, 255, 0.09) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 100% 50%, rgba(6, 182, 212, 0.05) 0%, transparent 50%),
        linear-gradient(180deg, #FAFAFA 0%, #F5F5F7 45%, #EFEFF4 100%);
    overflow: hidden;
}
.cm-pro::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(0, 0, 0, 0.025) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    opacity: 0.35;
}
.cm-pro-inner {
    position: relative;
    max-width: 1180px;
    margin: 0 auto;
}
.cm-pro-head {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 3rem;
}
.cm-pro-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.35rem 0.9rem;
    margin-bottom: 1rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #1D4ED8;
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(191, 219, 254, 0.9);
    box-shadow: 0 2px 12px rgba(43, 89, 255, 0.08);
}
.cm-pro-title {
    margin: 0 0 1rem;
    font-size: clamp(2.1rem, 4.5vw, 3.25rem);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.05;
    color: #1D1D1F;
}
.cm-pro-title span {
    background: linear-gradient(135deg, #2B59FF 0%, #0052FF 50%, #06B6D4 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.cm-pro-lead {
    margin: 0;
    font-size: 1.08rem;
    line-height: 1.65;
    color: #6E6E73;
    font-weight: 400;
}
.cm-pro-showcase {
    display: grid;
    grid-template-columns: minmax(280px, 340px) minmax(0, 1fr);
    gap: 1.5rem;
    align-items: start;
    padding: 1.5rem;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.9) inset,
        0 24px 64px rgba(15, 23, 42, 0.07),
        0 2px 8px rgba(15, 23, 42, 0.04);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
}
.cm-pro-compare {
    display: grid;
    gap: 1rem;
}
.cm-pro-plan {
    position: relative;
    padding: 1.35rem 1.25rem 1.25rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease;
}
.cm-pro-plan:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
}
.cm-pro-plan--premium {
    background: linear-gradient(165deg, #FFFFFF 0%, #F8FBFF 100%);
    border-color: rgba(43, 89, 255, 0.22);
    box-shadow:
        0 0 0 1px rgba(43, 89, 255, 0.08),
        0 16px 40px rgba(43, 89, 255, 0.1);
}
.cm-pro-plan--premium::before {
    content: "";
    position: absolute;
    inset: -1px;
    border-radius: 21px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(43, 89, 255, 0.45), rgba(6, 182, 212, 0.2), rgba(43, 89, 255, 0.15));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
.cm-pro-plan--free {
    opacity: 0.92;
    background: rgba(255, 255, 255, 0.65);
}
.cm-pro-plan-ribbon {
    position: absolute;
    top: 0.85rem;
    right: 0.85rem;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #FFFFFF;
    background: linear-gradient(135deg, #2B59FF, #0052FF);
    box-shadow: 0 4px 12px rgba(43, 89, 255, 0.35);
}
.cm-pro-plan-label {
    margin: 0 0 0.15rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-pro-plan--premium .cm-pro-plan-label { color: #2B59FF; }
.cm-pro-plan-price {
    margin: 0 0 1rem;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #1D1D1F;
    line-height: 1;
}
.cm-pro-plan-price span {
    font-size: 0.95rem;
    font-weight: 500;
    color: #86868B;
    letter-spacing: 0;
}
.cm-pro-features {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 0.55rem;
}
.cm-pro-feature {
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    font-size: 0.84rem;
    line-height: 1.45;
    color: #1D1D1F;
}
.cm-pro-feature.is-muted {
    color: #AEAEB2;
}
.cm-pro-icon {
    width: 1.1rem;
    height: 1.1rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
    color: #2B59FF;
}
.cm-pro-icon--muted { color: #C7C7CC; }
.cm-pro-sections-head {
    margin-bottom: 1.15rem;
}
.cm-pro-sections-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-pro-sections-title {
    margin: 0;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #1D1D1F;
}
.cm-pro-tile-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}
.cm-pro-tile {
    position: relative;
    min-height: 156px;
    padding: 1.1rem 1rem 1rem;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(0, 0, 0, 0.06);
    box-shadow: 0 2px 12px rgba(15, 23, 42, 0.04);
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s ease, border-color 0.25s ease;
}
.cm-pro-tile:not(.is-locked):hover {
    transform: translateY(-4px) scale(1.01);
    border-color: rgba(43, 89, 255, 0.18);
    box-shadow: 0 16px 40px rgba(43, 89, 255, 0.1);
}
.cm-pro-tile-icon {
    width: 2rem;
    height: 2rem;
    display: grid;
    place-items: center;
    margin-bottom: 0.75rem;
    border-radius: 10px;
    color: #2B59FF;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid rgba(191, 219, 254, 0.8);
}
.cm-pro-tile-icon svg {
    width: 1.1rem;
    height: 1.1rem;
}
.cm-pro-tile-num {
    margin: 0 0 0.2rem;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-pro-tile-title {
    margin: 0 0 0.35rem;
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #1D1D1F;
    line-height: 1.3;
}
.cm-pro-tile-sub {
    margin: 0;
    font-size: 0.74rem;
    line-height: 1.45;
    color: #6E6E73;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.cm-pro-tile.is-locked .cm-pro-tile-title,
.cm-pro-tile.is-locked .cm-pro-tile-num,
.cm-pro-tile.is-locked .cm-pro-tile-icon {
    filter: blur(3px);
    opacity: 0.55;
    user-select: none;
}
.cm-pro-tile-preview {
    display: grid;
    gap: 0.35rem;
    margin-top: 0.25rem;
    filter: blur(4px);
    opacity: 0.45;
}
.cm-pro-tile-preview span {
    display: block;
    height: 0.45rem;
    border-radius: 999px;
    background: linear-gradient(90deg, #E5E5EA, #D1D1D6);
}
.cm-pro-tile-preview span:nth-child(2) { width: 82%; }
.cm-pro-tile-preview span:nth-child(3) { width: 64%; }
.cm-pro-tile-lock {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(10px) saturate(160%);
    -webkit-backdrop-filter: blur(10px) saturate(160%);
}
.cm-pro-lock-icon {
    width: 1.35rem;
    height: 1.35rem;
    color: #2B59FF;
}
.cm-pro-tile-lock span {
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #1D4ED8;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(191, 219, 254, 0.9);
    box-shadow: 0 4px 14px rgba(43, 89, 255, 0.12);
}
.cm-pro-tile-shimmer {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        105deg,
        transparent 40%,
        rgba(255, 255, 255, 0.55) 50%,
        transparent 60%
    );
    transform: translateX(-120%);
    animation: cm-pro-shimmer 4s ease-in-out infinite;
    pointer-events: none;
}
@keyframes cm-pro-shimmer {
    0%, 100% { transform: translateX(-120%); }
    50% { transform: translateX(120%); }
}
.cm-pro-cta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    flex-wrap: wrap;
    margin-top: 2rem;
    padding: 1.65rem 2rem;
    border-radius: 24px;
    background: #1D1D1F;
    color: #F5F5F7;
    box-shadow:
        0 24px 64px rgba(0, 0, 0, 0.22),
        0 0 0 1px rgba(255, 255, 255, 0.06) inset;
}
.cm-pro-cta-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #86868B;
}
.cm-pro-cta-price {
    margin: 0 0 0.85rem;
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
    color: #FFFFFF;
}
.cm-pro-cta-price span {
    font-size: 1rem;
    font-weight: 500;
    color: #86868B;
    letter-spacing: 0;
}
.cm-pro-cta-points {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem 1.25rem;
}
.cm-pro-cta-points li {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.82rem;
    color: #D2D2D7;
}
.cm-pro-cta-points .cm-pro-icon {
    color: #64D2FF;
    width: 1rem;
    height: 1rem;
}
.cm-pro-cta-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 220px;
    padding: 0.95rem 1.75rem;
    border-radius: 999px;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: #1D1D1F !important;
    text-decoration: none !important;
    background: #FFFFFF;
    box-shadow: 0 8px 24px rgba(255, 255, 255, 0.12);
    transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
    white-space: nowrap;
}
.cm-pro-cta-btn:hover {
    transform: scale(1.03);
    background: #F5F5F7;
    box-shadow: 0 12px 32px rgba(255, 255, 255, 0.18);
    text-decoration: none !important;
}

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
.cm-score-story {
    display: flex;
    flex-direction: column;
    margin-top: 0.5rem;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.06) inset,
        0 24px 48px rgba(0, 0, 0, 0.18);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    overflow: hidden;
}
.cm-score-story-main {
    display: grid;
    grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
}
.cm-score-story-lead {
    display: flex;
    flex-direction: column;
    gap: 1.35rem;
    padding: 1.65rem 1.75rem;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-score-story-social {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
}
.cm-score-story-social .cm-avatar {
    width: 2.35rem;
    height: 2.35rem;
    border-color: rgba(255, 255, 255, 0.92);
}
.cm-score-story-social-text {
    margin: 0;
    flex: 1 1 220px;
    font-size: 0.88rem;
    line-height: 1.5;
    color: #CBD5E1;
    font-weight: 500;
}
.cm-score-story-values {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.65rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-score-value {
    padding: 0.85rem 0.65rem;
    border-radius: 14px;
    text-align: center;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-score-value strong {
    display: block;
    margin-bottom: 0.15rem;
    font-size: 0.92rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.01em;
}
.cm-score-value span {
    font-size: 0.74rem;
    color: #94A3B8;
}
.cm-score-story-aside {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 1.65rem 1.75rem;
    background: linear-gradient(165deg, rgba(43, 89, 255, 0.14) 0%, rgba(255, 255, 255, 0.03) 100%);
}
.cm-score-story-aside h3 {
    margin: 0 0 0.75rem;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}
.cm-score-story-aside p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.65;
    color: #94A3B8;
}
.cm-score-story-quote {
    margin: 0;
    padding: 1.35rem 1.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
    font-size: clamp(1.05rem, 2.5vw, 1.35rem);
    font-style: italic;
    font-weight: 500;
    letter-spacing: -0.01em;
    color: #CBD5E1;
    line-height: 1.5;
    background: rgba(0, 0, 0, 0.12);
}

/* Reviews */
.cm-reviews-trust {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    max-width: 640px;
    margin: -1rem auto 2rem;
    padding: 0.85rem 1.15rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid var(--cm-border);
    box-shadow: var(--cm-shadow);
}
.cm-reviews-trust .cm-avatar {
    width: 2.1rem;
    height: 2.1rem;
}
.cm-reviews-trust-text {
    flex: 1 1 220px;
    font-size: 0.84rem;
    font-weight: 500;
    color: #475569;
    text-align: center;
}
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
    gap: 0.65rem;
}
.cm-review-avatar {
    width: 2.35rem;
    height: 2.35rem;
    margin-left: 0;
    border-color: #FFFFFF;
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
@media (prefers-reduced-motion: reduce) {
    html.cm-reveal-ready .cm-reveal:not(.is-visible),
    .cm-animate-in {
        opacity: 1 !important;
        transform: none !important;
        animation: none !important;
    }
}

@media (max-width: 960px) {
    .cm-hero-grid,
    .cm-platform-engine-grid,
    .cm-platform-steps-track,
    .cm-pro-showcase,
    .cm-rpt-layout,
    .cm-brutal-grid,
    .cm-score-story-main { grid-template-columns: 1fr; }
    .cm-score-story-lead { border-right: none; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
    .cm-platform-steps-track::before { display: none; }
    .cm-site-stats-inner { flex-direction: column; align-items: flex-start; }
    .cm-site-stats-grid { grid-template-columns: 1fr 1fr; width: 100%; }
    .cm-eval-score-row { grid-template-columns: 1fr; justify-items: start; }
    .cm-eval-financials { grid-template-columns: 1fr 1fr; }
    .cm-eval-fin-divider { display: none; }
    .cm-reviews-grid,
    .cm-score-cards,
    .cm-section-cards { grid-template-columns: 1fr; }
    .cm-pro-tile-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cm-pro-cta { flex-direction: column; align-items: stretch; text-align: center; }
    .cm-pro-cta-points { justify-content: center; }
    .cm-pro-cta-btn { width: 100%; }
    .cm-rpt-nav {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.35rem;
        border-right: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }
    .cm-rpt-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .cm-rpt-panels { grid-template-columns: 1fr; }
    .cm-hero-stats-row { grid-template-columns: repeat(2, 1fr); }
    .cm-score-story-values { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
    .cm-section { padding: 3rem 0; }
    .cm-page { padding: 0 1rem; }
    .cm-live-stats { grid-template-columns: 1fr 1fr; }
    .cm-live-head { flex-direction: column; align-items: flex-start; }
    .cm-catalog-grid { grid-template-columns: repeat(2, 1fr); }
    .cm-platform-stats-grid { grid-template-columns: 1fr; }
    .cm-platform-hub { max-width: 320px; }
    .cm-platform-orbit-field { --orbit-radius: 118px !important; }
    .cm-platform-orbit { font-size: 0.62rem; padding: 0.35rem 0.55rem 0.35rem 0.45rem; }
    .cm-site-stats-grid { grid-template-columns: 1fr; }
    .cm-pro { padding-top: 3.5rem; padding-bottom: 4rem; }
    .cm-pro-tile-grid { grid-template-columns: 1fr; }
    .cm-pro-showcase { padding: 1rem; border-radius: 22px; }
    .cm-hero-screen {
        min-height: max(
            calc(100dvh - var(--ps-nav-h, 76px)),
            calc(100svh - var(--ps-nav-h, 76px))
        );
        padding: 3.5rem 1rem 4.5rem;
    }
    .cm-score-story { border-radius: 18px; }
    .cm-score-story-lead,
    .cm-score-story-aside { padding: 1.15rem; }
    .cm-score-story-quote { padding: 1.15rem; }
    .cm-reviews-trust {
        margin-top: -0.5rem;
        border-radius: 18px;
        padding: 0.85rem 1rem;
    }
    .cm-rpt { padding-top: 3.5rem; padding-bottom: 4rem; }
    .cm-rpt-window { border-radius: 18px; }
    .cm-rpt-nav { grid-template-columns: 1fr; }
    .cm-rpt-metrics { grid-template-columns: 1fr; }
    .cm-rpt-footer { padding: 0.75rem 1rem; }
    .cm-rpt-sample-link { width: 100%; justify-content: center; }
}
"""

AUTH_CM_CSS = """
/* Auth — Apple-inspired sign-in / sign-up */
.stApp:has(.cm-auth-page) .cm-auth-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    background:
        radial-gradient(ellipse 80% 55% at 15% -5%, rgba(43, 89, 255, 0.28) 0%, transparent 52%),
        radial-gradient(ellipse 65% 50% at 95% 15%, rgba(6, 182, 212, 0.12) 0%, transparent 48%),
        radial-gradient(ellipse 55% 45% at 50% 110%, rgba(43, 89, 255, 0.14) 0%, transparent 50%),
        linear-gradient(180deg, #060B18 0%, #0A1128 42%, #111827 100%);
}
.cm-auth-backdrop {
    display: none;
}
.cm-auth-backdrop::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.45;
}
.stApp:has(.cm-auth-page) {
    background: #060B18 !important;
    color: #F8FAFC !important;
}
.stApp:has(.cm-auth-page) .site-header,
.stApp:has(.cm-auth-page) .site-header__spacer {
    display: none !important;
}
.stApp:has(.cm-auth-page) section[data-testid="stMain"] > div {
    max-width: 100% !important;
    min-height: 100dvh;
    padding: clamp(1.75rem, 7vh, 3.25rem) 1.25rem 2rem !important;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    box-sizing: border-box;
}
.stApp:has(.cm-auth-page) .block-container {
    position: relative;
    z-index: 1;
    width: min(100%, 520px) !important;
    max-width: 520px !important;
    margin: 0 auto !important;
    padding: 2rem 2rem 1.75rem !important;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
        0 1px 0 rgba(255, 255, 255, 0.06) inset,
        0 24px 64px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-sizing: border-box;
}
.stApp:has(.cm-auth-page) .block-container > [data-testid="stVerticalBlock"] {
    gap: 0.9rem !important;
}
.stApp:has(.cm-auth-page) [data-testid="stMarkdownContainer"],
.stApp:has(.cm-auth-page) [data-testid="element-container"],
.stApp:has(.cm-auth-page) .stMarkdown {
    margin: 0 !important;
    padding: 0 !important;
}
.stApp:has(.cm-auth-page) [data-testid="stVerticalBlock"],
.stApp:has(.cm-auth-page) [data-testid="stForm"] {
    width: 100% !important;
    max-width: 100% !important;
}
.cm-auth-back {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.42rem 0.85rem;
    margin-bottom: 1.5rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #CBD5E1 !important;
    text-decoration: none !important;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: color 0.2s ease, background 0.2s ease, border-color 0.2s ease;
}
.cm-auth-back-inline {
    position: static;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
}
.cm-auth-back:hover {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.16);
    text-decoration: none !important;
}
.cm-auth-head {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1.35rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.cm-auth-brand-row {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.cm-auth-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 3.25rem;
    height: 3.25rem;
    margin: 0;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
}
.cm-auth-logo img {
    display: block;
    width: 2.15rem;
    height: 2.15rem;
    object-fit: contain;
}
.cm-auth-kicker {
    display: inline-flex;
    align-items: center;
    padding: 0.32rem 0.75rem;
    margin: 0;
    border-radius: 999px;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: #93C5FD;
    background: rgba(43, 89, 255, 0.12);
    border: 1px solid rgba(96, 165, 250, 0.22);
}
.cm-auth-title {
    margin: 0 0 0.5rem;
    font-size: clamp(1.45rem, 3vw, 1.75rem);
    font-weight: 700;
    letter-spacing: -0.035em;
    line-height: 1.12;
    color: #FFFFFF;
}
.cm-auth-title span {
    background: linear-gradient(135deg, #93C5FD 0%, #2B59FF 55%, #06B6D4 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.cm-auth-lead {
    margin: 0;
    font-size: 0.875rem;
    line-height: 1.55;
    color: #94A3B8;
}
.cm-auth-link {
    color: #FFFFFF !important;
    font-weight: 600;
    text-decoration: none !important;
    border-bottom: 1px solid rgba(147, 197, 253, 0.45);
    transition: border-color 0.15s ease, color 0.15s ease;
}
.cm-auth-link:hover {
    color: #93C5FD !important;
    border-bottom-color: #93C5FD;
}
.cm-auth-oauth-row {
    margin-bottom: 0.15rem;
}
.cm-auth-oauth {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.65rem;
    width: 100%;
    min-height: 2.75rem;
    padding: 0.65rem 1rem;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #F8FAFC !important;
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    text-decoration: none !important;
    box-sizing: border-box;
    transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.cm-auth-oauth:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.18);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    text-decoration: none !important;
}
.cm-auth-oauth-icon {
    flex-shrink: 0;
}
.cm-auth-divider {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.25rem 0 0.85rem;
}
.cm-auth-divider::before,
.cm-auth-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
}
.cm-auth-divider span {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #64748B;
}
.cm-auth-label {
    margin: 0 0 0.4rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: #94A3B8;
}
.cm-auth-legal {
    margin-top: 0.25rem;
    padding-top: 1.15rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
}
.cm-auth-legal p {
    margin: 0;
    font-size: 0.72rem;
    line-height: 1.6;
    color: #64748B;
}
.cm-auth-legal .cm-auth-link {
    color: #94A3B8 !important;
    font-weight: 500;
    border-bottom-color: rgba(148, 163, 184, 0.35);
}
.cm-auth-legal .cm-auth-link:hover {
    color: #FFFFFF !important;
    border-bottom-color: #FFFFFF;
}
@media (max-width: 640px) {
    .stApp:has(.cm-auth-page) section[data-testid="stMain"] > div {
        padding: 1.25rem 0.85rem 1.5rem !important;
    }
    .stApp:has(.cm-auth-page) .block-container {
        width: 100% !important;
        max-width: 100% !important;
        padding: 1.75rem 1.5rem 1.5rem !important;
        border-radius: 20px;
    }
    .cm-auth-head {
        margin-bottom: 1.25rem;
        padding-bottom: 1.15rem;
    }
}
"""
