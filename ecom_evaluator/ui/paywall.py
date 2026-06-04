"""Premium upgrade paywall."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.ui.subscription import stripe_checkout_url


def render_paywall_card() -> None:
    st.markdown(
        """
        <div class="paywall-card">
            <p class="paywall-kicker">You've used your free evaluation</p>
            <h2 class="paywall-title">Upgrade to Premium</h2>
            <p class="paywall-copy">
                Unlock unlimited product scans, priority analysis, and advanced TikTok hook variants —
                built for serious e-commerce operators.
            </p>
            <ul class="paywall-list">
                <li>Unlimited evaluations</li>
                <li>Faster analysis queue</li>
                <li>Advanced TikTok hooks &amp; GTM exports</li>
                <li>Priority support</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button(
            "Subscribe via Stripe",
            stripe_checkout_url(),
            type="primary",
            use_container_width=True,
        )
    with col_b:
        if st.button("Back to home", use_container_width=True, key="paywall_back_home"):
            st.session_state["app_view"] = "landing"
            st.rerun()

    st.caption("Payments are simulated until your Stripe Checkout link is configured in secrets.")
