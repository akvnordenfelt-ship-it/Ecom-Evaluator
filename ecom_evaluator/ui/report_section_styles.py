"""Premium report layout — Sections 1 & 2 (mockup-driven)."""

REPORT_S12_CSS = """
/* ── Shared section shell ─────────────────────────────────────────────────── */
.rpt-section {
    margin: 1.75rem 0 2rem;
}
.rpt-section-layout {
    display: grid;
    grid-template-columns: minmax(210px, 250px) minmax(0, 1fr);
    gap: 1.35rem;
    align-items: start;
}
.rpt-section-rail {
    position: sticky;
    top: calc(var(--ps-nav-h, 76px) + 0.75rem);
}
.rpt-section-kicker {
    display: inline-block;
    margin: 0 0 0.5rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #FB923C;
}
.rpt-section-title {
    margin: 0 0 0.55rem;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.15;
    color: var(--ws-section-heading, #0F172A);
}
.rpt-section-lead {
    margin: 0 0 1rem;
    font-size: 0.84rem;
    line-height: 1.55;
    color: var(--ws-text-muted, #64748B);
}
.rpt-rail-note {
    border-radius: 14px;
    padding: 0.9rem 0.95rem;
    background: var(--ws-surface, rgba(255, 255, 255, 0.04));
    border: 1px solid var(--ws-surface-border, rgba(255, 255, 255, 0.08));
}
.rpt-rail-note-kicker {
    margin: 0 0 0.35rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ws-text-faint, #94A3B8);
}
.rpt-rail-note p {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.5;
    color: var(--ws-text-muted, #94A3B8);
}
.rpt-rail-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1rem;
    padding: 0.45rem 0.7rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #FCA5A5;
    background: rgba(239, 68, 68, 0.12);
    border: 1px solid rgba(248, 113, 113, 0.28);
}
.rpt-section-body {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    min-width: 0;
}
.rpt-card {
    border-radius: 16px;
    padding: 1.1rem 1.15rem;
    background: var(--ws-surface, #FFFFFF);
    border: 1px solid var(--ws-surface-border, #E2E8F0);
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.04) inset;
}
.rpt-card-title {
    margin: 0 0 0.75rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ws-text-faint, #64748B);
}

/* ── Section 1 grid ───────────────────────────────────────────────────────── */
.rpt-s1-top {
    display: grid;
    grid-template-columns: minmax(220px, 1fr) minmax(260px, 1.35fr);
    gap: 0.85rem;
}
.rpt-gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100%;
}
.rpt-gauge {
    position: relative;
    width: min(100%, 220px);
    aspect-ratio: 2 / 1.05;
    overflow: hidden;
}
.rpt-gauge-arc {
    position: absolute;
    inset: 0;
    border-radius: 220px 220px 0 0;
    background:
        radial-gradient(circle at 50% 100%, var(--ws-surface, #0F172A) 58%, transparent 59%),
        conic-gradient(
            from 180deg at 50% 100%,
            #EF4444 0deg,
            #F59E0B 72deg,
            #22C55E 144deg,
            #22C55E 180deg,
            transparent 180deg
        );
    mask: radial-gradient(circle at 50% 100%, transparent 54%, #000 55%);
    -webkit-mask: radial-gradient(circle at 50% 100%, transparent 54%, #000 55%);
}
.rpt-gauge-needle {
    position: absolute;
    left: 50%;
    bottom: 8%;
    width: 3px;
    height: 42%;
    background: #F8FAFC;
    border-radius: 999px;
    transform-origin: 50% 100%;
    transform: translateX(-50%) rotate(var(--needle-deg, -90deg));
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.35);
}
.rpt-gauge-hub {
    position: absolute;
    left: 50%;
    bottom: 6%;
    width: 12px;
    height: 12px;
    border-radius: 999px;
    background: #F8FAFC;
    transform: translateX(-50%);
    box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.35);
}
.rpt-gauge-readout {
    position: absolute;
    left: 50%;
    bottom: 22%;
    transform: translateX(-50%);
    text-align: center;
    width: 100%;
}
.rpt-gauge-value {
    display: block;
    font-size: 2.35rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
    color: var(--ws-text, #F8FAFC);
}
.rpt-gauge-verdict {
    display: inline-block;
    margin-top: 0.35rem;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.rpt-gauge-verdict--go { color: #34D399; background: rgba(52, 211, 153, 0.14); }
.rpt-gauge-verdict--caution { color: #FBBF24; background: rgba(251, 191, 36, 0.14); }
.rpt-gauge-verdict--risk { color: #FB923C; background: rgba(251, 146, 60, 0.14); }
.rpt-gauge-verdict--walk { color: #F87171; background: rgba(248, 113, 113, 0.14); }
.rpt-gauge-caption {
    margin: 0.65rem 0 0;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--ws-text-muted, #94A3B8);
    text-align: center;
}

.rpt-metric-list {
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}
.rpt-metric-row {
    display: grid;
    grid-template-columns: 1.4rem minmax(0, 1fr) minmax(0, 2fr) auto;
    gap: 0.55rem;
    align-items: center;
}
.rpt-metric-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.4rem;
    height: 1.4rem;
    color: var(--ws-text-muted, #94A3B8);
}
.rpt-metric-icon svg {
    width: 1rem;
    height: 1rem;
}
.rpt-metric-label {
    margin: 0;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--ws-text, #E2E8F0);
    line-height: 1.3;
}
.rpt-metric-track {
    height: 0.42rem;
    border-radius: 999px;
    background: rgba(148, 163, 184, 0.18);
    overflow: hidden;
}
.rpt-metric-fill {
    height: 100%;
    border-radius: inherit;
    background: var(--metric-color, #22C55E);
}
.rpt-metric-score {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--ws-text-muted, #CBD5E1);
    white-space: nowrap;
}

.rpt-glance-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.55rem 1.25rem;
}
.rpt-glance-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 0;
}
.rpt-glance-key {
    margin: 0;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--ws-text-faint, #64748B);
}
.rpt-glance-val {
    margin: 0;
    font-size: 0.84rem;
    line-height: 1.45;
    color: var(--ws-text, #F8FAFC);
}

.rpt-s1-bottom {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.85rem;
}
.rpt-verdict-box,
.rpt-why-box {
    border-radius: 16px;
    padding: 1rem 1.1rem;
    border: 1px solid var(--ws-surface-border, rgba(255, 255, 255, 0.08));
    background: var(--ws-card-bg, rgba(255, 255, 255, 0.03));
}
.rpt-verdict-box-head,
.rpt-why-box-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.55rem;
}
.rpt-verdict-box-head span,
.rpt-why-box-head span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.65rem;
    height: 1.65rem;
    border-radius: 999px;
    font-size: 0.9rem;
    font-weight: 800;
}
.rpt-verdict-box--nogo .rpt-verdict-box-head span {
    color: #F87171;
    background: rgba(248, 113, 113, 0.14);
}
.rpt-verdict-box--go .rpt-verdict-box-head span {
    color: #34D399;
    background: rgba(52, 211, 153, 0.14);
}
.rpt-verdict-box--caution .rpt-verdict-box-head span {
    color: #FBBF24;
    background: rgba(251, 191, 36, 0.14);
}
.rpt-verdict-box-title,
.rpt-why-box-title {
    margin: 0;
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--ws-text, #F8FAFC);
}
.rpt-verdict-box-copy,
.rpt-why-box li {
    margin: 0;
    font-size: 0.82rem;
    line-height: 1.5;
    color: var(--ws-text-muted, #94A3B8);
}
.rpt-why-list {
    margin: 0;
    padding: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
}
.rpt-why-list li {
    display: flex;
    align-items: flex-start;
    gap: 0.45rem;
}
.rpt-why-list li::before {
    content: "✕";
    flex-shrink: 0;
    margin-top: 0.05rem;
    color: #F87171;
    font-size: 0.72rem;
    font-weight: 800;
}
.rpt-why-list--positive li::before {
    content: "✓";
    color: #34D399;
}

/* ── Section 2 layout ─────────────────────────────────────────────────────── */
.rpt-s2-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(220px, 0.85fr);
    gap: 0.85rem;
}
.rpt-flag-list {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
}
.rpt-flag-row {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 0.7rem;
    align-items: start;
    padding: 0.85rem 0.9rem;
    border-radius: 14px;
    background: rgba(239, 68, 68, 0.06);
    border: 1px solid rgba(248, 113, 113, 0.16);
}
.stApp:has(.cm-workspace-mode-bright) .rpt-flag-row,
.stApp:has(.cm-workspace-mode-white) .rpt-flag-row {
    background: #FEF2F2;
    border-color: #FECACA;
}
.rpt-flag-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.75rem;
    height: 1.75rem;
    border-radius: 10px;
    color: #F87171;
    background: rgba(248, 113, 113, 0.14);
    font-size: 0.95rem;
    line-height: 1;
}
.rpt-flag-title {
    margin: 0 0 0.2rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ws-text, #F8FAFC);
    line-height: 1.35;
}
.rpt-flag-desc {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.45;
    color: var(--ws-text-muted, #94A3B8);
}
.rpt-flag-impact {
    align-self: center;
    padding: 0.2rem 0.5rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    white-space: nowrap;
}
.rpt-flag-impact--severe { color: #FCA5A5; background: rgba(239, 68, 68, 0.18); }
.rpt-flag-impact--high { color: #FDBA74; background: rgba(249, 115, 22, 0.16); }
.rpt-flag-impact--moderate { color: #FDE68A; background: rgba(234, 179, 8, 0.14); }

.rpt-risk-panel {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.rpt-risk-ring-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 1.15rem 1rem 1rem;
}
.rpt-risk-ring {
    --risk-pct: 0.5;
    position: relative;
    width: 132px;
    height: 132px;
    border-radius: 999px;
    background: conic-gradient(
        #EF4444 0deg,
        #EF4444 calc(var(--risk-pct) * 360deg),
        rgba(148, 163, 184, 0.18) calc(var(--risk-pct) * 360deg),
        rgba(148, 163, 184, 0.18) 360deg
    );
    display: grid;
    place-items: center;
}
.rpt-risk-ring::before {
    content: "";
    width: 78%;
    height: 78%;
    border-radius: inherit;
    background: var(--ws-card-bg, #131D32);
    border: 1px solid var(--ws-surface-border, rgba(255, 255, 255, 0.08));
}
.rpt-risk-ring-readout {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.1rem;
}
.rpt-risk-ring-value {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ws-text, #F8FAFC);
    line-height: 1;
}
.rpt-risk-ring-value span {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--ws-text-muted, #94A3B8);
}
.rpt-risk-ring-label {
    margin: 0.65rem 0 0;
    font-size: 0.88rem;
    font-weight: 700;
    color: #F87171;
}
.rpt-risk-ring-caption {
    margin: 0.15rem 0 0;
    font-size: 0.72rem;
    color: var(--ws-text-muted, #94A3B8);
}

.rpt-invest-box {
    border-radius: 14px;
    padding: 0.95rem 1rem;
    border: 1px solid var(--ws-surface-border, rgba(255, 255, 255, 0.08));
    background: var(--ws-card-bg, rgba(255, 255, 255, 0.03));
}
.rpt-invest-box-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.35rem;
}
.rpt-invest-box-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.55rem;
    height: 1.55rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
}
.rpt-invest-box--no .rpt-invest-box-icon {
    color: #F87171;
    background: rgba(248, 113, 113, 0.14);
}
.rpt-invest-box--yes .rpt-invest-box-icon {
    color: #34D399;
    background: rgba(52, 211, 153, 0.14);
}
.rpt-invest-box-title {
    margin: 0;
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--ws-text, #F8FAFC);
}
.rpt-invest-box-copy {
    margin: 0;
    font-size: 0.78rem;
    line-height: 1.45;
    color: var(--ws-text-muted, #94A3B8);
}

@media (max-width: 960px) {
    .rpt-section-layout,
    .rpt-s1-top,
    .rpt-s1-bottom,
    .rpt-s2-grid {
        grid-template-columns: 1fr;
    }
    .rpt-section-rail {
        position: static;
    }
    .rpt-metric-row {
        grid-template-columns: 1.4rem minmax(0, 1fr) auto;
    }
    .rpt-metric-track {
        grid-column: 2 / -1;
    }
}
"""
