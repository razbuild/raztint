import pytest

from raztint.core.ansi import (
    apply_background,
    apply_bg_color256,
    apply_bg_rgb,
    apply_color,
    apply_color256,
    apply_rgb,
    apply_style,
)


class TestAnsiHelpers:
    def test_apply_color_disabled(self) -> None:
        assert apply_color("x", "31", use_color=False) == "x"

    def test_apply_color_enabled(self) -> None:
        assert apply_color("x", "31", use_color=True) == "\033[31mx\033[0m"

    def test_apply_background_enabled(self) -> None:
        assert apply_background("x", "44", use_color=True) == "\033[44mx\033[49m"

    def test_apply_style_enabled(self) -> None:
        assert apply_style("x", "1", "22", use_color=True) == "\033[1mx\033[22m"

    @pytest.mark.parametrize(
        ("helper", "args", "expected"),
        [
            (apply_rgb, (12, 34, 56), "\033[38;2;12;34;56mx\033[0m"),
            (apply_bg_rgb, (12, 34, 56), "\033[48;2;12;34;56mx\033[49m"),
            (apply_color256, (123,), "\033[38;5;123mx\033[0m"),
            (apply_bg_color256, (123,), "\033[48;5;123mx\033[49m"),
        ],
    )
    def test_extended_color_enabled(self, helper, args, expected) -> None:
        assert helper("x", *args, use_color=True) == expected

    @pytest.mark.parametrize(
        ("helper", "args"),
        [
            (apply_rgb, (12, 34, 56)),
            (apply_bg_rgb, (12, 34, 56)),
            (apply_color256, (123,)),
            (apply_bg_color256, (123,)),
        ],
    )
    def test_extended_color_disabled(self, helper, args) -> None:
        assert helper("x", *args, use_color=False) == "x"
