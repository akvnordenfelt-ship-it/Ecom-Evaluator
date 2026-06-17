"""Local carousel product images for the landing page slideshow."""

from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path

STATIC_CAROUSEL_DIR = Path(__file__).resolve().parent.parent / "static" / "carousel"

CAROUSEL_IMAGE_SLUGS: tuple[str, ...] = (
    "flame-diffuser",
    "pet-travel-harness",
    "sleep-mask-headphones",
    "usb-blender",
    "smart-scale",
    "resistance-bands",
    "electric-jar-opener",
    "skin-scrubber",
    "cable-organizer",
    "camping-pillow",
    "baby-bibs",
    "peephole-camera",
)


def carousel_image_path(slug: str) -> Path | None:
    """Return the on-disk image path for a carousel product slug."""
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = STATIC_CAROUSEL_DIR / f"{slug}{ext}"
        if path.is_file():
            return path
    return None


@lru_cache(maxsize=len(CAROUSEL_IMAGE_SLUGS))
def carousel_image_data_uri(slug: str) -> str:
    """Inline data URI for HTML carousel cards."""
    path = carousel_image_path(slug)
    if path is None:
        return ""
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"
