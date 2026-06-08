"""Streamlit application entry point."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from ecom_evaluator.auth.oauth import handle_oauth_callback, install_oauth_callback_bridge
from ecom_evaluator.auth.session import auth_is_required, is_authenticated, sync_user_evaluation_quota
from ecom_evaluator.economics import resolve_product_inputs
from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.gemini_client import run_product_evaluation
from ecom_evaluator.plans import get_plan_config
from ecom_evaluator.settings import resolve_api_key
from ecom_evaluator.ui.auth_screen import render_auth_screen
from ecom_evaluator.ui.dashboard import render_dashboard
from ecom_evaluator.ui.form import render_evaluation_form
from ecom_evaluator.ui.landing import render_landing_page
from ecom_evaluator.ui.navbar import render_site_navbar
from ecom_evaluator.ui.session import (
    clear_analysis_error,
    friendly_analysis_error,
    init_session_state,
    mark_analysis_for_rate_limit,
    render_analysis_error,
    set_analysis_error,
    validate_inputs,
)
from ecom_evaluator.ui.subscription import (
    APP_VIEW_AUTH,
    APP_VIEW_TOOL,
    get_subscription_tier,
    is_tool_view,
    mark_evaluation_consumed,
    show_paywall,
)
from ecom_evaluator.ui.theme import inject_custom_css


def _run_analysis_pipeline(data: dict, resolved_key: str) -> None:
    image_bytes: bytes | None = None
    image_mime: str | None = None
    if data["uploaded_file"] is not None:
        image_bytes = data["uploaded_file"].getvalue()
        image_mime = data["uploaded_file"].type

    resolved = resolve_product_inputs(
        purchase_price=data["purchase_price"],
        sales_price=data["sales_price"],
        weight_kg=data["weight_kg"],
        length_cm=data["length_cm"],
        width_cm=data["width_cm"],
        height_cm=data["height_cm"],
    )

    clear_analysis_error()
    st.session_state["analysis_running"] = True
    tier = get_subscription_tier()
    plan = get_plan_config(tier)

    try:
        if resolved.used_physical_baseline:
            st.info(
                "No weight or dimensions provided — using a lightweight package baseline "
                "(0.15 kg, 15×10×5 cm) for shipping estimates."
            )
        if resolved.used_sales_price_estimate:
            st.info(
                f"No selling price provided — estimating ${resolved.sales_price:.2f} "
                "(3× purchase cost) for margin calculations."
            )
        if image_bytes is None:
            st.warning(
                "No product image uploaded — profile and velocity scores may be less accurate."
            )

        if plan.runs_web_search:
            st.caption("Premium: full report with live web search and marketing engine.")

        with st.spinner("Running product evaluation…"):
            result = run_product_evaluation(
                api_key=resolved_key,
                product_name=data["product_name"].strip(),
                purchase_price=resolved.purchase_price,
                sales_price=resolved.sales_price,
                weight_kg=resolved.weight_kg,
                length_cm=resolved.length_cm,
                width_cm=resolved.width_cm,
                height_cm=resolved.height_cm,
                description=data["description"].strip(),
                image_bytes=image_bytes,
                image_mime=image_mime,
                web_research=None,
                tier=tier,
                used_physical_baseline=resolved.used_physical_baseline,
                used_sales_price_estimate=resolved.used_sales_price_estimate,
            )

        st.session_state["analysis_result"] = result
        st.session_state["analysis_meta"] = {
            "product_name": data["product_name"].strip(),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "purchase_price": resolved.purchase_price,
            "sales_price": resolved.sales_price,
            "weight_kg": resolved.weight_kg,
            "length_cm": resolved.length_cm,
            "width_cm": resolved.width_cm,
            "height_cm": resolved.height_cm,
            "used_physical_baseline": resolved.used_physical_baseline,
            "used_sales_price_estimate": resolved.used_sales_price_estimate,
            "subscription_tier": tier.value,
        }
        mark_analysis_for_rate_limit(data)
        mark_evaluation_consumed()
        st.session_state["app_view"] = APP_VIEW_TOOL
        st.session_state["analysis_running"] = False
        st.rerun()
    except AnalysisError as exc:
        set_analysis_error(friendly_analysis_error(str(exc)))
    except Exception as exc:
        set_analysis_error(
            f"Something unexpected went wrong: {exc}\n\n"
            "**Tip:** Check your internet connection and try again."
        )
    finally:
        st.session_state["analysis_running"] = False


def main() -> None:
    st.set_page_config(
        page_title="ProductScore — E-commerce Evaluator",
        page_icon="🦈",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    init_session_state()
    inject_custom_css(saas_mode=True)

    install_oauth_callback_bridge()
    if handle_oauth_callback():
        st.rerun()

    render_site_navbar()

    if auth_is_required() and not is_authenticated():
        view = st.session_state.get("app_view", "landing")
        if view == APP_VIEW_AUTH:
            render_auth_screen()
        else:
            render_landing_page()
        return

    sync_user_evaluation_quota()

    if not is_tool_view():
        render_landing_page()
        return

    has_report = st.session_state.get("analysis_result") is not None

    if has_report:
        tab_report, tab_inputs = st.tabs(["Evaluation report", "Product inputs"])
        with tab_inputs:
            data = render_evaluation_form(compact=True)
            render_analysis_error()
        with tab_report:
            meta = st.session_state.get("analysis_meta") or {}
            render_dashboard(st.session_state["analysis_result"], meta)
    else:
        data = render_evaluation_form(compact=False)

    render_analysis_error()

    resolved_key = resolve_api_key(data["api_key"])

    if data["run_analysis"]:
        clear_analysis_error()
        if show_paywall():
            return
        if st.session_state.get("analysis_running"):
            st.warning("An analysis is already running. Please wait for it to finish.")
        else:
            errors = validate_inputs(data)
            if errors:
                st.error("Fix these items before running:")
                for err in errors:
                    st.markdown(f"- {err}")
            else:
                _run_analysis_pipeline(data, resolved_key)


if __name__ == "__main__":
    main()
