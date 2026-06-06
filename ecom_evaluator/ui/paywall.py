"""Free-tier limit reached."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.plans import PLAN_CONFIG, PlanTier
from ecom_evaluator.ui.subscription import activate_plan, stripe_checkout_url


def render_paywall_card() -> None:
    premium = PLAN_CONFIG[PlanTier.PREMIUM]
    pro = PLAN_CONFIG[PlanTier.PRO]

    st.markdown(
        """
        <div class="paywall-card">
            <p class="paywall-kicker">Free evaluation used</p>
            <h2 class="paywall-title">Upgrade for live intel &amp; marketing scripts</h2>
            <p class="paywall-copy">
                Your free report covered sections 1–4 — product profile, red flags, margin matrix,
                and marketing teaser. Unlock the rest when you're ready to execute.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_premium, col_pro = st.columns(2)
    with col_premium:
        st.markdown(
            f"""
            <div class="pricing-card pricing-card--premium">
                <p class="pricing-name">Premium · ${premium.price_usd_monthly}/mo</p>
                <p class="pricing-copy">Section 5 — Live web search &amp; sourcing links</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Upgrade Premium", stripe_checkout_url(PlanTier.PREMIUM), use_container_width=True)
        if st.button("Simulate Premium", key="sim_premium", use_container_width=True):
            activate_plan(PlanTier.PREMIUM)
            st.rerun()

    with col_pro:
        st.markdown(
            f"""
            <div class="pricing-card pricing-card--pro">
                <p class="pricing-name">Pro · ${pro.price_usd_monthly}/mo</p>
                <p class="pricing-copy">Sections 5 + 6 — Web intel + marketing blueprint</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("Upgrade Pro", stripe_checkout_url(PlanTier.PRO), use_container_width=True)
        if st.button("Simulate Pro", key="sim_pro", use_container_width=True):
            activate_plan(PlanTier.PRO)
            st.rerun()

    if st.button("Back to home", key="paywall_home"):
        st.session_state["app_view"] = "landing"
        st.rerun()
