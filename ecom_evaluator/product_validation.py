"""Heuristic validation for product names before running an evaluation."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ecom_evaluator.product_links import ProductLinkInfo

_PRODUCT_EXAMPLES = (
    "Portable neck fan",
    "Silicone kitchen utensil set",
    "LED pet safety collar",
)

# Single-word inputs that are clearly not e-commerce product titles.
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

# Generic adjectives/nouns that need a product noun beside them.
_GENERIC_MODIFIERS: frozenset[str] = frozenset(
    {
        "wireless",
        "portable",
        "smart",
        "mini",
        "small",
        "large",
        "best",
        "new",
        "cool",
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
    }
)

_GIBBERISH_RE = re.compile(r"^[a-z]{1,2}$|^[b-df-hj-np-tv-xz]{4,}$", re.IGNORECASE)
_REPEAT_CHAR_RE = re.compile(r"(.)\1{3,}")
_VOWEL_RE = re.compile(r"[aeiouy]", re.IGNORECASE)


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
    name = " ".join(raw_name.split())
    if not name:
        return ProductNameValidation(ok=False, message="Enter a product name.")

    lowered = name.lower()
    words = [word for word in lowered.split() if word]

    if product_link is not None and len(name) >= 2:
        return ProductNameValidation(ok=True)

    if len(description.strip()) >= 24 and len(name) >= 3:
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

    if len(words) == 1:
        word = words[0]
        if word in _NON_PRODUCT_TERMS:
            return ProductNameValidation(
                ok=False,
                message=_invalid_name_message(
                    entered=name,
                    reason=(
                        f'"{name}" is not a sellable product title. ProductScore evaluates items '
                        "you could realistically source and sell online."
                    ),
                ),
            )
        if word in _GENERIC_MODIFIERS:
            return ProductNameValidation(
                ok=False,
                message=_invalid_name_message(
                    entered=name,
                    reason=(
                        f'"{name}" is too vague on its own. Add the product type '
                        '(for example, "portable neck fan" or "wireless earbud case").'
                    ),
                ),
            )
        if word.isalpha() and len(word) <= 10 and not _VOWEL_RE.search(word):
            return ProductNameValidation(
                ok=False,
                message=_invalid_name_message(
                    entered=name,
                    reason="That does not look like a recognizable product name.",
                ),
            )
        if word.isalpha() and len(word) <= 12:
            return ProductNameValidation(
                ok=False,
                message=_invalid_name_message(
                    entered=name,
                    reason=(
                        "Use a specific product title with at least two words when possible "
                        "(category + item), or paste a supplier listing URL below."
                    ),
                ),
            )

    if len(words) == 2 and all(word in _GENERIC_MODIFIERS for word in words):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="Add the actual product type so we know what you want evaluated.",
            ),
        )

    if all(word in _NON_PRODUCT_TERMS for word in words):
        return ProductNameValidation(
            ok=False,
            message=_invalid_name_message(
                entered=name,
                reason="Those words do not describe a product you can evaluate for e-commerce.",
            ),
        )

    return ProductNameValidation(ok=True)


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
        reason,
        "",
        f'You entered: "{entered}"',
        "",
        "Try a specific product title such as "
        f"{examples}.",
    ]
    if suggestion and suggestion.lower() != entered.lower():
        lines.extend(["", f"Did you mean **{suggestion}**?"])
    lines.extend(
        [
            "",
            "Tip: Paste an AliExpress or Amazon listing URL below — we can infer product details from the link.",
        ]
    )
    return "\n".join(lines)


def _suggest_name(entered: str) -> str | None:
    cleaned = " ".join(entered.split())
    if not cleaned:
        return None

    replacements = {
        "earbud": "wireless earbud case",
        "earbuds": "wireless earbuds",
        "blender": "portable USB blender",
        "fan": "portable neck fan",
        "collar": "LED pet safety collar",
        "spatula": "silicone kitchen spatula set",
        "diffuser": "flame effect essential oil diffuser",
        "harness": "personalized pet travel harness",
    }
    lowered = cleaned.lower()
    for key, suggestion in replacements.items():
        if key in lowered and len(cleaned.split()) == 1:
            return suggestion.title() if cleaned.islower() else suggestion
    return None
