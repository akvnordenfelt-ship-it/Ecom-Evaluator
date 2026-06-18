"""Marketing landing page — Crow Metrics SaaS redesign."""

from __future__ import annotations

import html

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.config import FREE_EVALUATIONS_PER_ACCOUNT
from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.report_sections import REPORT_SECTIONS
from ecom_evaluator.ui.branding import BRAND_NAME
from ecom_evaluator.ui.carousel_assets import carousel_image_data_uri
from ecom_evaluator.ui.carousel_samples import (
    install_carousel_sample_bridge,
    maybe_show_carousel_sample_dialog,
    render_hidden_carousel_sample_buttons,
)
from ecom_evaluator.ui.live_market_stats import (
    evaluated_today_ticker,
    format_count,
)
from ecom_evaluator.ui.subscription import request_free_evaluation

_HERO_SLUG = "pet-travel-harness"

_CAROUSEL_PRODUCTS: tuple[dict[str, str | float], ...] = (
    {"name": "Flame Effect Essential Oil Diffuser", "slug": "flame-diffuser", "category": "HOME & DECOR", "icon": "🕯️", "gradient": "linear-gradient(135deg, #FEF3C7 0%, #F97316 100%)", "score": 8.9, "trend": "↗ +41% Demand this month", "profit": "$1,450", "margin": "72%"},
    {"name": "Personalized Pet Travel Harness", "slug": "pet-travel-harness", "category": "PET SUPPLIES", "icon": "🦮", "gradient": "linear-gradient(135deg, #FFE4E6 0%, #FB7185 100%)", "score": 9.2, "trend": "↗ Hot Trend (Peak Summer)", "profit": "$1,820", "margin": "65%"},
    {"name": "Cheap Bluetooth Sleep Mask Headphones", "slug": "sleep-mask-headphones", "category": "ELECTRONICS", "icon": "😴", "gradient": "linear-gradient(135deg, #E5E7EB 0%, #6B7280 100%)", "score": 4.2, "trend": "↘ -28% Market Saturation", "profit": "-$250", "margin": "35%", "fail": True, "note": "High Return Rate — 18% of customers report battery failure within 2 weeks."},
    {"name": "Portable USB-C Rechargeable Blender", "slug": "usb-blender", "category": "SMART KITCHEN", "icon": "🥤", "gradient": "linear-gradient(135deg, #DCFCE7 0%, #06B6D4 100%)", "score": 8.4, "trend": "↗ +14% Demand this month", "profit": "$920", "margin": "58%"},
    {"name": "Sleep-Tech Smart Scales (Cloud Sync)", "slug": "smart-scale", "category": "HEALTH & TECH", "icon": "⚖️", "gradient": "linear-gradient(135deg, #E0E7FF 0%, #4F46E5 100%)", "score": 8.7, "trend": "↗ +22% Search Volume", "profit": "$2,100", "margin": "61%"},
    {"name": "Heavy Latex Resistance Loop Bands", "slug": "resistance-bands", "category": "FITNESS & GEAR", "icon": "💪", "gradient": "linear-gradient(135deg, #FEE2E2 0%, #EF4444 100%)", "score": 5.1, "trend": "→ Brutal Price War", "profit": "$80", "margin": "12%", "fail": True, "note": "Zero Margin — Oversaturated niche on Amazon, advertising cost eats all profit."},
    {"name": "Automatic Electric Jar Opener", "slug": "electric-jar-opener", "category": "KITCHEN & GADGETS", "icon": "🫙", "gradient": "linear-gradient(135deg, #FFEDD5 0%, #EA580C 100%)", "score": 8.1, "trend": "↗ +18% Search Volume", "profit": "$1,100", "margin": "64%"},
    {"name": "DIY Ultrasonic Skin Scrubber", "slug": "skin-scrubber", "category": "BEAUTY & COSMETICS", "icon": "⚠️", "gradient": "linear-gradient(135deg, #FEF2F2 0%, #DC2626 100%)", "score": 3.8, "trend": "↘ Legal / Liability Risk", "profit": "-$400", "margin": "48%", "fail": True, "note": "High Liability — Severe customer complaints regarding skin burns and lack of CE certification."},
    {"name": "Magnetic Desktop Cable Organizer", "slug": "cable-organizer", "category": "OFFICE & PRODUCTIVITY", "icon": "🧲", "gradient": "linear-gradient(135deg, #F5F5F4 0%, #78716C 100%)", "score": 7.9, "trend": "↗ Steady Growth", "profit": "$750", "margin": "70%"},
    {"name": "Ultra-Lightweight Inflatable Camping Pillow", "slug": "camping-pillow", "category": "TRAVEL & OUTDOOR", "icon": "🏕️", "gradient": "linear-gradient(135deg, #D1FAE5 0%, #059669 100%)", "score": 8.5, "trend": "↗ +33% Seasonal Spike", "profit": "$1,320", "margin": "67%"},
    {"name": "Silicone Baby Bibs with Food Catcher", "slug": "baby-bibs", "category": "BABY SUPPLIES", "icon": "👶", "gradient": "linear-gradient(135deg, #FCE7F3 0%, #F472B6 100%)", "score": 8.3, "trend": "↗ High Consistent Demand", "profit": "$980", "margin": "74%"},
    {"name": "Smart Wireless Peephole Camera", "slug": "peephole-camera", "category": "HOME SECURITY", "icon": "📹", "gradient": "linear-gradient(135deg, #DBEAFE 0%, #1D4ED8 100%)", "score": 8.8, "trend": "↗ +52% Year-over-Year", "profit": "$2,450", "margin": "59%"},
)

_SCAN_PRODUCTS: tuple[dict[str, str | float | bool], ...] = (
    {"name": "Flame Effect Essential Oil Diffuser", "slug": "flame-diffuser", "score": 94, "profit": "$14.50", "demand": "+41%", "category": "HOME & DECOR"},
    {"name": "Personalized Pet Travel Harness", "slug": "pet-travel-harness", "score": 91, "profit": "$18.20", "demand": "+22%", "category": "PET SUPPLIES"},
    {"name": "Smart Wireless Peephole Camera", "slug": "peephole-camera", "score": 88, "profit": "$24.50", "demand": "+52%", "category": "HOME SECURITY"},
    {"name": "Portable USB-C Rechargeable Blender", "slug": "usb-blender", "score": 84, "profit": "$9.20", "demand": "+14%", "category": "SMART KITCHEN"},
    {"name": "Silicone Baby Bibs with Food Catcher", "slug": "baby-bibs", "score": 81, "profit": "$9.80", "demand": "+19%", "category": "BABY SUPPLIES"},
    {"name": "Sleep-Tech Smart Scales", "slug": "smart-scale", "score": 76, "profit": "$21.00", "demand": "+22%", "category": "HEALTH & TECH"},
    {"name": "Electric Jar Opener", "slug": "electric-jar-opener", "score": 69, "profit": "$11.00", "demand": "+18%", "category": "KITCHEN"},
    {"name": "Inflatable Camping Pillow", "slug": "camping-pillow", "score": 64, "profit": "$13.20", "demand": "+33%", "category": "OUTDOOR"},
    {"name": "Magnetic Cable Organizer", "slug": "cable-organizer", "score": 52, "profit": "$7.50", "demand": "+6%", "category": "OFFICE"},
    {"name": "Resistance Loop Bands", "slug": "resistance-bands", "score": 44, "profit": "$0.80", "demand": "-12%", "category": "FITNESS"},
    {"name": "Bluetooth Sleep Mask Headphones", "slug": "sleep-mask-headphones", "score": 29, "profit": "-$2.50", "demand": "-28%", "category": "ELECTRONICS"},
    {"name": "Ultrasonic Skin Scrubber", "slug": "skin-scrubber", "score": 18, "profit": "-$4.00", "demand": "-35%", "category": "BEAUTY"},
)

_LIVE_CATALOG_AISLES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("Strong opportunities", "strong", ("flame-diffuser", "pet-travel-harness", "peephole-camera", "usb-blender", "baby-bibs")),
    ("Worth a closer look", "go", ("smart-scale", "electric-jar-opener", "camping-pillow")),
    ("Proceed with caution", "caution", ("cable-organizer",)),
    ("High risk — walk away", "walk", ("resistance-bands", "sleep-mask-headphones", "skin-scrubber")),
)

_LIVE_PRODUCT_BY_SLUG: dict[str, dict[str, str | float | bool]] = {
    str(item["slug"]): item for item in _SCAN_PRODUCTS
}

_FAQ_ITEMS: tuple[tuple[str, str], ...] = (
    (
        "Why doesn't the free tier include live web search?",
        "Live web search runs on every evaluation and adds cost. The free tier uses your product "
        "inputs only and still returns a weighted score, margin math, and red-flag analysis in Sections 1–2.",
    ),
    (
        "What's included in the free report?",
        "Sections 1–2 cover your product profile, core metrics, weighted score, and red-flag analysis. "
        "Premium adds the financial verdict, marketing blueprint, competitor intel, and review sentiment in Sections 3–6.",
    ),
    (
        "When should I upgrade to Premium?",
        "Upgrade when red flags have your attention and you need the math: margin stress-tests, "
        "final verdict, marketing blueprint, live competitor intel, and competitor review sentiment analysis.",
    ),
)

_HERO_AVATAR_IDS: tuple[int, ...] = (12, 32, 45, 68)

_REVIEWS: tuple[tuple[str, str, str], ...] = (
    (
        "Crow Metrics saved me from launching a saturated product. The red-flag section alone was worth it.",
        "Sarah M.",
        "Shopify seller",
    ),
    (
        "Finally an AI tool that doesn't hype everything. The GO/NO-GO verdict is brutally honest.",
        "James K.",
        "Amazon FBA",
    ),
    (
        "I run 3 evaluations a week now. The full report pays for itself on the first product I skipped.",
        "Alex T.",
        "DTC founder",
    ),
)


_ENGINE_SOURCES: tuple[tuple[str, str], ...] = (
    ("Amazon", "https://cdn.simpleicons.org/amazon/FF9900"),
    ("Google Trends", "https://cdn.simpleicons.org/google/4285F4"),
    ("TikTok Ads", "https://cdn.simpleicons.org/tiktok/000000"),
    ("Facebook Ads", "https://cdn.simpleicons.org/facebook/0866FF"),
    ("YouTube Ads", "https://cdn.simpleicons.org/youtube/FF0000"),
    ("AliExpress", "https://cdn.simpleicons.org/aliexpress/FF4747"),
    ("Shopify", "https://cdn.simpleicons.org/shopify/7AB55C"),
)

_ORBIT_RADIUS_PX = 148

_SIGNAL_LAYERS: tuple[tuple[str, str, str], ...] = (
    ("margin", "Margin stress-testing", "Models fees, shipping, and ad spend before you order inventory."),
    ("supplier", "Supplier vetting", "Surfaces MOQ traps, slow ships, and unreliable vendors early."),
    ("ads", "Ad saturation radar", "Spots creative fatigue and rising CPMs in your niche."),
    ("reviews", "Review sentiment mining", "Extracts recurring complaints competitors ignore."),
)

_PLATFORM_STEPS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "1",
        "Add your product",
        "Paste a link or upload an image. Enter cost, sell price, and dimensions.",
        "~60 sec",
        '<span class="cm-step-chip">🔗 Product URL</span><span class="cm-step-chip">📷 Upload image</span>',
    ),
    (
        "2",
        "Crow Metrics investigates",
        "Our engine cross-checks demand, competition, margins, suppliers, and risk signals.",
        "~90 sec",
        '<div class="cm-step-scan"><span class="cm-step-scan-line"></span>🔍 Scanning sources…</div>'
        '<div class="cm-step-scan-tags">Amazon · Trends · Ads · Suppliers</div>',
    ),
    (
        "3",
        "Get your evaluation",
        "Receive a scored report with GO/NO-GO verdict, red flags, and a launch plan.",
        "Instant",
        '<div class="cm-step-result"><strong>86</strong><span>/100</span><em>GO</em></div>'
        '<span class="cm-step-result-link">View full report →</span>',
    ),
)

_SIGNAL_ICONS: dict[str, str] = {
    "margin": "📊",
    "supplier": "🏭",
    "ads": "📡",
    "reviews": "💬",
}


def _platform_signal_html(*, key: str, title: str, body: str) -> str:
    icon = _SIGNAL_ICONS.get(key, "•")
    return (
        f'<div class="cm-platform-signal cm-reveal">'
        f'<span class="cm-platform-signal-icon">{icon}</span>'
        f"<div><p class=\"cm-platform-signal-title\">{html.escape(title)}</p>"
        f'<p class="cm-platform-signal-body">{html.escape(body)}</p></div></div>'
    )


def _platform_orbit_html(*, label: str, logo_url: str, angle: float, index: int) -> str:
    safe_label = html.escape(label)
    safe_logo = html.escape(logo_url, quote=True)
    angle_value = f"{angle:.4f}"
    return (
        f'<span class="cm-platform-orbit" data-orbit-index="{index}" '
        f'style="--orbit-angle:{angle_value}deg">'
        f'<img class="cm-platform-orbit-logo" src="{safe_logo}" alt="" loading="lazy" draggable="false" />'
        f"<span>{safe_label}</span></span>"
    )


def _platform_hub_html() -> str:
    count = len(_ENGINE_SOURCES)
    step = 360.0 / count
    orbits = "".join(
        _platform_orbit_html(
            label=label,
            logo_url=logo_url,
            angle=-90.0 + index * step,
            index=index,
        )
        for index, (label, logo_url) in enumerate(_ENGINE_SOURCES)
    )
    return (
        '<div class="cm-platform-hub cm-reveal" data-cm-hub>'
        '<div class="cm-platform-hub-stage">'
        '<svg class="cm-platform-hub-lines" viewBox="0 0 420 420" aria-hidden="true">'
        '<circle cx="210" cy="210" r="118" fill="none" stroke="rgba(43,89,255,0.12)" stroke-width="1.5" stroke-dasharray="6 8"/>'
        '<circle cx="210" cy="210" r="158" fill="none" stroke="rgba(43,89,255,0.08)" stroke-width="1" stroke-dasharray="4 10"/>'
        "</svg>"
        '<div class="cm-platform-hub-ring cm-platform-hub-ring--outer"></div>'
        '<div class="cm-platform-hub-ring cm-platform-hub-ring--inner"></div>'
        f'<div class="cm-platform-orbit-field" style="--orbit-radius:{_ORBIT_RADIUS_PX}px">{orbits}</div>'
        '<div class="cm-platform-hub-core">Crow<br>Metrics<br>AI</div>'
        "</div>"
        "</div>"
    )


def _platform_step_html(*, num: str, title: str, body: str, timing: str, mock: str) -> str:
    return (
        f'<article class="cm-platform-step cm-reveal">'
        f'<div class="cm-platform-step-top">'
        f'<span class="cm-platform-step-num">{html.escape(num)}</span>'
        f'<span class="cm-platform-step-time">{html.escape(timing)}</span>'
        f"</div>"
        f'<h3 class="cm-platform-step-title">{html.escape(title)}</h3>'
        f'<p class="cm-platform-step-body">{html.escape(body)}</p>'
        f'<div class="cm-platform-step-mock">{mock}</div>'
        f"</article>"
    )


def _install_platform_hub() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            const REPULSE_RADIUS = 112;
            const REPULSE_PUSH = 54;
            const LERP = 0.13;

            function initHub(hub) {
                if (hub.dataset.cmHubReady) return;
                const stage = hub.querySelector(".cm-platform-hub-stage");
                const field = hub.querySelector(".cm-platform-orbit-field");
                const orbits = hub.querySelectorAll(".cm-platform-orbit");
                if (!stage || !field || !orbits.length) return;
                hub.dataset.cmHubReady = "1";

                const pills = Array.prototype.map.call(orbits, function (el) {
                    const angle = parseFloat(el.style.getPropertyValue("--orbit-angle")) || 0;
                    return { el: el, angle: angle, x: 0, y: 0, tx: 0, ty: 0 };
                });

                function orbitRadius() {
                    const raw = win.getComputedStyle(field).getPropertyValue("--orbit-radius").trim();
                    return parseFloat(raw) || 148;
                }

                function setTargets(clientX, clientY) {
                    const rect = stage.getBoundingClientRect();
                    const cx = rect.left + rect.width * 0.5;
                    const cy = rect.top + rect.height * 0.5;
                    const radius = orbitRadius();

                    pills.forEach(function (pill) {
                        const rad = (pill.angle * Math.PI) / 180;
                        const bx = cx + Math.cos(rad) * radius;
                        const by = cy + Math.sin(rad) * radius;
                        const dx = bx - clientX;
                        const dy = by - clientY;
                        const dist = Math.hypot(dx, dy);
                        if (dist < REPULSE_RADIUS && dist > 1) {
                            const falloff = 1 - dist / REPULSE_RADIUS;
                            const force = falloff * falloff * REPULSE_PUSH;
                            pill.tx = (dx / dist) * force;
                            pill.ty = (dy / dist) * force;
                        } else {
                            pill.tx = 0;
                            pill.ty = 0;
                        }
                    });
                }

                function resetTargets() {
                    pills.forEach(function (pill) {
                        pill.tx = 0;
                        pill.ty = 0;
                    });
                }

                function tick() {
                    pills.forEach(function (pill) {
                        pill.x += (pill.tx - pill.x) * LERP;
                        pill.y += (pill.ty - pill.y) * LERP;
                        pill.el.style.setProperty("--repel-x", pill.x.toFixed(2) + "px");
                        pill.el.style.setProperty("--repel-y", pill.y.toFixed(2) + "px");
                    });
                    requestAnimationFrame(tick);
                }
                tick();

                stage.addEventListener("mousemove", function (event) {
                    setTargets(event.clientX, event.clientY);
                });
                stage.addEventListener("mouseleave", resetTargets);
                stage.addEventListener(
                    "touchmove",
                    function (event) {
                        if (!event.touches.length) return;
                        setTargets(event.touches[0].clientX, event.touches[0].clientY);
                    },
                    { passive: true }
                );
                stage.addEventListener("touchend", resetTargets);
                stage.addEventListener("touchcancel", resetTargets);
            }

            function scan() {
                doc.querySelectorAll("[data-cm-hub]").forEach(initHub);
            }

            if (!win.__cmPlatformHub) {
                win.__cmPlatformHub = { scan };
                new MutationObserver(scan).observe(doc.body, { childList: true, subtree: true });
            }
            requestAnimationFrame(function () { requestAnimationFrame(scan); });
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _hero_avatars_html() -> str:
    faces = []
    for avatar_id in _HERO_AVATAR_IDS:
        src = html.escape(f"https://i.pravatar.cc/96?img={avatar_id}", quote=True)
        faces.append(f'<img class="cm-avatar" src="{src}" alt="" loading="lazy" />')
    return f'<span class="cm-avatars" aria-hidden="true">{"".join(faces)}</span>'


def _score_tone(score: int) -> str:
    if score >= 90:
        return "strong"
    if score >= 80:
        return "go"
    if score >= 60:
        return "caution"
    if score >= 40:
        return "risk"
    return "walk"


def _score_verdict(score: int) -> str:
    tone = _score_tone(score)
    return {
        "strong": "Strong GO",
        "go": "GO",
        "caution": "Caution",
        "risk": "High Risk",
        "walk": "Walk Away",
    }[tone]


def _live_product_card_html(*, product: dict[str, str | float | bool], compact: bool = False) -> str:
    score = int(product["score"])
    tone = _score_tone(score)
    slug_raw = str(product["slug"])
    slug = html.escape(slug_raw, quote=True)
    name = html.escape(str(product["name"]))
    category = html.escape(str(product.get("category", "PRODUCT")))
    profit = html.escape(str(product["profit"]))
    demand = html.escape(str(product["demand"]))
    verdict = html.escape(_score_verdict(score))
    image_url = html.escape(carousel_image_data_uri(slug_raw), quote=True)
    profit_class = "is-loss" if str(product["profit"]).strip().startswith("-") else ""

    if compact:
        return (
            f'<button type="button" class="cm-catalog-item cm-reveal" data-ps-sample-slug="{slug_raw}" '
            f'data-score-tier="{tone}">'
            f'<div class="cm-catalog-item-img">'
            f'<img src="{image_url}" alt="{name}" loading="lazy" />'
            f'<span class="cm-catalog-item-score cm-live-card-score--{tone}">{score}</span>'
            f"</div>"
            f'<div class="cm-catalog-item-body">'
            f'<p class="cm-catalog-item-name">{name}</p>'
            f'<p class="cm-catalog-item-tag">{verdict} · {category}</p>'
            f"</div></button>"
        )

    loss_attr = f' class="{profit_class}"' if profit_class else ""
    return (
        f'<button type="button" class="cm-live-card cm-reveal" data-ps-sample-slug="{slug_raw}">'
        f'<span class="cm-live-card-score cm-live-card-score--{tone}">{score}</span>'
        f'<div class="cm-live-card-img">'
        f'<img src="{image_url}" alt="{name}" loading="lazy" draggable="false" />'
        f'<span class="cm-live-card-category">{category}</span>'
        f"</div>"
        f'<div class="cm-live-card-body">'
        f'<p class="cm-live-card-name">{name}</p>'
        f'<span class="cm-live-card-verdict cm-live-card-verdict--{tone}">{verdict}</span>'
        f'<div class="cm-live-card-meta">'
        f"<span>Est. Profit<strong{loss_attr}>{profit}</strong></span>"
        f"<span>Demand<strong>{demand}</strong></span>"
        f"</div>"
        f'<span class="cm-live-card-action">View evaluation →</span>'
        f"</div></button>"
    )


_HERO_PREVIEW_SLUG = "usb-blender"

_HERO_METRICS: tuple[tuple[str, str, int, str], ...] = (
    ("demand", "Market Demand", 92, "blue"),
    ("profit", "Profitability", 85, "blue"),
    ("competition", "Competition", 71, "blue"),
    ("saturation", "Saturation Risk", 38, "amber"),
    ("supplier", "Supplier Score", 82, "blue"),
)

_METRIC_ICONS: dict[str, str] = {
    "demand": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M4 19V5M4 19H20M8 15V11M12 15V7M16 15V9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
        "</svg>"
    ),
    "profit": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M12 3V21M17 8H9.5a2.5 2.5 0 100 5H14a2.5 2.5 0 010 5H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
        "</svg>"
    ),
    "competition": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M16 11c1.66 0 3-1.34 3-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zM8 11c1.66 0 3-1.34 3-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5C15 14.17 10.33 13 8 13zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor"/>'
        "</svg>"
    ),
    "saturation": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M12 3L3 20h18L12 3zm0 6.5a1 1 0 011 1v4a1 1 0 11-2 0v-4a1 1 0 011-1zm-1 8h2v2h-2v-2z" fill="currentColor"/>'
        "</svg>"
    ),
    "supplier": (
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" stroke="currentColor" stroke-width="2"/>'
        "</svg>"
    ),
}


def _eval_metric_row(*, key: str, label: str, score: int, tone: str) -> str:
    tone_class = "is-warn" if tone == "amber" else ""
    icon = _METRIC_ICONS[key]
    safe_label = html.escape(label)
    return (
        f'<button type="button" class="cm-eval-metric cm-eval-click" data-ps-sample-slug="{_HERO_PREVIEW_SLUG}">'
        f'<span class="cm-eval-metric-icon">{icon}</span>'
        f"<div class=\"cm-eval-metric-body\">"
        f'<span class="cm-eval-metric-label">{safe_label}</span>'
        f'<div class="cm-eval-metric-bar"><i class="{tone_class}" data-score="{score}"></i></div>'
        f"</div>"
        f'<span class="cm-eval-metric-score">{score}<span>/100</span></span>'
        f"</button>"
    )


def _hero_card_html() -> str:
    image_url = html.escape(carousel_image_data_uri(_HERO_PREVIEW_SLUG), quote=True)
    slug = html.escape(_HERO_PREVIEW_SLUG, quote=True)
    metrics = "".join(
        _eval_metric_row(key=key, label=label, score=score, tone=tone)
        for key, label, score, tone in _HERO_METRICS
    )
    return (
        '<div class="cm-eval-wrap cm-animate-in cm-animate-in-delay-2">'
        f'<article class="cm-eval-card cm-reveal" data-eval-score="89" aria-label="Sample product evaluation">'
        f'<a class="cm-eval-head cm-eval-click" href="#" data-ps-sample-slug="{slug}" target="_self">'
        f'<img class="cm-eval-thumb" src="{image_url}" alt="Portable USB-C Rechargeable Blender" loading="lazy" />'
        '<div class="cm-eval-meta">'
        '<h3 class="cm-eval-name">Portable USB-C Rechargeable Blender</h3>'
        '<div class="cm-eval-badges">'
        '<span class="cm-eval-badge cm-eval-badge--score">8.4 / 10</span>'
        '<span class="cm-eval-badge cm-eval-badge--trend">↗ +14% Demand this month</span>'
        "</div></div></a>"
        '<div class="cm-eval-financials">'
        '<div class="cm-eval-fin-item">'
        '<span class="cm-eval-fin-label">Est. Net Profit</span>'
        '<strong class="cm-eval-fin-value cm-eval-fin-value--green">$920 / mo</strong>'
        "</div>"
        '<div class="cm-eval-fin-divider" aria-hidden="true"></div>'
        '<div class="cm-eval-fin-item">'
        '<span class="cm-eval-fin-label">Gross Margin</span>'
        '<strong class="cm-eval-fin-value">58%</strong>'
        "</div></div>"
        '<div class="cm-eval-score-panel">'
        '<p class="cm-eval-score-kicker">Overall score</p>'
        '<div class="cm-eval-score-row">'
        '<div class="cm-eval-ring" data-target="89" aria-hidden="true">'
        '<svg class="cm-eval-ring-svg" viewBox="0 0 120 120">'
        '<circle class="cm-eval-ring-track" cx="60" cy="60" r="52" />'
        '<circle class="cm-eval-ring-fill" cx="60" cy="60" r="52" />'
        "</svg>"
        '<span class="cm-eval-ring-value">89</span>'
        "</div>"
        '<div class="cm-eval-verdict">'
        '<p class="cm-eval-verdict-title">High Potential</p>'
        '<p class="cm-eval-verdict-copy">Strong product-market fit with low execution risk.</p>'
        f'<a class="cm-eval-go cm-eval-click" href="#" data-ps-sample-slug="{slug}" target="_self">GO</a>'
        "</div></div></div>"
        f'<div class="cm-eval-metrics">{metrics}</div>'
        f'<a class="cm-eval-footer cm-eval-click" href="#" data-ps-sample-slug="{slug}" target="_self">View Full Report →</a>'
        "</article></div>"
    )


def _report_nav_item(section_num: int, title: str, *, active: bool = False, locked: bool = False) -> str:
    icon = "🔒" if locked else ("●" if active else "○")
    classes = "cm-report-nav-item"
    if active:
        classes += " is-active"
    if locked:
        classes += " is-locked"
    return f'<div class="{classes}"><span>{icon}</span>{html.escape(title)}</div>'


def _install_eval_card_animations() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__cmEvalCardAnim) return;
            win.__cmEvalCardAnim = true;

            const RING_R = 52;
            const RING_C = 2 * Math.PI * RING_R;

            function animateCard(card) {
                if (card.dataset.cmEvalAnimated) return;
                card.dataset.cmEvalAnimated = "1";

                const ring = card.querySelector(".cm-eval-ring-fill");
                const target = parseInt(card.getAttribute("data-eval-score") || "89", 10);
                if (ring) {
                    const offset = RING_C * (1 - target / 100);
                    ring.style.strokeDasharray = RING_C.toFixed(2);
                    ring.style.strokeDashoffset = RING_C.toFixed(2);
                    requestAnimationFrame(function () {
                        ring.style.transition = "stroke-dashoffset 1.35s cubic-bezier(0.22, 1, 0.36, 1)";
                        ring.style.strokeDashoffset = offset.toFixed(2);
                    });
                }

                card.querySelectorAll(".cm-eval-metric-bar i").forEach(function (bar, index) {
                    const score = parseInt(bar.getAttribute("data-score") || "0", 10);
                    bar.style.width = "0%";
                    win.setTimeout(function () {
                        bar.style.width = score + "%";
                    }, 180 + index * 90);
                });

                const valueNode = card.querySelector(".cm-eval-ring-value");
                if (valueNode) {
                    let current = 0;
                    const step = Math.max(1, Math.round(target / 40));
                    const timer = win.setInterval(function () {
                        current += step;
                        if (current >= target) {
                            current = target;
                            win.clearInterval(timer);
                        }
                        valueNode.textContent = String(current);
                    }, 28);
                }
            }

            function bindCard(card) {
                if (card.dataset.cmEvalBound) return;
                card.dataset.cmEvalBound = "1";
                const io = new IntersectionObserver(
                    function (entries) {
                        entries.forEach(function (entry) {
                            if (!entry.isIntersecting) return;
                            animateCard(entry.target);
                            io.unobserve(entry.target);
                        });
                    },
                    { threshold: 0.35 }
                );
                io.observe(card);
            }

            function scan() {
                doc.querySelectorAll(".cm-eval-card").forEach(bindCard);
            }

            scan();
            new MutationObserver(scan).observe(doc.body, { childList: true, subtree: true });

            doc.addEventListener(
                "click",
                function (event) {
                    const clicker = event.target.closest(".cm-eval-click");
                    if (!clicker) return;
                    const card = clicker.closest(".cm-eval-card");
                    if (card) card.classList.add("is-pressed");
                    win.setTimeout(function () {
                        if (card) card.classList.remove("is-pressed");
                    }, 180);
                },
                true
            );
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _install_landing_cta_bridge() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__psLandingCtaInstalled) return;
            win.__psLandingCtaInstalled = true;

            function clickHeroCta(attempt) {
                const tries = attempt || 0;
                const host = doc.querySelector('[class*="st-key-landing_hero_cta"]');
                if (!host) {
                    if (tries < 8) win.setTimeout(function () { clickHeroCta(tries + 1); }, 40);
                    return;
                }
                const button = host.querySelector("button");
                if (!button) {
                    if (tries < 8) win.setTimeout(function () { clickHeroCta(tries + 1); }, 40);
                    return;
                }
                button.click();
            }

            doc.addEventListener(
                "click",
                function (event) {
                    const link = event.target.closest(".cm-cta, .lp-hero-cta");
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


def _install_scroll_reveal() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (!win.__cmReveal) {
                win.__cmReveal = {
                    io: new IntersectionObserver(
                        (entries) => {
                            entries.forEach((entry) => {
                                if (!entry.isIntersecting) return;
                                entry.target.classList.add("is-visible");
                            });
                        },
                        { threshold: 0.12, rootMargin: "0px 0px -4% 0px" }
                    ),
                };
                win.__cmReveal.mo = new MutationObserver(() => win.__cmReveal.scan());
                win.__cmReveal.mo.observe(doc.body, { childList: true, subtree: true });
            }
            win.__cmReveal.scan = function scan() {
                doc.documentElement.classList.add("cm-reveal-ready");
                doc.querySelectorAll(".cm-reveal:not([data-cm-observed])").forEach((node) => {
                    node.dataset.cmObserved = "1";
                    win.__cmReveal.io.observe(node);
                });
            };
            win.__cmReveal.scan();
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _install_scan_carousel() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            const AUTO_SPEED = 0.35;
            const FRICTION = 0.94;
            const MIN_VELOCITY = 0.15;

            function initViewport(viewport) {
                if (viewport.dataset.cmScanReady) return;
                const track = viewport.querySelector(".cm-scan-track");
                if (!track) return;
                viewport.dataset.cmScanReady = "1";

                let position = 0;
                let loopWidth = 0;
                let paused = false;
                let dragging = false;
                let startX = 0;
                let startPos = 0;
                let moved = 0;
                let velocity = 0;
                let lastX = 0;
                let lastTime = 0;
                let momentumId = null;
                let frame = null;

                function measure() {
                    loopWidth = track.scrollWidth / 2;
                    if (!loopWidth) loopWidth = 1;
                }
                function wrap() {
                    while (position <= -loopWidth) position += loopWidth;
                    while (position > 0) position -= loopWidth;
                }
                function render() {
                    track.style.transform = "translate3d(" + position + "px,0,0)";
                }
                function resumeAuto() {
                    if (!dragging && momentumId === null) paused = false;
                }
                function step() {
                    if (!paused && !dragging && momentumId === null) {
                        position -= AUTO_SPEED;
                        wrap();
                        render();
                    }
                    frame = requestAnimationFrame(step);
                }
                function stopMomentum() {
                    if (momentumId !== null) {
                        cancelAnimationFrame(momentumId);
                        momentumId = null;
                    }
                }
                function runMomentum() {
                    let speed = velocity * 18;
                    function tick() {
                        if (Math.abs(speed) < MIN_VELOCITY) {
                            momentumId = null;
                            resumeAuto();
                            return;
                        }
                        position += speed;
                        speed *= FRICTION;
                        wrap();
                        render();
                        momentumId = requestAnimationFrame(tick);
                    }
                    momentumId = requestAnimationFrame(tick);
                }

                viewport.addEventListener("pointerdown", function (event) {
                    if (event.button !== 0 && event.pointerType === "mouse") return;
                    dragging = true;
                    paused = true;
                    moved = 0;
                    startX = event.clientX;
                    startPos = position;
                    lastX = event.clientX;
                    lastTime = performance.now();
                    velocity = 0;
                    stopMomentum();
                    viewport.setPointerCapture(event.pointerId);
                    viewport.classList.add("is-grabbing");
                });
                viewport.addEventListener("pointermove", function (event) {
                    if (!dragging) return;
                    const dx = event.clientX - startX;
                    moved = Math.max(moved, Math.abs(dx));
                    position = startPos + dx;
                    wrap();
                    render();
                    const now = performance.now();
                    const dt = now - lastTime;
                    if (dt > 0) {
                        velocity = (event.clientX - lastX) / dt;
                        lastX = event.clientX;
                        lastTime = now;
                    }
                });
                function endDrag(event) {
                    if (!dragging) return;
                    dragging = false;
                    viewport.classList.remove("is-grabbing");
                    try { viewport.releasePointerCapture(event.pointerId); } catch (_) {}
                    if (moved > 8) {
                        viewport.dataset.cmDragged = "1";
                        win.setTimeout(function () { delete viewport.dataset.cmDragged; }, 120);
                    }
                    if (Math.abs(velocity) > 0.02) {
                        runMomentum();
                    } else {
                        resumeAuto();
                    }
                }
                viewport.addEventListener("pointerup", endDrag);
                viewport.addEventListener("pointercancel", endDrag);
                viewport.addEventListener("mouseenter", function () { paused = true; });
                viewport.addEventListener("mouseleave", function () {
                    dragging = false;
                    stopMomentum();
                    resumeAuto();
                });
                track.addEventListener(
                    "click",
                    function (event) {
                        if (viewport.dataset.cmDragged) {
                            event.preventDefault();
                            event.stopImmediatePropagation();
                        }
                    },
                    true
                );

                measure();
                render();
                frame = requestAnimationFrame(step);
                win.addEventListener("resize", function () { measure(); wrap(); render(); });
            }

            function scan() {
                doc.querySelectorAll(".cm-scan-viewport").forEach(initViewport);
            }
            if (!win.__cmScan) {
                win.__cmScan = { scan };
                new MutationObserver(scan).observe(doc.body, { childList: true, subtree: true });
            }
            requestAnimationFrame(function () { requestAnimationFrame(scan); });
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _install_evaluated_today_ticker(*, day_start_ms: int, target: int) -> None:
    components.html(
        f"""
        <script>
        (function () {{
            const win = window.parent;
            const doc = win.document;
            const DAY_START_MS = {day_start_ms};
            const TARGET = {target};

            function liveCount() {{
                const elapsed = Date.now() - DAY_START_MS;
                const fraction = Math.min(1, Math.max(0, elapsed / 86400000));
                return Math.floor(TARGET * Math.pow(fraction, 0.88));
            }}
            function formatCount(value) {{
                return value.toLocaleString("en-GB");
            }}
            function tick() {{
                const value = liveCount();
                doc.querySelectorAll("[data-cm-eval-today]").forEach(function (el) {{
                    el.textContent = formatCount(value);
                }});
            }}
            if (!win.__cmEvalTicker) {{
                win.__cmEvalTicker = true;
                tick();
                win.setInterval(tick, 15000);
            }} else {{
                tick();
            }}
        }})();
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
            const el = window.parent.document.getElementById("section-{anchor}");
            if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


def render_landing_hero() -> None:
    brand = html.escape(BRAND_NAME)
    st.markdown(
        '<div class="cm-page cm-hero">'
        '<div class="cm-hero-grid">'
        '<div class="cm-hero-copy">'
        '<span class="cm-kicker cm-animate-in">🛡 Brutally honest AI product evaluations</span>'
        '<h1 class="cm-title cm-title--hero cm-animate-in cm-animate-in-delay-1">Know if a<br>product is<br><span class="cm-accent">worth selling.</span></h1>'
        f'<p class="cm-lead cm-animate-in cm-animate-in-delay-2">Stop wasting money on products that look good on paper. {brand} uses real market data from 10+ sources to tell you what to launch — and what to walk away from.</p>'
        '<ul class="cm-hero-bullets cm-animate-in cm-animate-in-delay-2">'
        "<li><span>✓</span> Real data from 10+ sources</li>"
        "<li><span>⚠</span> 100% honest risk analysis</li>"
        "<li><span>⚡</span> Actionable insights in minutes</li>"
        "</ul>"
        '<a class="cm-cta cm-cta--lg cm-animate-in cm-animate-in-delay-3" href="#">Start Your Free Evaluation →</a>'
        '<div class="cm-hero-social cm-animate-in cm-animate-in-delay-4">'
        + _hero_avatars_html()
        + '<span class="cm-stars">★★★★★</span>'
        '<span class="cm-social-text">Join 25,000+ entrepreneurs</span>'
        "</div></div>"
        + _hero_card_html()
        + "</div></div>",
        unsafe_allow_html=True,
    )


def _install_live_catalog_filters() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__cmCatalogFilters) return;
            win.__cmCatalogFilters = true;

            doc.addEventListener(
                "click",
                function (event) {
                    const btn = event.target.closest(".cm-catalog-filter");
                    if (!btn) return;
                    event.preventDefault();
                    const filter = btn.getAttribute("data-filter") || "all";
                    doc.querySelectorAll(".cm-catalog-filter").forEach(function (chip) {
                        chip.classList.toggle("is-active", chip === btn);
                    });
                    doc.querySelectorAll(".cm-catalog-item").forEach(function (item) {
                        const tier = item.getAttribute("data-score-tier") || "";
                        const show = filter === "all" || tier === filter;
                        item.classList.toggle("is-hidden", !show);
                    });
                },
                true
            );
        })();
        </script>
        """,
        height=0,
        width=0,
    )


def _live_catalog_grid_html() -> str:
    catalog_items: list[str] = []
    for aisle_label, _aisle_key, slugs in _LIVE_CATALOG_AISLES:
        catalog_items.append(f'<p class="cm-catalog-aisle cm-reveal">{html.escape(aisle_label)}</p>')
        for slug in slugs:
            product = _LIVE_PRODUCT_BY_SLUG.get(slug)
            if product:
                catalog_items.append(_live_product_card_html(product=product, compact=True))

    filter_chips = (
        '<button type="button" class="cm-catalog-filter is-active" data-filter="all">All products</button>'
        '<button type="button" class="cm-catalog-filter" data-filter="strong">Strong GO</button>'
        '<button type="button" class="cm-catalog-filter" data-filter="go">GO</button>'
        '<button type="button" class="cm-catalog-filter" data-filter="caution">Caution</button>'
        '<button type="button" class="cm-catalog-filter" data-filter="risk">High risk</button>'
        '<button type="button" class="cm-catalog-filter" data-filter="walk">Walk away</button>'
    )

    return (
        '<div class="cm-catalog-head cm-reveal">'
        '<h3 class="cm-catalog-title">Live product <span>marketplace</span></h3>'
        f'<div class="cm-catalog-filters">{filter_chips}</div>'
        "</div>"
        f'<div class="cm-catalog-grid">{"".join(catalog_items)}</div>'
    )


def render_live_scan_section() -> None:
    ticker = evaluated_today_ticker()
    evaluated_label = format_count(ticker["count"])
    carousel_cards = "".join(_live_product_card_html(product=p) for p in _SCAN_PRODUCTS)
    track = f'<div class="cm-scan-track">{carousel_cards}{carousel_cards}</div>'

    st.markdown(
        '<section class="cm-live-market">'
        '<div class="cm-live-inner">'
        '<div class="cm-live-head cm-reveal">'
        '<div class="cm-live-head-main">'
        '<span class="cm-live-pulse"><span class="cm-live-pulse-dot"></span>Live market scan</span>'
        '<h2 class="cm-live-title">Products being evaluated <span>right now</span></h2>'
        '<p class="cm-live-lead">Real products. Real data. Updated continuously — click any card to open a full sample evaluation. Drag the carousel to browse.</p>'
        "</div>"
        '<a class="cm-live-cta-link cm-reveal" href="#" data-ps-nav-action="live_catalog" target="_self">View all live products →</a>'
        "</div>"
        '<div class="cm-live-stats cm-reveal">'
        '<div class="cm-live-stat"><strong>250+</strong><span>Live niches tracked</span></div>'
        f'<div class="cm-live-stat"><strong data-cm-eval-today>{evaluated_label}</strong><span>Evaluated today</span></div>'
        '<div class="cm-live-stat"><strong>94–18</strong><span>Score range (full spread)</span></div>'
        '<div class="cm-live-stat"><strong>~30 sec</strong><span>Per evaluation</span></div>'
        "</div>"
        f'<div class="cm-scan-shell cm-reveal"><div class="cm-scan-viewport">{track}</div></div>'
        "</div></section>",
        unsafe_allow_html=True,
    )
    _install_evaluated_today_ticker(day_start_ms=ticker["day_start_ms"], target=ticker["target"])


def render_live_catalog_page() -> None:
    render_hidden_carousel_sample_buttons()
    install_carousel_sample_bridge()

    st.markdown(
        '<div class="cm-catalog-page">'
        '<div class="cm-page">'
        '<a class="cm-catalog-back cm-reveal" href="#" data-ps-nav-action="home" target="_self">← Back to home</a>'
        '<div class="cm-catalog-page-hero cm-reveal">'
        '<span class="cm-live-pulse"><span class="cm-live-pulse-dot"></span>Live marketplace</span>'
        '<h1 class="cm-catalog-page-title">Live product <span>marketplace</span></h1>'
        '<p class="cm-catalog-page-lead">Browse every niche we are tracking right now. Filter by score tier and click any product to open a full sample evaluation.</p>'
        "</div>"
        f'<div class="cm-live-catalog">{_live_catalog_grid_html()}</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )

    _install_live_catalog_filters()
    _install_scroll_reveal()
    maybe_show_carousel_sample_dialog()


def render_platform_section() -> None:
    signals = "".join(
        _platform_signal_html(key=key, title=title, body=body) for key, title, body in _SIGNAL_LAYERS
    )
    steps = "".join(
        _platform_step_html(num=num, title=title, body=body, timing=timing, mock=mock)
        for num, title, body, timing, mock in _PLATFORM_STEPS
    )

    st.markdown(
        '<section class="cm-platform" id="section-process">'
        '<div class="cm-platform-inner">'
        '<div class="cm-platform-engine">'
        '<div class="cm-platform-head cm-reveal">'
        '<span class="cm-live-pulse"><span class="cm-live-pulse-dot"></span>AI investigation engine</span>'
        '<h2 class="cm-platform-title">We leave no stone unturned. That\'s how we stay <span>brutally honest.</span></h2>'
        '<p class="cm-platform-lead">Before you spend a dollar, our engine cross-references demand signals, ad intelligence, '
        f"supplier data, and competitor sentiment — then runs proprietary checks you won't find in generic research tools.</p>"
        "</div>"
        '<div class="cm-platform-engine-grid">'
        f'<div class="cm-platform-signals">{signals}</div>'
        f"{_platform_hub_html()}"
        "</div>"
        "</div>"
        '<div class="cm-platform-divider cm-reveal" aria-hidden="true"><span>How it works</span></div>'
        '<div class="cm-platform-steps-block">'
        '<div class="cm-platform-steps-head cm-reveal">'
        f'<h3 class="cm-platform-steps-title">Get your product evaluation in <span>3 simple steps</span></h3>'
        f'<p class="cm-platform-steps-lead">From product link to launch decision in under two minutes — no spreadsheets, no guesswork.</p>'
        "</div>"
        f'<div class="cm-platform-steps-track">{steps}</div>'
        "</div>"
        "</div></section>",
        unsafe_allow_html=True,
    )
    _install_platform_hub()


def render_site_stats_bar() -> None:
    brand = html.escape(BRAND_NAME)
    st.markdown(
        '<section class="cm-site-stats cm-reveal">'
        '<div class="cm-site-stats-inner">'
        '<div class="cm-site-stats-brand">'
        '<span class="cm-site-stats-icon">🛡</span>'
        '<p>Brutal by design.<br>Built to save you money.</p>'
        "</div>"
        '<div class="cm-site-stats-grid">'
        '<div class="cm-site-stat"><strong>10M+</strong><span>Data points analyzed daily</span></div>'
        '<div class="cm-site-stat"><strong>70+</strong><span>Proprietary signals</span></div>'
        '<div class="cm-site-stat"><strong>25,000+</strong><span>Entrepreneurs trust us</span></div>'
        '<div class="cm-site-stat"><strong>12+</strong><span>Risk categories screened</span></div>'
        "</div></div>"
        f'<p class="cm-site-stats-foot">{brand} · Built for e-commerce operators who demand the truth</p>'
        "</section>",
        unsafe_allow_html=True,
    )


def render_report_preview() -> None:
    image_url = html.escape(carousel_image_data_uri(_HERO_SLUG), quote=True)
    nav = "".join(
        _report_nav_item(
            s.number,
            s.title.split("&")[0].strip() if "&" in s.title else s.title,
            active=s.number == 1,
            locked=s.number > 2,
        )
        for s in REPORT_SECTIONS
    )
    st.markdown(
        '<section class="cm-section" id="section-sample">'
        '<div class="cm-page">'
        '<div class="cm-section-head cm-reveal">'
        '<span class="cm-kicker">Report preview</span>'
        '<h2 class="cm-title">Here\'s a preview of your <span class="cm-accent">full report</span></h2>'
        f'<p class="cm-lead">Sections 1–2 are free on every evaluation. Upgrade to Premium for the complete 6-section investigation.</p>'
        "</div>"
        '<div class="cm-report-shell cm-reveal">'
        '<div class="cm-report-layout">'
        f'<nav class="cm-report-nav">{nav}</nav>'
        '<div class="cm-report-main">'
        '<div class="cm-report-header">'
        f'<img class="cm-report-product-img" src="{image_url}" alt="Pet Travel Harness" />'
        "<div>"
        '<p style="margin:0;font-weight:700;color:#0A1128">Personalized Pet Travel Harness</p>'
        '<p style="margin:0.25rem 0 0;font-size:0.78rem;color:#64748B">Pet Supplies · Travel niche · Low competition</p>'
        "</div></div>"
        '<div class="cm-report-verdict">'
        '<div><div class="cm-report-verdict-score">86<span style="font-size:0.9rem;color:#059669">/100</span></div>'
        '<p style="margin:0.35rem 0 0;font-size:0.82rem;font-weight:700;color:#047857">GO — Strong Opportunity</p></div>'
        '<p style="margin:0;font-size:0.78rem;color:#059669;font-weight:600">92% confidence</p>'
        "</div>"
        '<div class="cm-report-kpis">'
        '<div class="cm-report-kpi"><label>Est. Profit</label><strong>$15.43/unit</strong></div>'
        '<div class="cm-report-kpi"><label>Margin</label><strong>57%</strong></div>'
        '<div class="cm-report-kpi"><label>Demand</label><strong style="color:#059669">+22%</strong></div>'
        '<div class="cm-report-kpi"><label>Saturation</label><strong>Low</strong></div>'
        '<div class="cm-report-kpi"><label>Overall Risk</label><strong>Low</strong></div>'
        "</div>"
        '<div class="cm-report-charts">'
        '<div class="cm-chart-box"><p class="cm-chart-title">Demand over time</p>'
        '<div class="cm-chart-bars">'
        '<div class="cm-chart-bar" style="height:45%"></div>'
        '<div class="cm-chart-bar" style="height:55%"></div>'
        '<div class="cm-chart-bar" style="height:62%"></div>'
        '<div class="cm-chart-bar" style="height:78%"></div>'
        '<div class="cm-chart-bar" style="height:85%"></div>'
        '<div class="cm-chart-bar" style="height:92%"></div>'
        "</div></div>"
        '<div class="cm-chart-box"><p class="cm-chart-title">Top risk factors</p>'
        '<ul class="cm-risk-list">'
        "<li>⚠ Seasonal spike in Q2 — plan inventory</li>"
        "<li>⚠ 2 competitors undercutting on Amazon</li>"
        "<li>✓ Strong supplier score on AliExpress</li>"
        "</ul></div></div></div></div>"
        '<div class="cm-report-footer">'
        '<a href="#" data-ps-sample-slug="pet-travel-harness" target="_self">View full report sample →</a>'
        "</div></div></div></section>",
        unsafe_allow_html=True,
    )


def render_unlock_premium() -> None:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    free_checks = (
        '<div class="cm-check-row"><span>✓</span> Sections 1–2 (profile + red flags)</div>'
        '<div class="cm-check-row"><span>✓</span> Weighted 5-metric score</div>'
        f'<div class="cm-check-row"><span>✓</span> {FREE_EVALUATIONS_PER_ACCOUNT} free evaluations</div>'
        '<div class="cm-check-row is-no"><span>—</span> Financial GO/NO-GO verdict</div>'
        '<div class="cm-check-row is-no"><span>—</span> Live web intelligence</div>'
    )
    premium_checks = (
        '<div class="cm-check-row"><span>✓</span> All 6 sections unlocked</div>'
        '<div class="cm-check-row"><span>✓</span> Unlimited evaluations</div>'
        '<div class="cm-check-row"><span>✓</span> Full financial matrix</div>'
        '<div class="cm-check-row"><span>✓</span> Marketing blueprint + ad intel</div>'
        '<div class="cm-check-row"><span>✓</span> Competitor sentiment analysis</div>'
    )
    section_cards = ""
    for section in REPORT_SECTIONS:
        locked = section.number > 2
        section_cards += (
            f'<div class="cm-section-mini{" is-locked" if locked else ""}">'
            f'<p class="cm-section-mini-num">Section {section.number}</p>'
            f'<p class="cm-section-mini-title">{html.escape(section.title.split("&")[0].strip())}</p>'
            f"</div>"
        )
    st.markdown(
        f'<section class="cm-section cm-section--tight" id="section-pricing">'
        f'<div class="cm-page">'
        f'<div class="cm-section-head cm-reveal">'
        f'<span class="cm-kicker">Premium</span>'
        f'<h2 class="cm-title">Go beyond the preview. Get the <span class="cm-accent">full investigation</span></h2>'
        f"</div>"
        f'<div class="cm-premium-grid">'
        f'<div class="cm-reveal">'
        f'<div class="cm-premium-checklist" style="margin-bottom:1rem"><h3>Free</h3>{free_checks}</div>'
        f'<div class="cm-premium-checklist"><h3>Premium</h3>{premium_checks}</div>'
        f"</div>"
        f'<div class="cm-section-cards cm-reveal">{section_cards}</div>'
        f"</div>"
        f'<div class="cm-pricing-bar cm-reveal">'
        f'<div class="cm-pricing-points">'
        f"<span>✓ Unlimited product evaluations</span>"
        f"<span>✓ All 6 sections for every report</span>"
        f"<span>✓ Cancel anytime</span>"
        f"</div>"
        f'<div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap">'
        f'<p class="cm-pricing-price">Only ${premium.price_usd_monthly}<span>/month</span></p>'
        f'<a class="cm-cta" href="#">Unlock Full Report →</a>'
        f"</div></div></div></section>",
        unsafe_allow_html=True,
    )


def render_score_legend() -> None:
    st.markdown(
        '<section class="cm-section cm-section--dark">'
        '<div class="cm-page">'
        '<div class="cm-section-head cm-reveal">'
        '<span class="cm-kicker cm-kicker--dark">Scoring</span>'
        '<h2 class="cm-title">Know exactly what your score <span class="cm-accent">means</span></h2>'
        "</div>"
        '<div class="cm-score-cards cm-reveal">'
        '<div class="cm-score-card cm-score-card--strong"><p class="cm-score-range" style="color:#4ADE80">90–100</p>'
        '<p class="cm-score-label">Strong GO</p><p class="cm-score-desc">Exceptional opportunity with strong demand and margins.</p></div>'
        '<div class="cm-score-card cm-score-card--go"><p class="cm-score-range" style="color:#86EFAC">80–89</p>'
        '<p class="cm-score-label">GO</p><p class="cm-score-desc">Strong opportunity — proceed with a clear launch plan.</p></div>'
        '<div class="cm-score-card cm-score-card--caution"><p class="cm-score-range" style="color:#FDE047">60–79</p>'
        '<p class="cm-score-label">Caution</p><p class="cm-score-desc">Potential exists, but weaknesses need attention.</p></div>'
        '<div class="cm-score-card cm-score-card--risk"><p class="cm-score-range" style="color:#FB923C">40–59</p>'
        '<p class="cm-score-label">High Risk</p><p class="cm-score-desc">More risks than rewards — reconsider before investing.</p></div>'
        '<div class="cm-score-card cm-score-card--walk"><p class="cm-score-range" style="color:#F87171">0–39</p>'
        '<p class="cm-score-label">Walk Away</p><p class="cm-score-desc">Low chance of success — save your capital.</p></div>'
        "</div>"
        '<div class="cm-brutal-grid cm-reveal">'
        "<div>"
        '<div class="cm-hero-social" style="margin-bottom:1.5rem">'
        '<span class="cm-avatars"><span class="cm-avatar"></span><span class="cm-avatar cm-avatar--b"></span>'
        '<span class="cm-avatar cm-avatar--c"></span><span class="cm-avatar cm-avatar--d"></span></span>'
        '<span class="cm-stars">★★★★★</span>'
        '<span class="cm-social-text" style="color:#94A3B8">Join 25,000+ entrepreneurs making smarter decisions</span>'
        "</div>"
        '<div class="cm-value-bar">'
        '<div class="cm-value-item"><strong>100% honest</strong>analysis</div>'
        '<div class="cm-value-item"><strong>Data over</strong>opinions</div>'
        '<div class="cm-value-item"><strong>Your success</strong>first</div>'
        "</div></div>"
        '<div class="cm-brutal-card">'
        "<h3>Why so brutal?</h3>"
        "<p>Most tools tell you what you want to hear. Crow Metrics has no bias, no affiliate deals, and no reason to hype a bad product. Just data, patterns, and the brutal truth.</p>"
        "</div></div>"
        '<p class="cm-quote cm-reveal">"The AI that tells you what to do — and what not to do."</p>'
        "</div></section>",
        unsafe_allow_html=True,
    )


def render_reviews_section() -> None:
    cards = []
    for text, author, role in _REVIEWS:
        cards.append(
            f'<div class="cm-review-card cm-reveal">'
            f'<div class="cm-review-stars">★★★★★</div>'
            f'<p class="cm-review-text">{html.escape(text)}</p>'
            f'<div class="cm-review-author">'
            f'<span class="cm-avatar"></span>'
            f"<div><strong>{html.escape(author)}</strong><span>{html.escape(role)}</span></div>"
            f"</div></div>"
        )
    st.markdown(
        '<section class="cm-section" id="section-reviews">'
        '<div class="cm-page">'
        '<div class="cm-section-head cm-reveal">'
        '<span class="cm-kicker">Reviews</span>'
        '<h2 class="cm-title">Trusted by <span class="cm-accent">ecommerce founders</span></h2>'
        "</div>"
        f'<div class="cm-reviews-grid">{"".join(cards)}</div>'
        "</div></section>",
        unsafe_allow_html=True,
    )


def render_faq_section() -> None:
    items = []
    for question, answer in _FAQ_ITEMS:
        items.append(
            f'<details class="cm-faq-item cm-reveal">'
            f"<summary>{html.escape(question)}</summary>"
            f'<p class="cm-faq-answer">{html.escape(answer)}</p>'
            f"</details>"
        )
    st.markdown(
        f'<section class="cm-section cm-section--tight" id="section-resources">'
        f'<div class="cm-page">'
        f'<div class="cm-section-head cm-reveal">'
        f'<span class="cm-kicker">FAQ</span>'
        f'<h2 class="cm-title">Common questions</h2>'
        f"</div>"
        f'<div class="cm-faq-list">{"".join(items)}</div>'
        f"</div></section>",
        unsafe_allow_html=True,
    )


def render_final_cta() -> None:
    st.markdown(
        f'<section class="cm-final cm-reveal">'
        f'<div class="cm-page">'
        f'<h2 class="cm-title">Your first {FREE_EVALUATIONS_PER_ACCOUNT} evaluations are free</h2>'
        f'<p class="cm-lead" style="margin-bottom:1.5rem">No credit card required. Get your brutal truth in ~30 seconds.</p>'
        f'<a class="cm-cta cm-cta--lg" href="#">Start Your Free Evaluation →</a>'
        f"</div></section>",
        unsafe_allow_html=True,
    )


def render_landing_footnote() -> None:
    st.markdown(
        f'<p class="cm-footer cm-reveal">{html.escape(BRAND_NAME)} · Built for e-commerce operators who demand the truth</p>',
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    render_hidden_carousel_sample_buttons()
    install_carousel_sample_bridge()
    _install_landing_cta_bridge()
    render_landing_hero()

    st.markdown('<div class="cm-cta-host">', unsafe_allow_html=True)
    if st.button("Start Free Evaluation →", type="primary", key="landing_hero_cta"):
        request_free_evaluation()
    st.markdown("</div>", unsafe_allow_html=True)

    render_live_scan_section()
    render_platform_section()
    render_report_preview()
    render_unlock_premium()
    render_score_legend()
    render_reviews_section()
    render_faq_section()
    render_final_cta()
    render_site_stats_bar()

    _install_scroll_reveal()
    _install_eval_card_animations()
    _install_scan_carousel()
    _scroll_to_anchor_if_needed()
    maybe_show_carousel_sample_dialog()
