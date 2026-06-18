"""Landing carousel sample evaluation dialog and click bridge."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from ecom_evaluator.data.carousel_samples import get_carousel_sample, list_carousel_sample_slugs
from ecom_evaluator.ui.carousel_assets import carousel_image_path
from ecom_evaluator.ui.dashboard import render_section_1, render_section_2


def render_hidden_carousel_sample_buttons() -> None:
    for slug in list_carousel_sample_slugs():
        if st.button(f"__PSSAMPLE_{slug}__", key=f"ps_sample_{slug}"):
            st.session_state["carousel_sample_slug"] = slug
            st.rerun()


def install_carousel_sample_bridge() -> None:
    components.html(
        """
        <script>
        (function () {
            const win = window.parent;
            const doc = win.document;
            if (win.__psCarouselSampleInstalled) return;
            win.__psCarouselSampleInstalled = true;

            function clickSampleSlug(slug, attempt) {
                const tries = attempt || 0;
                const host = doc.querySelector('[class*="st-key-ps_sample_' + slug + '"]');
                if (!host) {
                    if (tries < 8) {
                        win.setTimeout(function () {
                            clickSampleSlug(slug, tries + 1);
                        }, 40);
                    }
                    return false;
                }
                const button = host.querySelector("button");
                if (!button) {
                    if (tries < 8) {
                        win.setTimeout(function () {
                            clickSampleSlug(slug, tries + 1);
                        }, 40);
                    }
                    return false;
                }
                button.click();
                return true;
            }

            doc.addEventListener(
                "click",
                function (event) {
                    const target = event.target.closest("[data-ps-sample-slug]");
                    if (!target) return;
                    event.preventDefault();
                    event.stopImmediatePropagation();
                    const slug = target.getAttribute("data-ps-sample-slug");
                    if (slug) clickSampleSlug(slug, 0);
                },
                true
            );
        })();
        </script>
        """,
        height=0,
        width=0,
    )


@st.dialog("Sample evaluation", width="large")
def _carousel_sample_dialog(slug: str) -> None:
    sample = get_carousel_sample(slug)
    if sample is None:
        st.error("Sample report not found for this product.")
        return

    st.markdown(f"### {sample.product_name}")
    st.caption("Demo report — Sections 1–2 only. Run your own evaluation for live, product-specific results.")

    image_path = carousel_image_path(slug)
    if image_path is not None:
        st.image(str(image_path), use_container_width=True)

    render_section_1(sample.result)
    st.divider()
    render_section_2(sample.result)

    if st.button("Close sample", key=f"close_carousel_sample_{slug}", use_container_width=True):
        st.session_state.pop("carousel_sample_slug", None)
        st.rerun()


def maybe_show_carousel_sample_dialog() -> None:
    slug = st.session_state.get("carousel_sample_slug")
    if slug:
        _carousel_sample_dialog(str(slug))
