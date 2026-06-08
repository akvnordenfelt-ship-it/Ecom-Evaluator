"""Marketing landing page."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, ReportSection
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
        "highlight": "Python-calculated ROI, scaling matrix, and GO/NO-GO verdict",
    },
    "marketing_teaser": {
        "icon": "🎯",
        "accent": "#8B5CF6",
        "accent_soft": "#F5F3FF",
        "highlight": "Channel fit, hook index and buyer persona",
    },
    "web_intelligence": {
        "icon": "🌐",
        "accent": "#0EA5E9",
        "accent_soft": "#F0F9FF",
        "highlight": "Live Amazon, AliExpress and Shopify intel",
    },
    "marketing_deep_dive": {
        "icon": "🚀",
        "accent": "#F59E0B",
        "accent_soft": "#FFFBEB",
        "highlight": "5 ad scripts, targeting and influencer DMs",
    },
}


def _page_divider(label: str, *, band: bool = False) -> None:
    band_class = " lp-page-divider--band" if band else ""
    st.markdown(
        f'<div class="lp-page-divider{band_class}"><span>{label}</span></div>',
        unsafe_allow_html=True,
    )


def _section_header(kicker: str, title: str, lead: str | None = None) -> None:
    lead_html = f'<p class="lp-section-header-lead">{lead}</p>' if lead else ""
    st.markdown(
        f"""
        <div class="lp-section-header">
            <p class="lp-section-header-kicker">{kicker}</p>
            <h2 class="lp-section-header-title">{title}</h2>
            {lead_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _section_card_html(section: ReportSection, *, badge: str = "Free") -> str:
    vis = SECTION_VISUALS[section.id]
    badge_class = "lp-free-pill" if badge == "Free" else "lp-premium-pill"
    return (
        f'<div class="lp-section-card" style="--accent:{vis["accent"]};--accent-soft:{vis["accent_soft"]}">'
        f'<div class="lp-section-card-top">'
        f'<span class="lp-section-icon">{vis["icon"]}</span>'
        f'<span class="{badge_class}">{badge}</span>'
        f"</div>"
        f'<p class="lp-section-num">Section {section.number}</p>'
        f'<p class="lp-section-title">{section.title}</p>'
        f'<p class="lp-section-body">{section.subtitle}</p>'
        f'<p class="lp-section-highlight">{vis["highlight"]}</p>'
        f"</div>"
    )


def _render_free_section_cards() -> None:
    free_sections = REPORT_SECTIONS[:3]
    col1, col2, col3 = st.columns(3)
    for col, section in zip((col1, col2, col3), free_sections, strict=True):
        with col:
            st.markdown(_section_card_html(section, badge="Free"), unsafe_allow_html=True)


def _premium_pricing_html() -> str:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    return (
        '<div class="lp-pricing-card lp-pricing-card--premium">'
        '<span class="lp-popular-pill">Most popular</span>'
        '<p class="lp-pricing-tier">Premium</p>'
        f'<p class="lp-pricing-price">${premium.price_usd_monthly}<span>/mo</span></p>'
        "<p class=\"lp-pricing-blurb\">Unlock live market intelligence when you're ready to source and price-check competitors.</p>"
        '<ul class="lp-pricing-features">'
        "<li>Section 4 — Marketing Viability Teaser</li>"
        "<li>Section 5 — Live web search and sourcing links</li>"
        "<li>Amazon and AliExpress competitor snapshots</li>"
        "<li>Actionable supplier URL matches</li>"
        f"<li>{premium.monthly_evaluations} evaluations / month</li>"
        "</ul></div>"
    )


def _pro_pricing_html() -> str:
    pro = PLAN_CONFIG[PlanTier.PRO]
    return (
        '<div class="lp-pricing-card lp-pricing-card--pro">'
        '<span class="lp-pro-pill">Full stack</span>'
        '<p class="lp-pricing-tier">Pro</p>'
        f'<p class="lp-pricing-price">${pro.price_usd_monthly}<span>/mo</span></p>'
        "<p class=\"lp-pricing-blurb\">Everything in Premium plus the ultimate marketing engine powered by Gemini 2.5 Pro.</p>"
        '<ul class="lp-pricing-features">'
        "<li>All Premium features included</li>"
        "<li>Section 6 — Ultimate marketing blueprint</li>"
        "<li>5 TikTok/Reels ad scripts with visual cues</li>"
        "<li>Precision Meta and TikTok targeting stacks</li>"
        f"<li>{pro.monthly_evaluations} evaluations / month</li>"
        "</ul></div>"
    )


def _step_card_html(number: int, title: str, body: str) -> str:
    return (
        f'<div class="lp-step-card">'
        f'<span class="lp-step-num">{number}</span>'
        f'<p class="lp-step-title">{title}</p>'
        f'<p class="lp-step-body">{body}</p>'
        f"</div>"
    )


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
                    <span class="lp-hero-badge">~30 sec analysis</span>
                    <span class="lp-hero-badge">3 sections free</span>
                    <span class="lp-hero-badge">Gemini 2.5 Flash</span>
                    <span class="lp-hero-badge">No credit card</span>
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

    _page_divider("At a glance")

    st.markdown(
        """
        <div class="lp-value-grid">
            <div class="lp-value-tile">
                <span class="lp-value-icon">⚡</span>
                <p class="lp-value-title">~30 seconds</p>
                <p class="lp-value-desc">From upload to your full 4-section free report</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">📋</span>
                <p class="lp-value-title">3 sections free</p>
                <p class="lp-value-desc">Profile, red flags, and margin matrix with verdict</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">💳</span>
                <p class="lp-value-title">$0 to start</p>
                <p class="lp-value-desc">One free evaluation — no credit card required</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">📊</span>
                <p class="lp-value-title">5 scored metrics</p>
                <p class="lp-value-desc">Saturation, velocity, logistics, seasonality, and brandability</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _page_divider("Free tier", band=True)
    _section_header(
        "What you get free",
        "Three sections that show the ceiling — not the floor",
        "We designed the free tier to feel premium. Real scores, real red flags, real math, "
        "and a Python-calculated verdict — enough to decide if this product deserves your money.",
    )
    _render_free_section_cards()
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    _page_divider("Paid tiers", band=True)
    _section_header(
        "When you're ready to execute",
        "Unlock marketing intel, live search, and ad firepower",
        "Sections 4–6 are for operators who've validated the opportunity and need channel fit, "
        "sourcing links, competitor tracking, and ready-to-film ad scripts.",
    )
    prem_col, pro_col = st.columns(2)
    with prem_col:
        st.markdown(_premium_pricing_html(), unsafe_allow_html=True)
    with pro_col:
        st.markdown(_pro_pricing_html(), unsafe_allow_html=True)
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    _page_divider("Process", band=True)
    _section_header("How it works", "From product photo to go/no-go in three steps")
    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown(
            _step_card_html(
                1,
                "Upload and input",
                "Add your product image, cost, sell price, dimensions, and a short description. Takes 60 seconds.",
            ),
            unsafe_allow_html=True,
        )
    with step2:
        st.markdown(
            _step_card_html(
                2,
                "AI evaluates",
                "Gemini 2.5 Flash analyzes your inputs — profile, risks, marketing fit — with no expensive web APIs on free.",
            ),
            unsafe_allow_html=True,
        )
    with step3:
        st.markdown(
            _step_card_html(
                3,
                "Decide and scale",
                "Read your margin matrix, red flags, and overall score. Upgrade when you need live intel and ad scripts.",
            ),
            unsafe_allow_html=True,
        )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    _page_divider("Sample output", band=True)
    _section_header("Inside your report", "A snapshot of what you'll see")
    st.markdown(
        """
        <div class="lp-preview-card">
            <div class="lp-preview-left">
                <p class="lp-preview-label">Overall product score</p>
                <p class="lp-preview-score">74<span>/100</span></p>
                <p class="lp-preview-verdict">Proceed with caution</p>
            </div>
            <div class="lp-preview-right">
                <p class="lp-preview-metric"><span>Market saturation</span><span class="lp-bar"><i style="width:62%"></i></span><strong>62</strong></p>
                <p class="lp-preview-metric"><span>Marketing velocity</span><span class="lp-bar"><i style="width:81%"></i></span><strong>81</strong></p>
                <p class="lp-preview-metric"><span>Logistics and margin</span><span class="lp-bar"><i style="width:88%"></i></span><strong>88</strong></p>
                <p class="lp-preview-metric"><span>Seasonality</span><span class="lp-bar"><i style="width:55%"></i></span><strong>55</strong></p>
                <p class="lp-preview-metric"><span>Brandability</span><span class="lp-bar"><i style="width:70%"></i></span><strong>70</strong></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    _page_divider("Plans", band=True)
    _section_header("Compare plans", "Pick the tier that matches your stage")
    st.markdown(
        """
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
                    <tr><td>Sections 1–3 (profile, risks, margin + verdict)</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Weighted 5-metric score (Python-calculated)</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Marketing Viability Teaser (Section 4)</td><td>—</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Live web search and sourcing (Section 5)</td><td>—</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Marketing blueprint (Section 6)</td><td>—</td><td>—</td><td>Yes</td></tr>
                    <tr><td>Evaluations / month</td><td>1</td><td>20</td><td>100</td></tr>
                    <tr><td>Price</td><td>$0</td><td>$29/mo</td><td>$79/mo</td></tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    _page_divider("FAQ", band=True)
    with st.expander("Why no web search on the free tier?"):
        st.markdown(
            "Web search APIs cost money on every evaluation. We keep the free tier input-only so "
            "you still get a **premium-quality** profile, risk analysis, and margin math — without us "
            "burning budget on tire-kickers. When you're serious, Premium unlocks live competitor intel."
        )
    with st.expander("What makes the free report 'ceiling quality'?"):
        st.markdown(
            "Sections 1–3 use the same structured scoring framework as paid tiers: a weighted overall gauge, "
            "five core metrics, Shark Tank red flags, and a full Python-calculated scaling matrix with verdict. "
            "You're not getting a dumbed-down teaser — you're getting the decision layer."
        )
    with st.expander("When should I upgrade to Pro?"):
        st.markdown(
            "Upgrade to **Premium** when you need sourcing links and live competitor prices. "
            "Go **Pro** when you're ready to launch ads and need full TikTok/Reels scripts, "
            "targeting stacks, and influencer outreach templates."
        )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

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
