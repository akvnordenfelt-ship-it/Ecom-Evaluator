"""Free-tier limit reached."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.ui.subscription import activate_plan, stripe_checkout_url


def render_paywall_card() -> None:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]

    st.markdown(
        """
        <div class="paywall-card">
            <p class="paywall-kicker">Free evaluation used</p>
            <h2 class="paywall-title">Unlock the full verdict &amp; execution stack</h2>
            <p class="paywall-copy">
                Your free preview covered Sections 1–2 — product profile and red flags.
                Upgrade to Premium to see if the numbers work, how to market it, and where to source it.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="pricing-card pricing-card--premium" style="margin-bottom:0.75rem;">
            <p class="pricing-name">Premium · ${premium.price_usd_monthly}/mo</p>
            <ul class="paywall-list">
                <li>Sections 3–6 — Financial verdict, marketing blueprint, live web intel, 5× video scripts</li>
                <li>Unlimited evaluations</li>
                <li>Powered by our most advanced commercial AI engine</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button(
        f"Upgrade to Premium — ${premium.price_usd_monthly}/mo",
        stripe_checkout_url(PlanTier.PREMIUM),
        type="primary",
        use_container_width=True,
    )
    if st.button("Simulate Premium (dev)", key="sim_premium", use_container_width=True):
        activate_plan(PlanTier.PREMIUM)
        st.rerun()

    if st.button("Back to home", key="paywall_home"):
        st.session_state["app_view"] = "landing"
        st.rerun()
