"""Heuristic validation for product names before running an evaluation."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ecom_evaluator.product_links import ProductLinkInfo

_PRODUCT_EXAMPLES = (
    "Portable neck fan",
    "Magnetic drawing board for kids",
    "Silicone kitchen utensil set",
)

# Words that are never valid alone — food, profanity, test junk, etc.
_NON_PRODUCT_TERMS: frozenset[str] = frozenset(
    {
        "potato",
        "tomato",
        "banana",
        "apple",
        "orange",
        "carrot",
        "broccoli",
        "pizza",
        "burger",
        "coffee",
        "water",
        "beer",
        "wine",
        "jesus",
        "christ",
        "god",
        "allah",
        "buddha",
        "satan",
        "devil",
        "hello",
        "world",
        "test",
        "testing",
        "demo",
        "sample",
        "example",
        "product",
        "item",
        "thing",
        "stuff",
        "something",
        "nothing",
        "random",
        "asdf",
        "qwerty",
        "abc",
        "xyz",
        "foo",
        "bar",
        "baz",
        "name",
        "user",
        "admin",
        "password",
        "lol",
        "haha",
        "yes",
        "no",
        "ok",
        "okay",
        "help",
        "please",
        "thanks",
        "money",
        "cash",
        "rich",
        "poor",
        "love",
        "hate",
        "sex",
        "porn",
        "nude",
        "fuck",
        "shit",
    }
)

# Too vague to identify a sellable SKU without more context.
_VAGUE_PRODUCT_TERMS: frozenset[str] = frozenset(
    {
        "doodle",
        "doodles",
        "gadget",
        "gadgets",
        "gizmo",
        "toy",
        "toys",
        "gift",
        "gifts",
        "item",
        "items",
        "product",
        "products",
        "thing",
        "things",
        "stuff",
        "accessory",
        "accessories",
        "device",
        "devices",
        "tool",
        "tools",
        "kit",
        "kits",
        "gear",
        "merch",
        "novelty",
        "cool",
        "nice",
        "good",
        "best",
        "new",
        "sale",
        "shop",
        "store",
        "brand",
        "widget",
        "object",
        "creation",
        "invention",
        "idea",
        "concept",
        "art",
        "craft",
        "crafts",
        "draw",
        "drawing",
        "sketch",
        "sketches",
    }
)

_GENERIC_MODIFIERS: frozenset[str] = frozenset(
    {
        "wireless",
        "portable",
        "smart",
        "mini",
        "small",
        "large",
        "cheap",
        "premium",
        "digital",
        "electric",
        "automatic",
        "manual",
        "rechargeable",
        "waterproof",
        "organic",
        "natural",
        "custom",
        "personalized",
        "cute",
        "luxury",
        "professional",
        "magnetic",
        "usb",
        "led",
    }
)

_GIBBERISH_RE = re.compile(r"^[a-z]{1,2}$|^[b-df-hj-np-tv-xz]{4,}$", re.IGNORECASE)
_REPEAT_CHAR_RE = re.compile(r"(.)\1{3,}")
_VOWEL_RE = re.compile(r"[aeiouy]", re.IGNORECASE)
_MIN_WORDS_WITHOUT_URL = 2


@dataclass(frozen=True)
class ProductNameValidation:
    ok: bool
    message: str | None = None


def validate_product_name(
    raw_name: str,
    *,
    product_link: ProductLinkInfo | None = None,
    description: str = "",
) -> ProductNameValidation:
    """Reject vague or non-product inputs before calling the AI evaluator."""
    _ = description  # Description alone must not bypass title requirements.
    name = " ".join(raw_name.split())
    if not name:
        return ProductNameValidation(ok=False, message="Enter a product name.")

    lowered = name.lower()
    words = [re.sub(r"[^a-z0-9]+", "", word) for word in lowered.split()]
    words = [word for word in words if word]

    if product_link is not None and len(name) >= 2:
        return ProductNameValidation(ok=True)

    if len(name) < 3:
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="Product names must be at least 3 characters.",
            ),
        )

    if _REPEAT_CHAR_RE.search(lowered) or _looks_like_keyboard_mash(lowered):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="That input looks like random characters rather than a product listing.",
            ),
        )

    if len(words) < _MIN_WORDS_WITHOUT_URL:
        word = words[0] if words else lowered
        if word in _NON_PRODUCT_TERMS or word in _VAGUE_PRODUCT_TERMS:
            reason = (
                f'"{name}" is too vague to evaluate. ProductScore needs a specific product '
                "you could source and sell — not a generic word or category."
            )
        else:
            reason = (
                f'"{name}" is not specific enough. Enter at least two words describing the '
                "actual product (for example, \"magnetic drawing board\"), or paste a supplier listing URL."
            )
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(entered=name, reason=reason),
        )

    if any(word in _NON_PRODUCT_TERMS for word in words):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="That input does not describe a sellable e-commerce product.",
            ),
        )

    if all(word in _GENERIC_MODIFIERS or word in _VAGUE_PRODUCT_TERMS for word in words):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="Add the actual product type so we know what you want evaluated.",
            ),
        )

    if not any(_is_specific_word(word) for word in words):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason=(
                    "We still cannot tell what this product actually is. "
                    "Use a concrete listing-style title or paste a supplier URL."
                ),
            ),
        )

    return ProductNameValidation(ok=True)


def product_name_error_message(
    raw_name: str,
    *,
    product_link: ProductLinkInfo | None = None,
    description: str = "",
) -> str | None:
    """Return a user-facing error string, or None when the name is acceptable."""
    result = validate_product_name(
        raw_name,
        product_link=product_link,
        description=description,
    )
    return result.message if not result.ok else None


def _is_specific_word(word: str) -> bool:
    if word in _NON_PRODUCT_TERMS or word in _VAGUE_PRODUCT_TERMS or word in _GENERIC_MODIFIERS:
        return False
    if word.isdigit():
        return False
    return len(word) >= 4 or (len(word) == 3 and word not in {"pad", "cup", "box", "bag", "hat", "pen"})


def _looks_like_keyboard_mash(text: str) -> bool:
    compact = re.sub(r"[^a-z]", "", text.lower())
    if len(compact) < 4:
        return False
    if _GIBBERISH_RE.match(compact):
        return True
    vowels = len(_VOWEL_RE.findall(compact))
    return vowels == 0 and len(compact) >= 4


def _invalid_name_message(*, entered: str, reason: str) -> str:
    examples = ", ".join(f"**{example}**" for example in _PRODUCT_EXAMPLES)
    suggestion = _suggest_name(entered)
    lines = [
        "**We can't evaluate that input.**",
        "",
        reason,
        "",
        f'You entered: "{entered}"',
        "",
        "ProductScore only runs on identifiable products — not guesses. "
        "Use a specific listing-style title such as "
        f"{examples}.",
    ]
    if suggestion and suggestion.lower() != entered.lower():
        lines.extend(["", f"Did you mean **{suggestion}**?"])
    lines.extend(
        [
            "",
            "Or paste an AliExpress / Amazon listing URL so we can read the real product context.",
        ]
    )
    return "\n".join(lines)


def _suggest_name(entered: str) -> str | None:
    cleaned = " ".join(entered.split())
    if not cleaned:
        return None

    replacements = {
        "doodle": "magnetic drawing board for kids",
        "doodles": "magnetic drawing board for kids",
        "earbud": "wireless earbud case",
        "earbuds": "wireless earbuds",
        "blender": "portable USB blender",
        "fan": "portable neck fan",
        "collar": "LED pet safety collar",
        "spatula": "silicone kitchen spatula set",
        "diffuser": "flame effect essential oil diffuser",
        "harness": "personalized pet travel harness",
        "gadget": "portable phone stand with wireless charger",
        "toy": "STEM building block set for ages 6+",
    }
    lowered = cleaned.lower()
    for key, suggestion in replacements.items():
        if key == lowered or (key in lowered.split() and len(cleaned.split()) == 1):
            return suggestion.title() if cleaned.islower() else suggestion
    return None
