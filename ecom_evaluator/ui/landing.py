"""Marketing landing page."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS
from ecom_evaluator.ui.subscription import enter_tool_view

SECTION_VISUALS: dict[str, dict[str, str]] = {
    "product_profile": {
        "icon": "📦",
        "accent": "#3B82F6",
        "accent_soft": "#EFF6FF",
        "highlight": "Overall score + 5 core e-commerce metrics",
    },
    "red_flags": {
        "icon": "🚨",
        "accent": "#EF4444",
        "accent_soft": "#FEF2F2",
        "highlight": "Brutal Shark Tank-style deal-breakers",
    },
    "margin_matrix": {
        "icon": "📊",
        "accent": "#10B981",
        "accent_soft": "#ECFDF5",
        "highlight": "Python-calculated ROI & scaling projections",
    },
    "marketing_teaser": {
        "icon": "🎯",
        "accent": "#8B5CF6",
        "accent_soft": "#F5F3FF",
        "highlight": "Channel fit, hook index & buyer persona",
    },
    "web_intelligence": {
        "icon": "🌐",
        "accent": "#0EA5E9",
        "accent_soft": "#F0F9FF",
        "highlight": "Live Amazon, AliExpress & Shopify intel",
    },
    "marketing_deep_dive": {
        "icon": "🚀",
        "accent": "#F59E0B",
        "accent_soft": "#FFFBEB",
        "highlight": "5× ad scripts, targeting & influencer DMs",
    },
}


def _render_free_section_cards() -> str:
    cards: list[str] = []
    for section in REPORT_SECTIONS[:4]:
        vis = SECTION_VISUALS[section.id]
        cards.append(
            f"""
            <div class="lp-section-card" style="--accent:{vis['accent']};--accent-soft:{vis['accent_soft']}">
                <div class="lp-section-card-top">
                    <span class="lp-section-icon">{vis['icon']}</span>
                    <span class="lp-free-pill">Free</span>
                </div>
                <p class="lp-section-num">Section {section.number}</p>
                <p class="lp-section-title">{section.title}</p>
                <p class="lp-section-body">{section.subtitle}</p>
                <p class="lp-section-highlight">{vis['highlight']}</p>
            </div>
            """
        )
    return f'<div class="lp-section-grid">{"".join(cards)}</div>'


def _render_pricing_cards() -> str:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    pro = PLAN_CONFIG[PlanTier.PRO]
    return f"""
    <div class="lp-pricing-grid">
        <div class="lp-pricing-card lp-pricing-card--premium">
            <span class="lp-popular-pill">Most popular</span>
            <p class="lp-pricing-tier">Premium</p>
            <p class="lp-pricing-price">${premium.price_usd_monthly}<span>/mo</span></p>
            <p class="lp-pricing-blurb">Unlock live market intelligence when you're ready to source and price-check competitors.</p>
            <ul class="lp-pricing-features">
                <li>🌐 Section 5 — Live web search &amp; sourcing links</li>
                <li>🔍 Amazon &amp; AliExpress competitor snapshots</li>
                <li>🔗 Actionable supplier URL matches</li>
                <li>{premium.monthly_evaluations} evaluations / month</li>
            </ul>
        </div>
        <div class="lp-pricing-card lp-pricing-card--pro">
            <span class="lp-pro-pill">Full stack</span>
            <p class="lp-pricing-tier">Pro</p>
            <p class="lp-pricing-price">${pro.price_usd_monthly}<span>/mo</span></p>
            <p class="lp-pricing-blurb">Everything in Premium plus the ultimate marketing engine powered by Gemini 2.5 Pro.</p>
            <ul class="lp-pricing-features">
                <li>✅ All Premium features included</li>
                <li>🚀 Section 6 — Ultimate marketing blueprint</li>
                <li>🎬 5× TikTok/Reels ad scripts with visual cues</li>
                <li>🎯 Precision Meta &amp; TikTok targeting stacks</li>
                <li>{pro.monthly_evaluations} evaluations / month</li>
            </ul>
        </div>
    </div>
    """


def render_landing_page() -> None:
    st.markdown(
        """
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Know if your product can win — before you spend a dollar</h1>
                <p class="landing-lead">
                    Upload your product, enter your numbers, and get a ceiling-quality evaluation in ~30 seconds.
                    Free tier runs on Gemini 2.5 Flash — your inputs and image only. No web search. Near-zero cost.
                </p>
                <div class="lp-hero-badges">
                    <span class="lp-hero-badge">⚡ ~30 sec analysis</span>
                    <span class="lp-hero-badge">🆓 4 sections free</span>
                    <span class="lp-hero-badge">🤖 Gemini 2.5 Flash</span>
                    <span class="lp-hero-badge">🔒 No credit card</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, hero_cta, _ = st.columns([1, 1.4, 1])
    with hero_cta:
        if st.button("Run your free evaluation →", type="primary", use_container_width=True, key="landing_hero_cta"):
            enter_tool_view()
            st.rerun()

    st.markdown(
        """
        <div class="lp-stats-strip">
            <div class="lp-stat"><span class="lp-stat-value">6</span><span class="lp-stat-label">Report sections</span></div>
            <div class="lp-stat"><span class="lp-stat-value">4</span><span class="lp-stat-label">Free on signup</span></div>
            <div class="lp-stat"><span class="lp-stat-value">$0</span><span class="lp-stat-label">Free tier cost</span></div>
            <div class="lp-stat"><span class="lp-stat-value">5</span><span class="lp-stat-label">Core metrics scored</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">What you get free</p>
            <h2 class="lp-section-header-title">Four sections that show the ceiling — not the floor</h2>
            <p class="lp-section-header-lead">
                We designed the free tier to feel premium. Real scores, real red flags, real math —
                enough to decide if this product deserves your money.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(_render_free_section_cards(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">When you're ready to execute</p>
            <h2 class="lp-section-header-title">Unlock live intel &amp; marketing firepower</h2>
            <p class="lp-section-header-lead">
                Sections 5 and 6 are for operators who've validated the opportunity and need sourcing links,
                competitor tracking, and ready-to-film ad scripts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(_render_pricing_cards(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">How it works</p>
            <h2 class="lp-section-header-title">From product photo to go/no-go in three steps</h2>
        </div>
        <div class="lp-steps-grid">
            <div class="lp-step-card">
                <span class="lp-step-num">1</span>
                <p class="lp-step-title">Upload &amp; input</p>
                <p class="lp-step-body">Add your product image, cost, sell price, dimensions, and a short description. Takes 60 seconds.</p>
            </div>
            <div class="lp-step-card">
                <span class="lp-step-num">2</span>
                <p class="lp-step-title">AI evaluates</p>
                <p class="lp-step-body">Gemini 2.5 Flash analyzes your inputs — profile, risks, marketing fit — with no expensive web APIs on free.</p>
            </div>
            <div class="lp-step-card">
                <span class="lp-step-num">3</span>
                <p class="lp-step-title">Decide &amp; scale</p>
                <p class="lp-step-body">Read your margin matrix, red flags, and overall score. Upgrade when you need live intel and ad scripts.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">Inside your report</p>
            <h2 class="lp-section-header-title">A snapshot of what you'll see</h2>
        </div>
        <div class="lp-preview-card">
            <div class="lp-preview-left">
                <p class="lp-preview-label">Overall product score</p>
                <p class="lp-preview-score">74<span>/100</span></p>
                <p class="lp-preview-verdict">Proceed with caution</p>
            </div>
            <div class="lp-preview-right">
                <p class="lp-preview-metric"><span>Market saturation</span><span class="lp-bar"><i style="width:62%"></i></span><strong>62</strong></p>
                <p class="lp-preview-metric"><span>Marketing velocity</span><span class="lp-bar"><i style="width:81%"></i></span><strong>81</strong></p>
                <p class="lp-preview-metric"><span>Logistics &amp; margin</span><span class="lp-bar"><i style="width:88%"></i></span><strong>88</strong></p>
                <p class="lp-preview-metric"><span>Seasonality</span><span class="lp-bar"><i style="width:55%"></i></span><strong>55</strong></p>
                <p class="lp-preview-metric"><span>Brandability</span><span class="lp-bar"><i style="width:70%"></i></span><strong>70</strong></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">Compare plans</p>
            <h2 class="lp-section-header-title">Pick the tier that matches your stage</h2>
        </div>
        <div class="lp-compare-wrap">
            <table class="lp-compare-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Free</th>
                        <th>Premium</th>
                        <th>Pro</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Sections 1–4 (profile, risks, margin, teaser)</td><td>✅</td><td>✅</td><td>✅</td></tr>
                    <tr><td>Gemini 2.5 Flash analysis</td><td>✅</td><td>✅</td><td>✅</td></tr>
                    <tr><td>Python margin &amp; scaling matrix</td><td>✅</td><td>✅</td><td>✅</td></tr>
                    <tr><td>Live web search &amp; sourcing (Section 5)</td><td>—</td><td>✅</td><td>✅</td></tr>
                    <tr><td>Marketing blueprint (Section 6)</td><td>—</td><td>—</td><td>✅</td></tr>
                    <tr><td>Evaluations / month</td><td>1</td><td>20</td><td>100</td></tr>
                    <tr><td>Price</td><td>$0</td><td>$29/mo</td><td>$79/mo</td></tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("❓ Why no web search on the free tier?"):
        st.markdown(
            "Web search APIs cost money on every evaluation. We keep the free tier input-only so "
            "you still get a **premium-quality** profile, risk analysis, and margin math — without us "
            "burning budget on tire-kickers. When you're serious, Premium unlocks live competitor intel."
        )
    with st.expander("❓ What makes the free report 'ceiling quality'?"):
        st.markdown(
            "Sections 1–4 use the same structured scoring framework as paid tiers: an overall gauge, "
            "five weighted metrics, Shark Tank red flags, and a full Python-calculated scaling matrix. "
            "You're not getting a dumbed-down teaser — you're getting the decision layer."
        )
    with st.expander("❓ When should I upgrade to Pro?"):
        st.markdown(
            "Upgrade to **Premium** when you need sourcing links and live competitor prices. "
            "Go **Pro** when you're ready to launch ads and need full TikTok/Reels scripts, "
            "targeting stacks, and influencer outreach templates."
        )

    st.markdown(
        """
        <div class="lp-final-cta">
            <p class="lp-final-kicker">Ready to evaluate?</p>
            <h2 class="lp-final-title">Your first evaluation is free — no credit card required</h2>
            <p class="lp-final-lead">Upload a product image, enter your numbers, and get your score in about 30 seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, bottom_cta, _ = st.columns([1, 1.4, 1])
    with bottom_cta:
        if st.button("Start free evaluation →", type="primary", use_container_width=True, key="landing_bottom_cta"):
            enter_tool_view()
            st.rerun()

    st.markdown(
        '<p class="landing-footnote">ProductScore · Gemini 2.5 Flash · Built for e-commerce operators</p>',
        unsafe_allow_html=True,
    )
