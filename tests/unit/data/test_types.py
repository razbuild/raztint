from typing import get_args

from raztint.data import COLORS, INTENTS, STYLES
from raztint.data.types import (
    BackgroundColorName,
    ColorName,
    IconName,
    IntentName,
    StyleName,
)


def test_color_name_literal_matches_palette() -> None:
    expected = {name.lower() for name in COLORS}
    assert set(get_args(ColorName)) == expected


def test_background_name_literal_includes_prefixed_and_short() -> None:
    names = set(get_args(BackgroundColorName))
    assert "red" in names


def test_style_name_literal_matches_styles() -> None:
    expected = {name.lower() for name in STYLES}
    assert set(get_args(StyleName)) == expected


def test_icon_and_intent_literals() -> None:
    assert set(get_args(IconName)) == {"ok", "err", "warn", "info", "pending", "debug"}
    assert set(get_args(IntentName)) == set(INTENTS)
