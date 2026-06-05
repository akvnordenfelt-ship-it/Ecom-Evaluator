"""Streamlit application entry point."""

from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from ecom_evaluator.exceptions import AnalysisError
from ecom_evaluator.groq_client import run_product_evaluation
from ecom_evaluator.settings import has_shared_api_key, resolve_api_key
from ecom_evaluator.ui.dashboard import render_dashboard
from ecom_evaluator.ui.form import render_app_header, render_evaluation_form
from ecom_evaluator.ui.landing import render_landing_page
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
    APP_VIEW_TOOL,
    is_tool_view,
    mark_evaluation_consumed,
    show_paywall,
)
from ecom_evaluator.ui.theme import inject_custom_css
from ecom_evaluator.web_search import run_web_market_research


def _run_analysis_pipeline(data: dict, resolved_key: str) -> None:
    image_bytes: bytes | None = None
    image_mime: str | None = None
    if data["uploaded_file"] is not None:
        image_bytes = data["uploaded_file"].getvalue()
        image_mime = data["uploaded_file"].type

    clear_analysis_error()
    st.session_state["analysis_running"] = True

    try:
        if image_bytes is None:
            st.warning(
                "No product image uploaded — visual and creative scores may be less accurate."
            )

        with st.spinner("Searching Amazon, AliExpress, and the web (DuckDuckGo)…"):
            web_research = run_web_market_research(
                product_name=data["product_name"].strip(),
                description=data["description"].strip(),
            )
        if not web_research:
            st.warning(
                "Web search returned no results — analysis will continue, but market "
                "saturation may be less accurate. Try again in a minute if DuckDuckGo was rate-limited."
            )
        else:
            st.caption(f"Found {len(web_research)} competitor/search snippets.")

        with st.spinner("Shark Tank is analyzing with Groq… This may take 15–45 seconds."):
            result = run_product_evaluation(
                api_key=resolved_key,
                product_name=data["product_name"].strip(),
                purchase_price=data["purchase_price"],
                sales_price=data["sales_price"],
                weight_kg=data["weight_kg"],
                length_cm=data["length_cm"],
                width_cm=data["width_cm"],
                height_cm=data["height_cm"],
                description=data["description"].strip(),
                image_bytes=image_bytes,
                image_mime=image_mime,
                web_research=web_research,
            )

        st.session_state["analysis_result"] = result
        st.session_state["market_research"] = web_research
        st.session_state["analysis_meta"] = {
            "product_name": data["product_name"].strip(),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "web_research": web_research,
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
    render_app_header(hide_api_status=has_shared_api_key())

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
