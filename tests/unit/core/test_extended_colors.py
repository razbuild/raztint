"""Unit tests for True Color (rgb / hex_color) and 256-color functions."""

import pytest

from raztint.core import RazTint

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def t() -> RazTint:
    inst = RazTint()
    inst.set_color(True)
    return inst


@pytest.fixture
def t_off() -> RazTint:
    inst = RazTint()
    inst.set_color(False)
    return inst


# ── rgb() ─────────────────────────────────────────────────────────────────────


def test_rgb_produces_truecolor_escape(t: RazTint) -> None:
    result = t.rgb("hello", 255, 100, 50)
    assert "\033[38;2;255;100;50m" in result
    assert "hello" in result


def test_rgb_resets_after_text(t: RazTint) -> None:
    result = t.rgb("hello", 0, 200, 0)
    assert result.endswith("\033[0m")


def test_rgb_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.rgb("hello", 255, 0, 0) == "hello"


def test_rgb_invalid_channel_raises() -> None:
    t = RazTint()
    t.set_color(True)
    with pytest.raises(ValueError, match="RGB channel"):
        t.rgb("x", 300, 0, 0)
    with pytest.raises(ValueError, match="RGB channel"):
        t.rgb("x", 0, -1, 0)


# ── bg_rgb() ──────────────────────────────────────────────────────────────────


def test_bg_rgb_produces_truecolor_escape(t: RazTint) -> None:
    result = t.bg_rgb("hello", 255, 100, 50)
    assert "\033[48;2;255;100;50m" in result
    assert "hello" in result


def test_bg_rgb_resets_background_only(t: RazTint) -> None:
    result = t.bg_rgb("hello", 0, 0, 255)
    assert result.endswith("\033[49m")


def test_bg_rgb_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.bg_rgb("hello", 0, 0, 255) == "hello"


# ── hex_color() ───────────────────────────────────────────────────────────────


def test_hex_color_parses_correctly(t: RazTint) -> None:
    # #FF6432 → r=255, g=100, b=50
    result = t.hex_color("hello", "#FF6432")
    assert "\033[38;2;255;100;50m" in result


def test_hex_color_lowercase(t: RazTint) -> None:
    result = t.hex_color("hello", "#ff6432")
    assert "\033[38;2;255;100;50m" in result


def test_hex_color_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.hex_color("hello", "#FF6432") == "hello"


def test_hex_color_invalid_raises() -> None:
    t = RazTint()
    t.set_color(True)
    with pytest.raises(ValueError, match="6-digit hex"):
        t.hex_color("x", "#FFF")
    with pytest.raises(ValueError, match="Invalid hex"):
        t.hex_color("x", "#GGGGGG")


# ── bg_hex_color() ────────────────────────────────────────────────────────────


def test_bg_hex_color_produces_background_escape(t: RazTint) -> None:
    result = t.bg_hex_color("hello", "#FF6432")
    assert "\033[48;2;255;100;50m" in result


def test_bg_hex_color_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.bg_hex_color("hello", "#FF6432") == "hello"


# ── color256() ────────────────────────────────────────────────────────────────


def test_color256_produces_256_escape(t: RazTint) -> None:
    result = t.color256("hello", 208)
    assert "\033[38;5;208m" in result
    assert "hello" in result


def test_color256_resets_after_text(t: RazTint) -> None:
    result = t.color256("hello", 208)
    assert result.endswith("\033[0m")


def test_color256_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.color256("hello", 208) == "hello"


def test_color256_invalid_index_raises() -> None:
    t = RazTint()
    t.set_color(True)
    with pytest.raises(ValueError, match="256-color index"):
        t.color256("x", 256)
    with pytest.raises(ValueError, match="256-color index"):
        t.color256("x", -1)


# ── bg_color256() ─────────────────────────────────────────────────────────────


def test_bg_color256_produces_256_bg_escape(t: RazTint) -> None:
    result = t.bg_color256("hello", 208)
    assert "\033[48;5;208m" in result


def test_bg_color256_resets_background_only(t: RazTint) -> None:
    result = t.bg_color256("hello", 208)
    assert result.endswith("\033[49m")


def test_bg_color256_no_color_returns_plain(t_off: RazTint) -> None:
    assert t_off.bg_color256("hello", 208) == "hello"


# ── Composition with existing styles ─────────────────────────────────────────


def test_rgb_composes_with_bold(t: RazTint) -> None:
    inner = t.rgb("hello", 0, 200, 0)
    result = t.bold(inner)
    assert "\033[38;2;0;200;0m" in result
    assert "\033[1m" in result


def test_rgb_wraps_color256(t: RazTint) -> None:
    inner = t.color256("hello", 208)
    result = t.rgb(inner, 255, 255, 255)
    assert "\033[38;2;255;255;255m" in result
    assert "\033[38;5;208m" in result


# ── Module-level imports ──────────────────────────────────────────────────────


def test_module_level_rgb_importable() -> None:
    from raztint import bg_color256, bg_hex_color, bg_rgb, color256, hex_color, rgb

    assert callable(rgb)
    assert callable(bg_rgb)
    assert callable(hex_color)
    assert callable(bg_hex_color)
    assert callable(color256)
    assert callable(bg_color256)


def test_module_level_rgb_no_crash() -> None:
    from raztint import rgb

    result = rgb("test", 100, 150, 200)
    assert "test" in result
