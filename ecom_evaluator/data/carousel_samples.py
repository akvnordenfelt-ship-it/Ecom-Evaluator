"""Pre-built sample evaluations for landing-page carousel products."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from ecom_evaluator.llm_normalize import normalize_free_evaluation_payload
from ecom_evaluator.models import ProductEvaluationResponse
from ecom_evaluator.scoring import compute_overall_score


@dataclass(frozen=True)
class CarouselSample:
    slug: str
    product_name: str
    result: ProductEvaluationResponse
    meta: dict


def _metrics(score_10: float, *, fail: bool = False) -> tuple[int, int, int, int, int]:
    target = max(5, min(98, int(round(score_10 * 10))))
    if fail or target <= 45:
        return (
            max(8, target - 12),
            max(5, target - 18),
            max(8, target - 10),
            max(5, target - 15),
            max(10, target - 8),
        )
    return (
        min(98, target + 4),
        max(20, target - 6),
        min(98, target + 2),
        max(20, target - 10),
        max(20, target - 4),
    )


def _build_sample(
    *,
    slug: str,
    name: str,
    score_10: float,
    fail: bool,
    profile: str,
    weight: str,
    fragility: str,
    variants: str,
    shipping: str,
    logistics_note: str,
    saturation_note: str,
    velocity_note: str,
    brand_note: str,
    season_note: str,
    red_headline: str,
    red_analysis: str,
    red_1: str,
    red_2: str,
    red_3: str,
) -> CarouselSample:
    logistics, saturation, velocity, brandability, seasonality = _metrics(score_10, fail=fail)
    payload = normalize_free_evaluation_payload(
        {
            "product_profile_summary": profile,
            "physical_weight_assessment": weight,
            "fragility_assessment": fragility,
            "variant_complexity": variants,
            "shipping_complexity": shipping,
            "metric_logistics_margin": str(logistics),
            "metric_logistics_margin_note": logistics_note,
            "metric_market_saturation": str(saturation),
            "metric_market_saturation_note": saturation_note,
            "metric_marketing_velocity": str(velocity),
            "metric_marketing_velocity_note": velocity_note,
            "metric_brandability": str(brandability),
            "metric_brandability_note": brand_note,
            "metric_seasonality": str(seasonality),
            "metric_seasonality_note": season_note,
            "red_flag_headline": red_headline,
            "red_flag_analysis": red_analysis,
            "red_flag_1": red_1,
            "red_flag_2": red_2,
            "red_flag_3": red_3,
        }
    )
    result = ProductEvaluationResponse.model_validate(payload)
    expected = compute_overall_score(logistics, saturation, velocity, brandability, seasonality)
    assert result.overall_score == expected
    return CarouselSample(
        slug=slug,
        product_name=name,
        result=result,
        meta={
            "product_name": name,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "sample_slug": slug,
            "is_demo_sample": True,
        },
    )


_CAROUSEL_SAMPLES: dict[str, CarouselSample] = {
    sample.slug: sample
    for sample in (
        _build_sample(
            slug="flame-diffuser",
            name="Flame Effect Essential Oil Diffuser",
            score_10=8.9,
            fail=False,
            profile=(
                "Aromatherapy diffuser with LED flame simulation for cozy home decor. Strong gift appeal, "
                "compact footprint, and visually demo-friendly for short-form video."
            ),
            weight="Light unit (~0.4 kg) keeps parcel costs low and supports healthy contribution margin.",
            fragility="Glass reservoir and electronics need foam inserts; otherwise moderate fragility.",
            variants="Low — color/finish variants only.",
            shipping="Small-parcel friendly; poly mailer with corner protection is sufficient.",
            logistics_note="Strong markup potential with lightweight shipping profile.",
            saturation_note="Crowded diffuser niche, but flame-effect angle still has room on TikTok.",
            velocity_note="High organic demo potential — flame visual hooks stop the scroll.",
            brand_note="Brandable as a cozy-home gift line with repeat scent consumables.",
            season_note="Year-round with Q4 gift spike.",
            red_headline="Differentiate before Amazon clones arrive",
            red_analysis="Winners in this niche lead with creative and bundle strategy, not hardware alone.",
            red_1="Generic diffuser listings compress price within 90 days of viral spikes.",
            red_2="Leakage/PSU failures drive 1-star reviews if QC is weak.",
            red_3="Essential-oil compliance claims can trigger ad disapprovals if copy is sloppy.",
        ),
        _build_sample(
            slug="pet-travel-harness",
            name="Personalized Pet Travel Harness",
            score_10=9.2,
            fail=False,
            profile=(
                "Customizable pet travel harness with name patch — strong emotional purchase driver for "
                "dog owners and travel seasonality."
            ),
            weight="Light apparel-style SKU; inexpensive to ship in mailers.",
            fragility="Low fragility; main risk is sizing exchanges.",
            variants="Medium — sizes and embroidery colors multiply SKUs.",
            shipping="Standard small parcel; personalization adds handling time not weight.",
            logistics_note="Healthy margins on lightweight personalized SKU.",
            saturation_note="Pet personalization remains fragmented vs commodity harnesses.",
            velocity_note="UGC-friendly — unboxing with pet name reveal performs well.",
            brand_note="Strong repeat and referral potential in pet-owner communities.",
            season_note="Summer travel peak plus holiday gifting.",
            red_headline="Ops complexity from personalization",
            red_analysis="Demand is real; margin leaks come from returns and fulfillment errors.",
            red_1="Wrong size/name errors destroy reviews and drive costly remakes.",
            red_2="Turnaround time must be honest in listings to avoid chargebacks.",
            red_3="Embroidery MOQs can trap cash if ads scale before proof.",
        ),
        _build_sample(
            slug="sleep-mask-headphones",
            name="Cheap Bluetooth Sleep Mask Headphones",
            score_10=4.2,
            fail=True,
            profile=(
                "Low-cost sleep mask with integrated Bluetooth speakers — high return category with "
                "unreliable electronics and comfort complaints."
            ),
            weight="Light but electronics add return/refurb risk.",
            fragility="Electronics + fabric combo increases defect rate.",
            variants="Low SKU count; commodity black variants dominate.",
            shipping="Cheap to ship; return shipping destroys economics.",
            logistics_note="Thin margin after returns and warranty replacements.",
            saturation_note="Hyper-saturated with identical Alibaba listings.",
            velocity_note="Hard to demo differentiation — looks like every other mask ad.",
            brand_note="Commodity gadget with no defensible brand story.",
            season_note="Mild Q4 gift lift does not fix unit economics.",
            red_headline="Return rate will eat the business",
            red_analysis="This is a classic race-to-the-bottom electronics accessory play.",
            red_1="Battery failures reported within weeks on low-tier units.",
            red_2="Bluetooth pairing frustration drives 1–3★ review clusters.",
            red_3="Ad costs exceed contribution margin once creative fatigue hits.",
        ),
        _build_sample(
            slug="usb-blender",
            name="Portable USB-C Rechargeable Blender",
            score_10=8.4,
            fail=False,
            profile=(
                "Compact personal blender for smoothies on the go — strong demo content and gym/office use cases."
            ),
            weight="Moderate weight; still parcel-friendly.",
            fragility="Motor/base seals must survive shipping drops.",
            variants="Color variants only.",
            shipping="Small box with molded insert recommended.",
            logistics_note="Solid margin if motor quality holds and returns stay low.",
            saturation_note="Competitive but still room for lifestyle positioning.",
            velocity_note="Smoothie prep demos perform on TikTok/Reels.",
            brand_note="Can build a fitness/on-the-go micro-brand.",
            season_note="Steady year-round with New Year fitness bump.",
            red_headline="Motor quality makes or breaks reviews",
            red_analysis="Category winners invest in blade/motor QC and leak-proof gaskets.",
            red_1="Seal failures cause leakage complaints and returns.",
            red_2="Battery degradation after 60–90 days triggers negative reviews.",
            red_3="Counterfeit competitors undercut price on identical-looking units.",
        ),
        _build_sample(
            slug="smart-scale",
            name="Sleep-Tech Smart Scales (Cloud Sync)",
            score_10=8.7,
            fail=False,
            profile="App-connected body scale with sleep/recovery positioning — health tech with subscription upsell potential.",
            weight="Heavier SKU but still shippable; dimensional weight watch-out.",
            fragility="Glass top — requires rigid packaging.",
            variants="Black/white plus app tiers.",
            shipping="Requires corner-protected box; not mailer-safe.",
            logistics_note="Acceptable margin at premium price if breakage rate stays low.",
            saturation_note="Scale category crowded; app experience is the differentiator.",
            velocity_note="Transformation and unboxing content can work with influencer angles.",
            brand_note="App ecosystem enables retention if sync is reliable.",
            season_note="Strong Q1 health resolutions and Q4 gifting.",
            red_headline="App reliability is the product",
            red_analysis="Hardware is commoditized — software sync and trust win retention.",
            red_1="Bluetooth/Wi-Fi pairing failures dominate negative reviews in category.",
            red_2="Glass breakage in shipping erodes margin fast.",
            red_3="Health-data privacy messaging must be airtight for ad approval.",
        ),
        _build_sample(
            slug="resistance-bands",
            name="Heavy Latex Resistance Loop Bands",
            score_10=5.1,
            fail=True,
            profile="Commodity fitness bands — brutal Amazon price war and near-zero differentiation.",
            weight="Very light shipping; margin problem is price not logistics.",
            fragility="Latex durability varies; snap failures are common on cheap stock.",
            variants="Multi-pack tension levels — still commodity.",
            shipping="Cheapest parcel class available.",
            logistics_note="Logistics are fine; selling price is the problem.",
            saturation_note="One of the most overcrowded fitness subcategories online.",
            velocity_note="Hard to create novel creative — every ad looks the same.",
            brand_note="No durable brand moat without proprietary material or program.",
            season_note="January spike cannot offset CAC year-round.",
            red_headline="Zero-margin red ocean",
            red_analysis="Unless you own audience or unique programming, this is a NO-GO.",
            red_1="Amazon Basics and clones anchor price near cost.",
            red_2="Paid ads rarely profitable above break-even CAC.",
            red_3="Latex allergy/snap failures create liability and returns.",
        ),
        _build_sample(
            slug="electric-jar-opener",
            name="Automatic Electric Jar Opener",
            score_10=8.1,
            fail=False,
            profile="Senior-friendly kitchen gadget with clear problem/solution hook — strong gift and QVC-style demo angle.",
            weight="Moderate handheld appliance weight.",
            fragility="Low; rigid plastic body.",
            variants="Single SKU with color packaging variants.",
            shipping="Small box; no oversized freight.",
            logistics_note="Problem-solution products support premium pricing vs cost.",
            saturation_note="Niche is narrower than generic kitchen gadgets.",
            velocity_note="Before/after jar opening demos convert older buyers on Facebook.",
            brand_note="Giftable utility item with word-of-mouth in senior communities.",
            season_note="Mother's Day and holiday gifting spikes.",
            red_headline="Audience targeting matters more than virality",
            red_analysis="Works when creative speaks to seniors/caregivers, not TikTok trends.",
            red_1="Torque claims must match real jar lids or reviews punish you.",
            red_2="Battery/compatibility confusion in listings drives returns.",
            red_3="Copycat listings appear quickly after any viral spike.",
        ),
        _build_sample(
            slug="skin-scrubber",
            name="DIY Ultrasonic Skin Scrubber",
            score_10=3.8,
            fail=True,
            profile="Consumer-grade ultrasonic skin spatula — liability-heavy beauty device with burn/compatibility complaints.",
            weight="Light handheld device.",
            fragility="Electronics + water exposure increases failure modes.",
            variants="Low; white/silver commodity shells.",
            shipping="Small parcel; return rate is the killer.",
            logistics_note="Margin looks OK until returns and chargebacks hit.",
            saturation_note="Crowded beauty tool space with aggressive claims.",
            velocity_note="Before/after skin content faces ad policy scrutiny.",
            brand_note="Weak brand trust without clinical backing or certifications.",
            season_note="Minor gift-season lift does not fix liability profile.",
            red_headline="Liability and certification risk",
            red_analysis="This SKU profile is structurally risky for new sellers.",
            red_1="Burn/irritation complaints are common on unbranded ultrasonic tools.",
            red_2="CE/FDA-adjacent claims in ads can trigger bans and legal exposure.",
            red_3="Chargebacks spike when results do not match aggressive creative.",
        ),
        _build_sample(
            slug="cable-organizer",
            name="Magnetic Desktop Cable Organizer",
            score_10=7.9,
            fail=False,
            profile="Minimalist desk accessory for cable management — low COGS, clear utility, office/WFH audience.",
            weight="Very light; ideal mailer product.",
            fragility="Low; adhesive/magnet attachment is main failure point.",
            variants="Color + pack-size bundles.",
            shipping="Poly mailer or small box.",
            logistics_note="Excellent logistics/margin profile for lightweight accessory.",
            saturation_note="Moderate competition but still room for bundle positioning.",
            velocity_note="Satisfying desk-setup reels perform on TikTok.",
            brand_note="Bundle with desk aesthetic can build a micro productivity brand.",
            season_note="Steady WFH demand year-round.",
            red_headline="Adhesive failure drives bad reviews",
            red_analysis="Win on magnet/adhesive QA and bundle creative, not hardware complexity.",
            red_1="Weak adhesives fail on textured desks — visible in 3★ reviews.",
            red_2="Magnets too weak for thick USB-C cables.",
            red_3="Commodity clones undercut within weeks on Amazon.",
        ),
        _build_sample(
            slug="camping-pillow",
            name="Ultra-Lightweight Inflatable Camping Pillow",
            score_10=8.5,
            fail=False,
            profile="Compact inflatable camp pillow — seasonal outdoor niche with ultralight backpacker appeal.",
            weight="Extremely light; excellent shipping economics.",
            fragility="Valve/seam quality determines return rate.",
            variants="Colors and stuff-sack bundles.",
            shipping="Mailer-friendly; smallest packed volume wins SEO.",
            logistics_note="Strong contribution margin on lightweight outdoor SKU.",
            saturation_note="Outdoor accessory niche with identifiable sub-segments.",
            velocity_note="Pack-size comparison content works in hiking communities.",
            brand_note="Can anchor a small outdoor sleep comfort line.",
            season_note="Strong spring/summer spike; plan inventory accordingly.",
            red_headline="Valve QC determines refund rate",
            red_analysis="Outdoor buyers punish leaky valves harshly in reviews.",
            red_1="Slow leaks after 3–5 uses appear in competitor review patterns.",
            red_2="Oversized packed dimensions trigger 'not ultralight' complaints.",
            red_3="Seasonality concentrates cash flow in short windows.",
        ),
        _build_sample(
            slug="baby-bibs",
            name="Silicone Baby Bibs with Food Catcher",
            score_10=8.3,
            fail=False,
            profile="Silicone feeding bib with crumb catcher — staple baby SKU with repeat purchase and gift potential.",
            weight="Light and durable; mailer-friendly.",
            fragility="Very low; silicone is robust.",
            variants="Colors and multi-packs drive AOV.",
            shipping="Cheap small parcel shipping.",
            logistics_note="Healthy margins on lightweight baby consumable-adjacent SKU.",
            saturation_note="Competitive but parents buy on safety/material trust.",
            velocity_note="Messy baby meal demos are relatable parent content.",
            brand_note="Bundle packs build brand in registry/gift segments.",
            season_note="Consistent demand with baby-shower gifting peaks.",
            red_headline="Material safety messaging must be perfect",
            red_analysis="Parents forgive price less than they forgive unclear material claims.",
            red_1="BPA/phthalate claims must match lab documentation.",
            red_2="Stiff silicone neck openings drive sizing returns.",
            red_3="Amazon private-label packs compress price on multi-bibs.",
        ),
        _build_sample(
            slug="peephole-camera",
            name="Smart Wireless Peephole Camera",
            score_10=8.8,
            fail=False,
            profile="Door peephole replacement camera with app alerts — security upsell with clear renter/homeowner use case.",
            weight="Moderate electronics weight.",
            fragility="Electronics + install kit; packaging must protect lens.",
            variants="Model variants by door thickness and app tier.",
            shipping="Small box with foam; not oversized.",
            logistics_note="Premium price supports decent contribution if install UX is smooth.",
            saturation_note="Security niche growing; differentiation via install ease.",
            velocity_note="Install demo + package theft angle performs in homeowner creative.",
            brand_note="Subscription/cloud features can extend LTV if trust is established.",
            season_note="Year-round with crime-news-driven spikes.",
            red_headline="Install friction kills conversion",
            red_analysis="Security products live or die on setup reliability and app reviews.",
            red_1="Door compatibility issues dominate 1–2★ reviews in category.",
            red_2="Cloud subscription upsell must be transparent or chargebacks follow.",
            red_3="Privacy concerns require crisp data-handling copy.",
        ),
    )
}


def get_carousel_sample(slug: str) -> CarouselSample | None:
    return _CAROUSEL_SAMPLES.get(slug)


def list_carousel_sample_slugs() -> tuple[str, ...]:
    return tuple(_CAROUSEL_SAMPLES.keys())
