"""Marketing landing page."""

from __future__ import annotations

import html

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, ReportSection
from ecom_evaluator.ui.subscription import request_free_evaluation

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

_FAQ_ITEMS: tuple[tuple[str, str], ...] = (
    (
        "Why no web search on the free tier?",
        "Web search APIs cost money on every evaluation. We keep the free tier input-only so "
        "you still get a premium-quality profile, risk analysis, and margin math — without us "
        "burning budget on tire-kickers. When you're serious, Premium unlocks live competitor intel.",
    ),
    (
        "What makes the free report 'ceiling quality'?",
        "The free preview gives you Sections 1–2: a weighted product score and Shark Tank-grade red flags. "
        "Premium unlocks the financial GO/NO-GO verdict plus the full execution stack.",
    ),
    (
        "When should I upgrade to Premium?",
        "Upgrade when red flags have your attention and you need the math: margin stress-tests, "
        "final verdict, marketing blueprint, live competitor intel, and ready-to-film ad scripts.",
    ),
)


def _band_open(band: str, *, section_id: str | None = None) -> str:
    id_attr = f' id="{section_id}"' if section_id else ""
    return f'<section class="lp-band lp-band--{band}"{id_attr}><div class="lp-band-bg" aria-hidden="true"></div><div class="lp-band-inner">'


def _band_close() -> str:
    return "</div></section>"


def _section_header_html(
    kicker: str,
    title: str,
    lead: str | None = None,
    *,
    reveal_class: str = "lp-reveal",
) -> str:
    lead_html = (
        f'<p class="lp-section-header-lead">{html.escape(lead)}</p>' if lead else ""
    )
    return (
        f'<div class="lp-section-header {reveal_class}">'
        f'<span class="lp-band-label">{html.escape(kicker)}</span>'
        f'<h2 class="lp-section-header-title">{html.escape(title)}</h2>'
        f"{lead_html}"
        f"</div>"
    )


def _section_card_html(section: ReportSection, *, badge: str = "Free", reveal: str = "lp-reveal") -> str:
    vis = SECTION_VISUALS[section.id]
    badge_class = "lp-free-pill" if badge == "Free" else "lp-premium-pill"
    return (
        f'<div class="lp-section-card {reveal}" style="--accent:{vis["accent"]};--accent-soft:{vis["accent_soft"]}">'
        f'<div class="lp-section-card-top">'
        f'<span class="lp-section-icon">{vis["icon"]}</span>'
        f'<span class="{badge_class}">{badge}</span>'
        f"</div>"
        f'<p class="lp-section-num">Section {section.number}</p>'
        f'<p class="lp-section-title">{html.escape(section.title)}</p>'
        f'<p class="lp-section-body">{html.escape(section.subtitle)}</p>'
        f'<p class="lp-section-highlight">{html.escape(vis["highlight"])}</p>'
        f"</div>"
    )


def _premium_pricing_html(*, reveal: str = "lp-reveal lp-reveal-scale") -> str:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    return (
        f'<div class="lp-pricing-card lp-pricing-card--premium lp-pricing-card--solo {reveal}">'
        f'<span class="lp-popular-pill">Everything included</span>'
        f'<p class="lp-pricing-tier">Premium</p>'
        f'<p class="lp-pricing-price">${premium.price_usd_monthly}<span>/mo</span></p>'
        f'<p class="lp-pricing-blurb">One plan. Full stack. Unlimited evaluations. '
        f"Unlock every section — financial verdict, marketing blueprint, live web intel, and 5× video scripts — "
        f'powered by our most advanced commercial AI engine.</p>'
        f'<ul class="lp-pricing-features">'
        f"<li>Section 3 — Financial matrix &amp; GO/NO-GO verdict</li>"
        f"<li>Section 4 — Marketing viability &amp; targeting blueprint</li>"
        f"<li>Section 5 — Live web intelligence &amp; sourcing links</li>"
        f"<li>Section 6 — Ultimate 5× video content engine</li>"
        f"<li>Unlimited evaluations</li>"
        f"</ul></div>"
    )


def _step_card_html(number: int, title: str, body: str, *, reveal: str) -> str:
    return (
        f'<div class="lp-step-card {reveal}">'
        f'<span class="lp-step-num">{number}</span>'
        f'<p class="lp-step-title">{html.escape(title)}</p>'
        f'<p class="lp-step-body">{html.escape(body)}</p>'
        f"</div>"
    )


def _faq_html() -> str:
    items = []
    for index, (question, answer) in enumerate(_FAQ_ITEMS):
        delay = f" lp-reveal-delay-{min(index + 1, 4)}"
        items.append(
            f'<details class="lp-faq-item lp-reveal{delay}">'
            f"<summary>{html.escape(question)}</summary>"
            f'<p class="lp-faq-answer">{html.escape(answer)}</p>'
            f"</details>"
        )
    return f'<div class="lp-faq-list">{"".join(items)}</div>'


def _install_scroll_reveal() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (doc.documentElement.dataset.lpRevealReady) return;
            doc.documentElement.dataset.lpRevealReady = "1";
            doc.documentElement.classList.add("lp-reveal-ready");

            const io = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (!entry.isIntersecting) return;
                        entry.target.classList.add("is-visible");
                    });
                },
                { threshold: 0.08, rootMargin: "0px 0px -2% 0px" }
            );

            const markIfInView = (node) => {
                const rect = node.getBoundingClientRect();
                if (rect.top < win.innerHeight * 0.94 && rect.bottom > 0) {
                    node.classList.add("is-visible");
                }
            };

            const bindRevealNodes = () => {
                doc.querySelectorAll(".lp-reveal:not(.lp-reveal-hero)").forEach((node) => {
                    if (node.dataset.lpObserved) return;
                    node.dataset.lpObserved = "1";
                    markIfInView(node);
                    io.observe(node);
                });
            };

            bindRevealNodes();
            win.addEventListener("load", bindRevealNodes, { once: true });
            win.addEventListener("resize", bindRevealNodes);
            const mo = new MutationObserver(() => bindRevealNodes());
            mo.observe(doc.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        height=0,
        width=0,
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


def render_landing_hero() -> None:
    st.markdown(
        f'<div class="landing-wrap"><div class="landing-hero">'
        f'<p class="landing-kicker lp-reveal-hero">Shark Tank-grade analysis</p>'
        f'<h1 class="landing-title lp-reveal-hero lp-reveal-delay-1">Know if your product can win — before you spend a dollar</h1>'
        f'<p class="landing-lead lp-reveal-hero lp-reveal-delay-2">Upload your product, enter your numbers, and get a sharp profile + red-flag analysis in ~30 seconds. '
        f"Free preview covers Sections 1–2. Upgrade to Premium for the financial verdict and full execution stack.</p>"
        f'<div class="lp-hero-badges lp-reveal-hero lp-reveal-delay-3">'
        f'<span class="lp-hero-badge">~30 sec preview</span>'
        f'<span class="lp-hero-badge">{FREE_EVALUATIONS_PER_ACCOUNT} free evals / account</span>'
        f'<span class="lp-hero-badge">2 sections free</span>'
        f'<span class="lp-hero-badge">Premium · $29/mo</span>'
        f"</div></div></div>",
        unsafe_allow_html=True,
    )


def render_landing_at_a_glance() -> None:
    st.markdown(
        _band_open("glance")
        + '<div class="lp-section-header lp-reveal"><span class="lp-band-label">At a glance</span>'
        + '<h2 class="lp-section-header-title">Everything you need to decide fast</h2></div>'
        + '<div class="lp-value-grid">'
        + '<div class="lp-value-tile lp-reveal lp-reveal-delay-1"><span class="lp-value-icon">⚡</span>'
        + '<p class="lp-value-title">~30 seconds</p>'
        + '<p class="lp-value-desc">From upload to your free profile + red-flag preview</p></div>'
        + '<div class="lp-value-tile lp-reveal lp-reveal-delay-2"><span class="lp-value-icon">📋</span>'
        + '<p class="lp-value-title">2 sections free</p>'
        + '<p class="lp-value-desc">Product profile, core metrics, and Shark Tank red flags</p></div>'
        + '<div class="lp-value-tile lp-reveal lp-reveal-delay-3"><span class="lp-value-icon">💳</span>'
        + '<p class="lp-value-title">$0 to start</p>'
        + f'<p class="lp-value-desc">{FREE_EVALUATIONS_PER_ACCOUNT} free evaluations per account — no credit card required</p></div>'
        + '<div class="lp-value-tile lp-reveal lp-reveal-delay-4"><span class="lp-value-icon">📊</span>'
        + '<p class="lp-value-title">5 scored metrics</p>'
        + '<p class="lp-value-desc">Saturation, velocity, logistics, seasonality, and brandability</p></div>'
        + "</div>"
        + _band_close(),
        unsafe_allow_html=True,
    )


def render_landing_body() -> None:
    free_sections = REPORT_SECTIONS[:2]
    st.markdown(
        _band_open("free")
        + _section_header_html(
            "What you get free",
            "Two sections designed to hook you — then Premium delivers the verdict",
            "Free users get a real profile score and brutal red-flag analysis — enough to feel the opportunity "
            "and the risk. The financial GO/NO-GO verdict and execution stack unlock on Premium.",
        )
        + '<div class="lp-section-grid">'
        + _section_card_html(free_sections[0], reveal="lp-reveal lp-reveal-left lp-reveal-delay-1")
        + _section_card_html(free_sections[1], reveal="lp-reveal lp-reveal-right lp-reveal-delay-2")
        + "</div>"
        + _band_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        _band_open("premium", section_id="section-pricing")
        + _section_header_html(
            "Unlock the full report",
            "One plan. Everything included. $29/month.",
            "Sections 3–6 cover the financial verdict, marketing blueprint, live competitor intel, "
            "and five ready-to-shoot video scripts — plus unlimited evaluations.",
        )
        + _premium_pricing_html()
        + _band_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        _band_open("process", section_id="section-process")
        + _section_header_html("How it works", "From product photo to go/no-go in three steps")
        + '<div class="lp-steps-grid">'
        + _step_card_html(
            1,
            "Upload and input",
            "Add your product image, cost, sell price, dimensions, and a short description. Takes 60 seconds.",
            reveal="lp-reveal lp-reveal-delay-1",
        )
        + _step_card_html(
            2,
            "AI evaluates",
            "Our AI analyzes your inputs — profile and risks on free, full stack on Premium.",
            reveal="lp-reveal lp-reveal-delay-2",
        )
        + _step_card_html(
            3,
            "Decide and scale",
            "Read red flags free. Upgrade for the GO/NO-GO verdict, sourcing intel, and ad scripts.",
            reveal="lp-reveal lp-reveal-delay-3",
        )
        + "</div>"
        + _band_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        _band_open("sample", section_id="section-sample")
        + _section_header_html("Inside your report", "A snapshot of what you'll see")
        + '<div class="lp-preview-card lp-reveal lp-reveal-scale">'
        + '<div class="lp-preview-left">'
        + '<p class="lp-preview-label">Overall product score</p>'
        + '<p class="lp-preview-score">74<span>/100</span></p>'
        + '<p class="lp-preview-verdict">Proceed with caution</p>'
        + "</div>"
        + '<div class="lp-preview-right">'
        + '<p class="lp-preview-metric"><span>Market saturation</span><span class="lp-bar"><i style="width:62%"></i></span><strong>62</strong></p>'
        + '<p class="lp-preview-metric"><span>Marketing velocity</span><span class="lp-bar"><i style="width:81%"></i></span><strong>81</strong></p>'
        + '<p class="lp-preview-metric"><span>Logistics and margin</span><span class="lp-bar"><i style="width:88%"></i></span><strong>88</strong></p>'
        + '<p class="lp-preview-metric"><span>Seasonality</span><span class="lp-bar"><i style="width:55%"></i></span><strong>55</strong></p>'
        + '<p class="lp-preview-metric"><span>Brandability</span><span class="lp-bar"><i style="width:70%"></i></span><strong>70</strong></p>'
        + "</div></div>"
        + _band_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        _band_open("compare")
        + _section_header_html("Compare plans", "Free preview vs Premium full stack")
        + f'<div class="lp-compare-wrap lp-reveal lp-reveal-scale"><table class="lp-compare-table">'
        f"<thead><tr><th>Feature</th><th>Free</th><th>Premium</th></tr></thead><tbody>"
        f"<tr><td>Sections 1–2 (profile + red flags)</td><td>Yes</td><td>Yes</td></tr>"
        f"<tr><td>Weighted 5-metric score</td><td>Yes</td><td>Yes</td></tr>"
        f"<tr><td>Financial matrix &amp; GO/NO-GO verdict (Section 3)</td><td>—</td><td>Yes</td></tr>"
        f"<tr><td>Marketing blueprint (Section 4)</td><td>—</td><td>Yes</td></tr>"
        f"<tr><td>Live web intel &amp; sourcing (Section 5)</td><td>—</td><td>Yes</td></tr>"
        f"<tr><td>5× video script engine (Section 6)</td><td>—</td><td>Yes</td></tr>"
        f"<tr><td>Evaluations</td><td>{FREE_EVALUATIONS_PER_ACCOUNT} free / account</td><td>Unlimited</td></tr>"
        f"<tr><td>Price</td><td>$0</td><td>$29/mo</td></tr>"
        f"</tbody></table></div>"
        + _band_close(),
        unsafe_allow_html=True,
    )

    st.markdown(
        _band_open("faq", section_id="section-resources")
        + _section_header_html("FAQ", "Common questions before you evaluate")
        + _faq_html()
        + _band_close(),
        unsafe_allow_html=True,
    )


def render_landing_final_cta(*, show_buttons: bool = True) -> None:
    st.markdown(
        _band_open("final")
        + f'<div class="lp-final-cta lp-reveal">'
        f'<p class="lp-final-kicker">Ready to evaluate?</p>'
        f'<h2 class="lp-final-title">Your first {FREE_EVALUATIONS_PER_ACCOUNT} evaluations are free — no credit card required</h2>'
        f'<p class="lp-final-lead">Upload a product image, enter your numbers, and get your score in about 30 seconds.</p>'
        f"</div>"
        + _band_close(),
        unsafe_allow_html=True,
    )

    if show_buttons:
        _, bottom_cta, _ = st.columns([1, 1.4, 1])
        with bottom_cta:
            if st.button("Start free evaluation →", type="primary", use_container_width=True, key="landing_bottom_cta"):
                request_free_evaluation()


def render_landing_footnote() -> None:
    st.markdown(
        '<p class="landing-footnote lp-reveal">ProductScore · Built for e-commerce operators</p>',
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    _install_scroll_reveal()
    render_landing_hero()

    st.markdown('<div class="lp-hero-cta-gap" aria-hidden="true"></div>', unsafe_allow_html=True)
    _, hero_cta, _ = st.columns([1, 1.4, 1])
    with hero_cta:
        if st.button("Run your free evaluation →", type="primary", use_container_width=True, key="landing_hero_cta"):
            request_free_evaluation()

    render_landing_at_a_glance()
    render_landing_body()
    render_landing_final_cta()
    render_landing_footnote()
    _scroll_to_anchor_if_needed()
