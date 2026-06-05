"""Free-tier limit reached."""

from __future__ import annotations

import streamlit as st

from ecom_evaluator.config import PAID_TIERS_ENABLED


def render_paywall_card() -> None:
    st.markdown(
        """
        <div class="paywall-card">
            <p class="paywall-kicker">Free evaluation used</p>
            <h2 class="paywall-title">Thanks for trying ProductScore</h2>
            <p class="paywall-copy">
                You've used your free evaluation for this session. Review your report in the
                <strong>Evaluation report</strong> tab, or download it as JSON or Markdown.
            </p>
            <ul class="paywall-list">
                <li>Clear a new session (new browser tab) to run another free eval while we're in beta</li>
                <li>Share feedback — we're improving report quality every week</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if PAID_TIERS_ENABLED:
        st.info("Paid plans are enabled — upgrade options will appear here when Stripe is configured.")
        return

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        if st.button("Back to home", use_container_width=True, key="paywall_back_home"):
            st.session_state["app_view"] = "landing"
            st.rerun()

    st.caption("Paid plans coming soon. For now, focus is on making the free evaluation excellent.")
