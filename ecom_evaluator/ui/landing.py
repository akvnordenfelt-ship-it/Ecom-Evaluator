"""Marketing landing page."""

from __future__ import annotations

import html

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS, ReportSection
from ecom_evaluator.ui.branding import BRAND_NAME
from ecom_evaluator.ui.carousel_assets import carousel_image_data_uri
from ecom_evaluator.ui.carousel_samples import (
    install_carousel_sample_bridge,
    maybe_show_carousel_sample_dialog,
    render_hidden_carousel_sample_buttons,
)
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
    "competitor_sentiment": {
        "icon": "📊",
        "accent": "#F59E0B",
        "accent_soft": "#FFFBEB",
        "highlight": "Competitor review sentiment and product improvement directives",
    },
}

_CAROUSEL_PRODUCTS: tuple[dict[str, str | float], ...] = (
    {
        "name": "Flame Effect Essential Oil Diffuser",
        "slug": "flame-diffuser",
        "category": "HOME & DECOR",
        "icon": "🕯️",
        "gradient": "linear-gradient(135deg, #FEF3C7 0%, #F97316 100%)",
        "score": 8.9,
        "trend": "↗ +41% Demand this month",
        "profit": "$1,450",
        "margin": "72%",
    },
    {
        "name": "Personalized Pet Travel Harness",
        "slug": "pet-travel-harness",
        "category": "PET SUPPLIES",
        "icon": "🦮",
        "gradient": "linear-gradient(135deg, #FFE4E6 0%, #FB7185 100%)",
        "score": 9.2,
        "trend": "↗ Hot Trend (Peak Summer)",
        "profit": "$1,820",
        "margin": "65%",
    },
    {
        "name": "Cheap Bluetooth Sleep Mask Headphones",
        "slug": "sleep-mask-headphones",
        "category": "ELECTRONICS",
        "icon": "😴",
        "gradient": "linear-gradient(135deg, #E5E7EB 0%, #6B7280 100%)",
        "score": 4.2,
        "trend": "↘ -28% Market Saturation",
        "profit": "-$250",
        "margin": "35%",
        "fail": True,
        "note": "High Return Rate — 18% of customers report battery failure within 2 weeks.",
    },
    {
        "name": "Portable USB-C Rechargeable Blender",
        "slug": "usb-blender",
        "category": "SMART KITCHEN",
        "icon": "🥤",
        "gradient": "linear-gradient(135deg, #DCFCE7 0%, #06B6D4 100%)",
        "score": 8.4,
        "trend": "↗ +14% Demand this month",
        "profit": "$920",
        "margin": "58%",
    },
    {
        "name": "Sleep-Tech Smart Scales (Cloud Sync)",
        "slug": "smart-scale",
        "category": "HEALTH & TECH",
        "icon": "⚖️",
        "gradient": "linear-gradient(135deg, #E0E7FF 0%, #4F46E5 100%)",
        "score": 8.7,
        "trend": "↗ +22% Search Volume",
        "profit": "$2,100",
        "margin": "61%",
    },
    {
        "name": "Heavy Latex Resistance Loop Bands",
        "slug": "resistance-bands",
        "category": "FITNESS & GEAR",
        "icon": "💪",
        "gradient": "linear-gradient(135deg, #FEE2E2 0%, #EF4444 100%)",
        "score": 5.1,
        "trend": "→ Brutal Price War",
        "profit": "$80",
        "margin": "12%",
        "fail": True,
        "note": "Zero Margin — Oversaturated niche on Amazon, advertising cost eats all profit.",
    },
    {
        "name": "Automatic Electric Jar Opener",
        "slug": "electric-jar-opener",
        "category": "KITCHEN & GADGETS",
        "icon": "🫙",
        "gradient": "linear-gradient(135deg, #FFEDD5 0%, #EA580C 100%)",
        "score": 8.1,
        "trend": "↗ +18% Search Volume",
        "profit": "$1,100",
        "margin": "64%",
    },
    {
        "name": "DIY Ultrasonic Skin Scrubber",
        "slug": "skin-scrubber",
        "category": "BEAUTY & COSMETICS",
        "icon": "⚠️",
        "gradient": "linear-gradient(135deg, #FEF2F2 0%, #DC2626 100%)",
        "score": 3.8,
        "trend": "↘ Legal / Liability Risk",
        "profit": "-$400",
        "margin": "48%",
        "fail": True,
        "note": "High Liability — Severe customer complaints regarding skin burns and lack of CE certification.",
    },
    {
        "name": "Magnetic Desktop Cable Organizer",
        "slug": "cable-organizer",
        "category": "OFFICE & PRODUCTIVITY",
        "icon": "🧲",
        "gradient": "linear-gradient(135deg, #F5F5F4 0%, #78716C 100%)",
        "score": 7.9,
        "trend": "↗ Steady Growth",
        "profit": "$750",
        "margin": "70%",
    },
    {
        "name": "Ultra-Lightweight Inflatable Camping Pillow",
        "slug": "camping-pillow",
        "category": "TRAVEL & OUTDOOR",
        "icon": "🏕️",
        "gradient": "linear-gradient(135deg, #D1FAE5 0%, #059669 100%)",
        "score": 8.5,
        "trend": "↗ +33% Seasonal Spike",
        "profit": "$1,320",
        "margin": "67%",
    },
    {
        "name": "Silicone Baby Bibs with Food Catcher",
        "slug": "baby-bibs",
        "category": "BABY SUPPLIES",
        "icon": "👶",
        "gradient": "linear-gradient(135deg, #FCE7F3 0%, #F472B6 100%)",
        "score": 8.3,
        "trend": "↗ High Consistent Demand",
        "profit": "$980",
        "margin": "74%",
    },
    {
        "name": "Smart Wireless Peephole Camera",
        "slug": "peephole-camera",
        "category": "HOME SECURITY",
        "icon": "📹",
        "gradient": "linear-gradient(135deg, #DBEAFE 0%, #1D4ED8 100%)",
        "score": 8.8,
        "trend": "↗ +52% Year-over-Year",
        "profit": "$2,450",
        "margin": "59%",
    },
)

_FAQ_ITEMS: tuple[tuple[str, str], ...] = (
    (
        "Why doesn't the free tier include live web search?",
        "Live web search runs on every evaluation and adds cost. The free tier uses your product "
        "inputs only and still returns a weighted score, margin math, and red-flag analysis in Sections 1–2.",
    ),
    (
        "What's included in the free report?",
        "Sections 1–2 cover your product profile, core metrics, weighted score, and red-flag analysis. "
        "Premium adds the financial verdict, marketing blueprint, competitor intel, and review sentiment analysis in Sections 3–6.",
    ),
    (
        "When should I upgrade to Premium?",
        "Upgrade when red flags have your attention and you need the math: margin stress-tests, "
        "final verdict, marketing blueprint, live competitor intel, and competitor review sentiment analysis.",
    ),
)


def _band_open(band: str, *, section_id: str | None = None) -> str:
    id_attr = f' id="{section_id}"' if section_id else ""
    return (
        f'<section class="lp-band lp-band--{band} lp-page-flow"{id_attr}>'
        f'<div class="lp-band-bg" aria-hidden="true"></div>'
        f'<div class="lp-band-inner">'
    )


def _band_close() -> str:
    return "</div></section>"


def _carousel_score_class(score: float, *, is_fail: bool = False) -> str:
    if is_fail or score < 6.0:
        return "lp-carousel-score lp-carousel-score--fail"
    if score >= 8.0:
        return "lp-carousel-score lp-carousel-score--high"
    if score >= 7.0:
        return "lp-carousel-score lp-carousel-score--mid"
    return "lp-carousel-score lp-carousel-score--low"


def _carousel_product_card(product: dict[str, str | float]) -> str:
    score = float(product["score"])
    is_fail = bool(product.get("fail"))
    score_class = _carousel_score_class(score, is_fail=is_fail)
    slug_raw = str(product["slug"])
    name = html.escape(str(product["name"]))
    category = html.escape(str(product["category"]))
    icon = html.escape(str(product["icon"]))
    gradient = str(product["gradient"])
    trend = html.escape(str(product["trend"]))
    profit = html.escape(str(product["profit"]))
    margin = html.escape(str(product["margin"]))
    image_url = html.escape(carousel_image_data_uri(slug_raw))
    card_class = "lp-carousel-card lp-carousel-card--fail" if is_fail else "lp-carousel-card"
    trend_class = "lp-carousel-trend lp-carousel-trend--fail" if is_fail else "lp-carousel-trend"
    profit_value_class = (
        "lp-carousel-profit-value--loss"
        if str(product["profit"]).strip().startswith("-")
        else ""
    )
    fail_badge = (
        '<span class="lp-carousel-fail-badge">FAIL · High Risk</span>' if is_fail else ""
    )
    note_html = ""
    if product.get("note"):
        note_html = f'<p class="lp-carousel-risk-note">{html.escape(str(product["note"]))}</p>'
    return (
        f'<article class="{card_class}">'
        f'<div class="lp-carousel-card-media" style="background:{gradient}">'
        f'<div class="lp-carousel-media-fallback" aria-hidden="true">'
        f'<span class="lp-carousel-media-icon">{icon}</span>'
        f"</div>"
        f'<img src="{image_url}" alt="{name}" loading="lazy" draggable="false" '
        f'onerror="this.classList.add(\'is-broken\')" />'
        f"</div>"
        f'<div class="lp-carousel-card-body">'
        f'<div class="lp-carousel-card-content">'
        f"{fail_badge}"
        f'<span class="lp-carousel-category">{category}</span>'
        f'<h3 class="lp-carousel-name">{name}</h3>'
        f'<div class="lp-carousel-score-row">'
        f'<span class="{score_class}">{score:.1f}<span>/10</span></span>'
        f'<span class="{trend_class}">{trend}</span>'
        f"</div>"
        f'<div class="lp-carousel-divider"></div>'
        f'<p class="lp-carousel-profit">Est. Net Profit: '
        f'<strong{" class=\"lp-carousel-profit-value--loss\"" if profit_value_class else ""}>'
        f"{profit} / mo</strong></p>"
        f'<p class="lp-carousel-margin">{margin} Gross Margin</p>'
        f"{note_html}"
        f"</div>"
        f'<div class="lp-carousel-card-footer">'
        f'<a class="lp-carousel-demo-link" href="#" data-ps-sample-slug="{html.escape(slug_raw)}" target="_self">View Sample Evaluation →</a>'
        f"</div></div></article>"
    )


def render_landing_product_carousel() -> None:
    cards = "".join(_carousel_product_card(product) for product in _CAROUSEL_PRODUCTS)
    track = f'<div class="lp-carousel-track">{cards}{cards}</div>'
    st.markdown(
        '<section class="lp-carousel-section lp-reveal" aria-label="Sample product evaluations">'
        '<div class="lp-carousel-header">'
        '<span class="lp-band-label">Live preview</span>'
        '<h2 class="lp-carousel-title">Trending products analyzed right now</h2>'
        '<p class="lp-carousel-lead">Realistic profit estimates and Crow Metrics scores from live niches. Auto-scrolls — click and drag to explore.</p>'
        "</div>"
        f'<div class="lp-carousel-shell"><div class="lp-carousel-viewport">{track}</div></div>'
        "</section>",
        unsafe_allow_html=True,
    )


def _install_carousel_drag() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            const CLICK_THRESHOLD = 6;
            const FRICTION = 0.92;
            const MIN_VELOCITY = 0.25;
            const AUTO_SPEED = 0.42;
            const AUTO_RESUME_MS = 1800;

            function initViewport(viewport) {
                if (viewport.dataset.lpCarouselReady) return;
                const track = viewport.querySelector(".lp-carousel-track");
                if (!track) return;
                viewport.dataset.lpCarouselReady = "1";

                let position = 0;
                let loopWidth = 0;
                let isDragging = false;
                let pointerId = null;
                let lastX = 0;
                let lastTime = 0;
                let velocity = 0;
                let dragDistance = 0;
                let suppressClick = false;
                let momentumFrame = null;
                let autoFrame = null;
                let autoPaused = false;
                let autoResumeTimer = null;
                const reducedMotion = win.matchMedia("(prefers-reduced-motion: reduce)");

                function measure() {
                    loopWidth = track.scrollWidth / 2;
                    if (!loopWidth || Number.isNaN(loopWidth)) loopWidth = 1;
                }

                function wrapPosition() {
                    if (loopWidth <= 0) return;
                    while (position <= -loopWidth) position += loopWidth;
                    while (position > 0) position -= loopWidth;
                }

                function render() {
                    track.style.transform = "translate3d(" + position + "px, 0, 0)";
                }

                function stopMomentum() {
                    if (!momentumFrame) return;
                    cancelAnimationFrame(momentumFrame);
                    momentumFrame = null;
                }

                function stopAuto() {
                    if (!autoFrame) return;
                    cancelAnimationFrame(autoFrame);
                    autoFrame = null;
                }

                function clearAutoResume() {
                    if (!autoResumeTimer) return;
                    clearTimeout(autoResumeTimer);
                    autoResumeTimer = null;
                }

                function canAutoRun() {
                    return (
                        !autoPaused &&
                        !isDragging &&
                        !momentumFrame &&
                        !reducedMotion.matches
                    );
                }

                function autoStep() {
                    autoFrame = null;
                    if (!canAutoRun()) return;
                    position -= AUTO_SPEED;
                    wrapPosition();
                    render();
                    autoFrame = requestAnimationFrame(autoStep);
                }

                function startAuto() {
                    if (autoFrame || !canAutoRun()) return;
                    autoFrame = requestAnimationFrame(autoStep);
                }

                function pauseAuto() {
                    autoPaused = true;
                    stopAuto();
                    clearAutoResume();
                }

                function resumeAutoAfter(delay) {
                    autoPaused = true;
                    stopAuto();
                    clearAutoResume();
                    autoResumeTimer = setTimeout(() => {
                        autoResumeTimer = null;
                        autoPaused = false;
                        startAuto();
                    }, delay);
                }

                function startMomentum() {
                    stopMomentum();
                    stopAuto();
                    function step() {
                        if (Math.abs(velocity) < MIN_VELOCITY) {
                            momentumFrame = null;
                            resumeAutoAfter(AUTO_RESUME_MS);
                            return;
                        }
                        position += velocity;
                        velocity *= FRICTION;
                        wrapPosition();
                        render();
                        momentumFrame = requestAnimationFrame(step);
                    }
                    momentumFrame = requestAnimationFrame(step);
                }

                function onPointerDown(event) {
                    if (event.button !== undefined && event.button !== 0) return;
                    isDragging = true;
                    pointerId = event.pointerId;
                    viewport.classList.add("is-grabbing");
                    try { viewport.setPointerCapture(event.pointerId); } catch (error) {}
                    lastX = event.clientX;
                    lastTime = performance.now();
                    velocity = 0;
                    dragDistance = 0;
                    suppressClick = false;
                    stopMomentum();
                    pauseAuto();
                }

                function onPointerMove(event) {
                    if (!isDragging || event.pointerId !== pointerId) return;
                    const dx = event.clientX - lastX;
                    position += dx;
                    dragDistance += Math.abs(dx);
                    const now = performance.now();
                    const dt = Math.max(now - lastTime, 1);
                    velocity = (dx / dt) * 16.67;
                    lastX = event.clientX;
                    lastTime = now;
                    wrapPosition();
                    render();
                    if (dragDistance > CLICK_THRESHOLD) {
                        suppressClick = true;
                        event.preventDefault();
                    }
                }

                function endDrag(event) {
                    if (!isDragging) return;
                    if (event && event.pointerId !== pointerId) return;
                    isDragging = false;
                    pointerId = null;
                    viewport.classList.remove("is-grabbing");
                    try {
                        if (event) viewport.releasePointerCapture(event.pointerId);
                    } catch (error) {}
                    if (Math.abs(velocity) >= MIN_VELOCITY) {
                        startMomentum();
                    } else {
                        resumeAutoAfter(AUTO_RESUME_MS);
                    }
                }

                viewport.addEventListener("pointerdown", onPointerDown);
                viewport.addEventListener("pointermove", onPointerMove, { passive: false });
                viewport.addEventListener("pointerup", endDrag);
                viewport.addEventListener("pointercancel", endDrag);
                viewport.addEventListener("mouseenter", pauseAuto);
                viewport.addEventListener("mouseleave", () => resumeAutoAfter(600));
                viewport.addEventListener("touchstart", pauseAuto, { passive: true });
                viewport.addEventListener("touchend", () => resumeAutoAfter(AUTO_RESUME_MS), { passive: true });

                viewport.addEventListener(
                    "click",
                    (event) => {
                        if (!suppressClick) return;
                        event.preventDefault();
                        event.stopPropagation();
                        suppressClick = false;
                    },
                    true
                );

                track.querySelectorAll("img").forEach((img) => {
                    img.setAttribute("draggable", "false");
                    if (!img.complete) {
                        img.addEventListener("load", () => {
                            measure();
                            wrapPosition();
                            render();
                        });
                    }
                });

                measure();
                render();
                win.addEventListener("resize", () => {
                    measure();
                    wrapPosition();
                    render();
                });
                setTimeout(() => {
                    measure();
                    wrapPosition();
                    render();
                    startAuto();
                }, 300);
            }

            function scan() {
                doc.querySelectorAll(".lp-carousel-viewport").forEach(initViewport);
            }

            if (!win.__lpCarousel) {
                win.__lpCarousel = { scan };
                win.__lpCarousel.mo = new MutationObserver(() => win.__lpCarousel.scan());
                win.__lpCarousel.mo.observe(doc.body, { childList: true, subtree: true });
            }
            requestAnimationFrame(() => requestAnimationFrame(scan));
        })();
        </script>
        """,
        height=0,
        width=0,
    )


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
        f"Unlock every section — financial verdict, marketing blueprint, live web intel, and competitor review sentiment — "
        f'powered by our most advanced commercial AI engine.</p>'
        f'<ul class="lp-pricing-features">'
        f"<li>Section 3 — Financial matrix &amp; GO/NO-GO verdict</li>"
        f"<li>Section 4 — Marketing viability &amp; targeting blueprint</li>"
        f"<li>Section 5 — Live web intelligence &amp; sourcing links</li>"
        f"<li>Section 6 — Competitor review sentiment analysis</li>"
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

            if (!win.__lpReveal) {
                win.__lpReveal = {
                    io: new IntersectionObserver(
                        (entries) => {
                            entries.forEach((entry) => {
                                if (!entry.isIntersecting) return;
                                entry.target.classList.add("is-visible");
                            });
                        },
                        { threshold: 0.1, rootMargin: "0px 0px -3% 0px" }
                    ),
                };
                win.__lpReveal.mo = new MutationObserver(() => win.__lpReveal.scan());
                win.__lpReveal.mo.observe(doc.body, { childList: true, subtree: true });
            }

            win.__lpReveal.scan = function scan() {
                doc.documentElement.classList.add("lp-reveal-ready");
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        doc.querySelectorAll(".lp-reveal:not(.lp-reveal-hero)").forEach((node) => {
                            if (node.dataset.lpObserved) return;
                            node.dataset.lpObserved = "1";
                            win.__lpReveal.io.observe(node);
                        });
                    });
                });
            };

            win.__lpReveal.scan();
        })();
        </script>
        """,
        height=0,
        width=0,
    )


_HERO_PREVIEW_SLUG = "usb-blender"

_HERO_METRICS: tuple[tuple[str, str, int, str], ...] = (
    ("📈", "Market Demand", 92, "blue"),
    ("💰", "Profitability", 85, "blue"),
    ("⚔️", "Competition", 71, "blue"),
    ("⚠️", "Saturation Risk", 38, "amber"),
    ("🏭", "Supplier Score", 82, "blue"),
)


def _hero_metric_row(*, icon: str, label: str, score: int, tone: str) -> str:
    tone_class = "is-amber" if tone == "amber" else ""
    return (
        f'<div class="lp-hero-metric">'
        f'<span class="lp-hero-metric-icon">{html.escape(icon)}</span>'
        f"<div>"
        f'<p class="lp-hero-metric-label">{html.escape(label)}</p>'
        f'<div class="lp-hero-metric-bar"><i class="{tone_class}" style="width:{score}%"></i></div>'
        f"</div>"
        f'<span class="lp-hero-metric-score">{score}/100</span>'
        f"</div>"
    )


def _hero_preview_card_html() -> str:
    image_url = html.escape(carousel_image_data_uri(_HERO_PREVIEW_SLUG), quote=True)
    metrics = "".join(
        _hero_metric_row(icon=icon, label=label, score=score, tone=tone)
        for icon, label, score, tone in _HERO_METRICS
    )
    return (
        '<div class="lp-hero-preview">'
        '<div class="lp-hero-card">'
        '<div class="lp-hero-card-head">'
        f'<img class="lp-hero-card-thumb" src="{image_url}" alt="Portable USB-C Rechargeable Blender" loading="lazy" />'
        '<div class="lp-hero-card-meta">'
        '<p class="lp-hero-card-name">Portable USB-C Rechargeable Blender</p>'
        '<div class="lp-hero-card-badges">'
        '<span class="lp-hero-score-pill">8.4 / 10</span>'
        '<span class="lp-hero-trend-pill">↗ +14% Demand this month</span>'
        "</div></div></div>"
        '<div class="lp-hero-card-stats">'
        '<div><p class="lp-hero-stat-label">Est. Net Profit</p>'
        '<p class="lp-hero-stat-value lp-hero-stat-value--green">$920 / mo</p></div>'
        '<div><p class="lp-hero-stat-label">Gross Margin</p>'
        '<p class="lp-hero-stat-value">58%</p></div>'
        "</div>"
        '<div class="lp-hero-card-body">'
        '<div class="lp-hero-score-ring" style="--score:89"><span>89</span></div>'
        "<div>"
        '<p class="lp-hero-verdict-kicker">Overall score</p>'
        '<p class="lp-hero-verdict-title">High potential</p>'
        '<p class="lp-hero-verdict-copy">Strong demand and healthy margins with manageable competition.</p>'
        '<span class="lp-hero-go-pill">GO</span>'
        "</div></div>"
        f'<div class="lp-hero-metrics">{metrics}</div>'
        '<a class="lp-hero-card-footer" href="#" data-ps-nav-anchor="sample" target="_self">View Full Report →</a>'
        "</div></div>"
    )


def _hero_features_html() -> str:
    return (
        '<div class="lp-hero-features">'
        '<div class="lp-hero-feature">'
        '<span class="lp-hero-feature-icon">⏱</span>'
        '<p class="lp-hero-feature-title">~30 seconds</p>'
        '<p class="lp-hero-feature-desc">From upload to full preview</p>'
        "</div>"
        '<div class="lp-hero-feature">'
        '<span class="lp-hero-feature-icon">📋</span>'
        '<p class="lp-hero-feature-title">2 sections free</p>'
        '<p class="lp-hero-feature-desc">Profile, core metrics &amp; red flags</p>'
        "</div>"
        f'<div class="lp-hero-feature">'
        f'<span class="lp-hero-feature-icon">🎁</span>'
        f'<p class="lp-hero-feature-title">{FREE_EVALUATIONS_PER_ACCOUNT} free evaluations</p>'
        f'<p class="lp-hero-feature-desc">Per account, no credit card</p>'
        f"</div>"
        '<div class="lp-hero-feature">'
        '<span class="lp-hero-feature-icon">🛡</span>'
        '<p class="lp-hero-feature-title">Upgrade anytime</p>'
        '<p class="lp-hero-feature-desc">Unlock full report, unlimited evaluations</p>'
        "</div></div>"
    )


def _install_landing_hero_cta_bridge() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__psLandingHeroCtaInstalled) return;
            win.__psLandingHeroCtaInstalled = true;

            function clickHeroCta(attempt) {
                const tries = attempt || 0;
                const host = doc.querySelector('[class*="st-key-landing_hero_cta"]');
                if (!host) {
                    if (tries < 8) {
                        win.setTimeout(function () { clickHeroCta(tries + 1); }, 40);
                    }
                    return;
                }
                const button = host.querySelector("button");
                if (!button) {
                    if (tries < 8) {
                        win.setTimeout(function () { clickHeroCta(tries + 1); }, 40);
                    }
                    return;
                }
                button.click();
            }

            doc.addEventListener(
                "click",
                function (event) {
                    const link = event.target.closest(".lp-hero-cta");
                    if (!link) return;
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    clickHeroCta(0);
                },
                true
            );
        })();
        </script>
        """,
        height=0,
        width=0,
    )

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
    brand = html.escape(BRAND_NAME)
    st.markdown(
        '<div class="landing-wrap"><section class="landing-hero">'
        '<div class="lp-hero-grid">'
        '<div class="lp-hero-copy">'
        '<span class="lp-hero-tag lp-reveal-hero">AI Product Evaluation</span>'
        '<h1 class="lp-hero-title lp-reveal-hero lp-reveal-delay-1">Know if a product is <em>worth selling.</em></h1>'
        f'<p class="lp-hero-lead lp-reveal-hero lp-reveal-delay-2">Upload any ecommerce product and <strong>{brand}</strong> uses AI to evaluate demand, profitability, competition, suppliers, and risk before you invest.</p>'
        '<a class="lp-hero-cta lp-reveal-hero lp-reveal-delay-3" href="#">Start Free Evaluation →</a>'
        '<div class="lp-hero-trust lp-reveal-hero lp-reveal-delay-3">'
        '<span class="lp-hero-trust-item"><span class="lp-hero-trust-icon">⚡</span>~30 sec preview</span>'
        '<span class="lp-hero-trust-item"><span class="lp-hero-trust-icon">★</span>No credit card required</span>'
        "</div>"
        '<div class="lp-hero-social lp-reveal-hero lp-reveal-delay-3">'
        '<span class="lp-hero-avatars" aria-hidden="true">'
        '<span class="lp-hero-avatar lp-hero-avatar--a"></span>'
        '<span class="lp-hero-avatar lp-hero-avatar--b"></span>'
        '<span class="lp-hero-avatar lp-hero-avatar--c"></span>'
        '<span class="lp-hero-avatar lp-hero-avatar--d"></span>'
        "</span>"
        '<span class="lp-hero-stars" aria-hidden="true">★★★★★</span>'
        '<span class="lp-hero-social-text">Trusted by ecommerce founders</span>'
        "</div></div>"
        + _hero_preview_card_html()
        + "</div>"
        + _hero_features_html()
        + "</section></div>",
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
    free_sections = REPORT_SECTIONS[:2]
    st.markdown(
        _band_open("free")
        + _section_header_html(
            "What you get free",
            "Sections 1–2: profile, score, and red-flag analysis",
            "The free report covers your product profile, core metrics, and risk flags. "
            "Premium adds the financial verdict and the full Sections 3–6 stack.",
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
            "and competitor review sentiment analysis — plus unlimited evaluations.",
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
            "Read red flags free. Upgrade for the GO/NO-GO verdict, sourcing intel, and sentiment analysis.",
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
        f"<tr><td>Competitor review sentiment analysis (Section 6)</td><td>—</td><td>Yes</td></tr>"
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
        st.markdown('<div class="lp-final-cta-gap" aria-hidden="true"></div>', unsafe_allow_html=True)
        st.markdown('<div class="lp-primary-cta-wrap">', unsafe_allow_html=True)
        if st.button("Start free evaluation →", type="primary", use_container_width=True, key="landing_bottom_cta"):
            request_free_evaluation()
        st.markdown("</div>", unsafe_allow_html=True)


def render_landing_footnote() -> None:
    st.markdown(
        f'<p class="landing-footnote lp-reveal">{html.escape(BRAND_NAME)} · Built for e-commerce operators</p>',
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    render_hidden_carousel_sample_buttons()
    install_carousel_sample_bridge()
    _install_landing_hero_cta_bridge()
    render_landing_hero()

    st.markdown('<div class="lp-hero-cta-host">', unsafe_allow_html=True)
    if st.button("Start Free Evaluation →", type="primary", key="landing_hero_cta"):
        request_free_evaluation()
    st.markdown("</div>", unsafe_allow_html=True)

    render_landing_product_carousel()
    render_landing_body()
    render_landing_final_cta()
    render_landing_footnote()
    _install_scroll_reveal()
    _install_carousel_drag()
    _scroll_to_anchor_if_needed()
    maybe_show_carousel_sample_dialog()
