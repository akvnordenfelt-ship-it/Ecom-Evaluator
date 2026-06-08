"""Marketing landing page."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, ReportSection
from ecom_evaluator.ui.subscription import enter_tool_view, request_free_evaluation

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
    free_sections = REPORT_SECTIONS[:2]
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(_section_card_html(free_sections[0], badge="Free"), unsafe_allow_html=True)
    with col_right:
        st.markdown(_section_card_html(free_sections[1], badge="Free"), unsafe_allow_html=True)


def _premium_pricing_html() -> str:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    return (
        '<div class="lp-pricing-card lp-pricing-card--premium lp-pricing-card--solo">'
        '<span class="lp-popular-pill">Everything included</span>'
        '<p class="lp-pricing-tier">Premium</p>'
        f'<p class="lp-pricing-price">${premium.price_usd_monthly}<span>/mo</span></p>'
        "<p class=\"lp-pricing-blurb\">One plan. Full stack. Unlimited evaluations. "
        "Unlock every section — financial verdict, marketing blueprint, live web intel, and 5× video scripts — "
        "powered by our most advanced commercial AI engine.</p>"
        '<ul class="lp-pricing-features">'
        "<li>Section 3 — Financial matrix &amp; GO/NO-GO verdict</li>"
        "<li>Section 4 — Marketing viability &amp; targeting blueprint</li>"
        "<li>Section 5 — Live web intelligence &amp; sourcing links</li>"
        "<li>Section 6 — Ultimate 5× video content engine</li>"
        "<li>Unlimited evaluations</li>"
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


def render_landing_hero() -> None:
    st.markdown(
        f"""
        <div class="landing-wrap">
            <div class="landing-hero">
                <p class="landing-kicker">Shark Tank-grade analysis</p>
                <h1 class="landing-title">Know if your product can win — before you spend a dollar</h1>
                <p class="landing-lead">
                    Upload your product, enter your numbers, and get a sharp profile + red-flag analysis in ~30 seconds.
                    Free preview covers Sections 1–2. Upgrade to Premium for the financial verdict and full execution stack.
                </p>
                <div class="lp-hero-badges">
                    <span class="lp-hero-badge">~30 sec preview</span>
                    <span class="lp-hero-badge">{FREE_EVALUATIONS_PER_ACCOUNT} free evals / account</span>
                    <span class="lp-hero-badge">2 sections free</span>
                    <span class="lp-hero-badge">Premium · $29/mo</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_landing_at_a_glance() -> None:
    _page_divider("At a glance")

    st.markdown(
        f"""
        <div class="lp-value-grid">
            <div class="lp-value-tile">
                <span class="lp-value-icon">⚡</span>
                <p class="lp-value-title">~30 seconds</p>
                <p class="lp-value-desc">From upload to your free profile + red-flag preview</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">📋</span>
                <p class="lp-value-title">2 sections free</p>
                <p class="lp-value-desc">Product profile, core metrics, and Shark Tank red flags</p>
            </div>
            <div class="lp-value-tile">
                <span class="lp-value-icon">💳</span>
                <p class="lp-value-title">$0 to start</p>
                <p class="lp-value-desc">{FREE_EVALUATIONS_PER_ACCOUNT} free evaluations per account — no credit card required</p>
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


def _scroll_to_anchor_if_needed() -> None:
    anchor = st.session_state.pop("landing_anchor", None)
    if not anchor:
        return
    components.html(
        f"""
        <script>
        (function () {{
            const doc = window.parent.document;
            const el = doc.getElementById("section-{anchor}");
            if (el) {{
                el.scrollIntoView({{ behavior: "smooth", block: "start" }});
            }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def render_landing_body() -> None:
    _page_divider("Free tier", band=True)
    _section_header(
        "What you get free",
        "Two sections designed to hook you — then Premium delivers the verdict",
        "Free users get a real profile score and brutal red-flag analysis — enough to feel the opportunity "
        "and the risk. The financial GO/NO-GO verdict and execution stack unlock on Premium.",
    )
    _render_free_section_cards()
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    st.markdown('<div id="section-pricing"></div>', unsafe_allow_html=True)
    _page_divider("Premium", band=True)
    _section_header(
        "Unlock the full report",
        "One plan. Everything included. $29/month.",
        "Sections 3–6 cover the financial verdict, marketing blueprint, live competitor intel, "
        "and five ready-to-shoot video scripts — plus unlimited evaluations.",
    )
    _, premium_col, _ = st.columns([0.35, 1.3, 0.35])
    with premium_col:
        st.markdown(_premium_pricing_html(), unsafe_allow_html=True)
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
                "Our AI analyzes your inputs — profile and risks on free, full stack on Premium.",
            ),
            unsafe_allow_html=True,
        )
    with step3:
        st.markdown(
            _step_card_html(
                3,
                "Decide and scale",
                "Read red flags free. Upgrade for the GO/NO-GO verdict, sourcing intel, and ad scripts.",
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
    _section_header("Compare plans", "Free preview vs Premium full stack")
    st.markdown(
        f"""
        <div class="lp-compare-wrap">
            <table class="lp-compare-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Free</th>
                        <th>Premium</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Sections 1–2 (profile + red flags)</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Weighted 5-metric score</td><td>Yes</td><td>Yes</td></tr>
                    <tr><td>Financial matrix &amp; GO/NO-GO verdict (Section 3)</td><td>—</td><td>Yes</td></tr>
                    <tr><td>Marketing blueprint (Section 4)</td><td>—</td><td>Yes</td></tr>
                    <tr><td>Live web intel &amp; sourcing (Section 5)</td><td>—</td><td>Yes</td></tr>
                    <tr><td>5× video script engine (Section 6)</td><td>—</td><td>Yes</td></tr>
                    <tr><td>Evaluations</td><td>{FREE_EVALUATIONS_PER_ACCOUNT} free / account</td><td>Unlimited</td></tr>
                    <tr><td>Price</td><td>$0</td><td>$29/mo</td></tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)

    st.markdown('<div id="section-resources"></div>', unsafe_allow_html=True)
    _page_divider("FAQ", band=True)
    with st.expander("Why no web search on the free tier?"):
        st.markdown(
            "Web search APIs cost money on every evaluation. We keep the free tier input-only so "
            "you still get a **premium-quality** profile, risk analysis, and margin math — without us "
            "burning budget on tire-kickers. When you're serious, Premium unlocks live competitor intel."
        )
    with st.expander("What makes the free report 'ceiling quality'?"):
        st.markdown(
            "The free preview gives you Sections 1–2: a weighted product score and Shark Tank-grade red flags. "
            "Premium unlocks the financial GO/NO-GO verdict plus the full execution stack."
        )
    with st.expander("When should I upgrade to Premium?"):
        st.markdown(
            "Upgrade when red flags have your attention and you need the math: margin stress-tests, "
            "final verdict, marketing blueprint, live competitor intel, and ready-to-film ad scripts."
        )
    st.markdown('<div class="lp-band-end"></div>', unsafe_allow_html=True)


def render_landing_final_cta(*, show_buttons: bool = True) -> None:
    st.markdown(
        f"""
        <div class="lp-final-cta">
            <p class="lp-final-kicker">Ready to evaluate?</p>
            <h2 class="lp-final-title">Your first {FREE_EVALUATIONS_PER_ACCOUNT} evaluations are free — no credit card required</h2>
            <p class="lp-final-lead">Upload a product image, enter your numbers, and get your score in about 30 seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if show_buttons:
        _, bottom_cta, _ = st.columns([1, 1.4, 1])
        with bottom_cta:
            if st.button("Start free evaluation →", type="primary", use_container_width=True, key="landing_bottom_cta"):
                request_free_evaluation()


def render_landing_footnote() -> None:
    st.markdown(
        '<p class="landing-footnote">ProductScore · Built for e-commerce operators</p>',
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    render_landing_hero()

    _, hero_cta, _ = st.columns([1, 1.4, 1])
    with hero_cta:
        if st.button("Run your free evaluation →", type="primary", use_container_width=True, key="landing_hero_cta"):
            request_free_evaluation()

    render_landing_at_a_glance()
    render_landing_body()
    render_landing_final_cta()
    render_landing_footnote()
    _scroll_to_anchor_if_needed()
