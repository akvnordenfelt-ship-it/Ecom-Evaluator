"""Tests for landing carousel images and sample evaluations."""

from ecom_evaluator.data.carousel_samples import get_carousel_sample, list_carousel_sample_slugs
from ecom_evaluator.ui.carousel_assets import CAROUSEL_IMAGE_SLUGS, carousel_image_data_uri, carousel_image_path
from ecom_evaluator.ui.landing import _CAROUSEL_PRODUCTS


def test_carousel_slugs_match_landing_products():
    landing_slugs = {str(product["slug"]) for product in _CAROUSEL_PRODUCTS}
    sample_slugs = set(list_carousel_sample_slugs())
    image_slugs = set(CAROUSEL_IMAGE_SLUGS)
    assert landing_slugs == sample_slugs == image_slugs


def test_every_carousel_product_has_image_and_sample():
    for slug in CAROUSEL_IMAGE_SLUGS:
        assert carousel_image_path(slug) is not None
        data_uri = carousel_image_data_uri(slug)
        assert data_uri.startswith("data:image/")
        sample = get_carousel_sample(slug)
        assert sample is not None
        assert sample.result.overall_score is not None
        assert sample.result.product_profile_summary


def test_sample_scores_align_with_carousel_cards():
    by_slug = {str(product["slug"]): product for product in _CAROUSEL_PRODUCTS}
    for slug in list_carousel_sample_slugs():
        product = by_slug[slug]
        sample = get_carousel_sample(slug)
        assert sample is not None
        expected_fail = bool(product.get("fail"))
        assert (sample.result.overall_score < 50) == expected_fail
