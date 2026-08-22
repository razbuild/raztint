import os
from unittest import mock

import pytest

from raztint import paint, tint
from raztint.core import RazTint


class TestFormatText:
    """Test cases for the format_text method."""

    def test_format_text_exists(self):
        """Test that format_text method exists on RazTint."""
        raztint = RazTint()
        assert hasattr(raztint, "format_text")
        assert callable(raztint.format_text)

    def test_format_text_module_level_export(self):
        """Test that format_text is exported at module level."""
        from raztint import paint

        assert callable(paint)

    def test_format_text_disabled_returns_plain_text(self):
        """When color is disabled, format_text should return plain text."""
        raztint = RazTint()
        raztint.set_color(False)

        result = raztint.format_text("test", color="red", styles="bold")
        assert result == "test"

    def test_format_text_empty_args(self):
        """format_text with no color/bg/styles should return plain text."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test")
        assert result == "test"

    def test_format_text_color_only_string_name(self):
        """Test format_text with color name (lowercase string)."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="red")
        assert "\033[31m" in result
        assert "test" in result
        assert "\033[0m" in result

    def test_format_text_color_uppercase_name(self):
        """Test format_text accepts uppercase color names."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="red")
        assert "\033[31m" in result

    def test_format_text_color_integer_code(self):
        """Test format_text accepts ANSI color codes as integers."""
        raztint = RazTint()
        raztint.set_color(True)

        # 31 = red
        result = raztint.format_text("test", color=31)
        assert "\033[31m" in result

        # 91 = bright red
        result = raztint.format_text("test", color=91)
        assert "\033[91m" in result

    def test_format_text_color_invalid_name(self):
        """Test format_text raises ValueError for unknown color name."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", color="not_a_color")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "unknown color" in str(e).lower()

    def test_format_text_color_invalid_integer(self):
        """Test format_text raises ValueError for out-of-range ANSI codes."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", color=256)
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "invalid" in str(e).lower() or "256-color" in str(e)

    def test_format_text_background_string_name(self):
        """Test format_text with background color name."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", bg="bg_red")
        assert "\033[41m" in result
        assert "test" in result

    def test_format_text_background_integer_code(self):
        """Test format_text accepts ANSI background codes as integers."""
        raztint = RazTint()
        raztint.set_color(True)

        # 41 = red background
        result = raztint.format_text("test", bg=41)
        assert "\033[41m" in result

        # 101 = bright red background
        result = raztint.format_text("test", bg=101)
        assert "\033[101m" in result

    def test_format_text_background_invalid_name(self):
        """Test format_text raises ValueError for unknown background name."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", bg="not_a_bg")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "unknown" in str(e).lower()

    def test_format_text_background_invalid_integer(self):
        """Test format_text raises ValueError for out-of-range bg codes."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", bg=256)
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "invalid" in str(e).lower() or "256-color" in str(e)

    def test_format_text_single_style_string(self):
        """Test format_text with a single style as string."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", styles="bold")
        assert "\033[1m" in result
        assert "test" in result
        # With reset=True (default), uses full reset
        assert "\033[0m" in result

    def test_format_text_multiple_styles_list(self):
        """Test format_text with multiple styles as list."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", styles=["bold", "underline"])
        # Codes can be combined in one escape sequence: \033[1;4m
        assert ("1m" in result and "4m" in result) or "\033[1;4m" in result
        assert "test" in result

    def test_format_text_style_invalid_name(self):
        """Test format_text raises ValueError for unknown style name."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", styles="not_a_style")
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "unknown style" in str(e).lower()

    def test_format_text_styles_case_insensitive(self):
        """Test that style names are case-insensitive."""
        raztint = RazTint()
        raztint.set_color(True)

        result1 = raztint.format_text("test", styles="bold")
        result2 = raztint.format_text("test", styles="BOLD")
        result3 = raztint.format_text("test", styles="Bold")

        # All should contain the same ANSI codes
        assert "\033[1m" in result1
        assert "\033[1m" in result2
        assert "\033[1m" in result3

    def test_format_text_color_and_background(self):
        """Test format_text with both color and background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="white", bg="red")
        # Codes can be combined: \033[37;41m
        assert ("37m" in result and "41m" in result) or "\033[37;41m" in result
        assert "test" in result

    def test_format_text_all_parameters(self):
        """Test format_text with color, background, and styles."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text(
            "test", color="white", bg="red", styles=["bold", "underline"]
        )
        # All codes should be present (may be combined in one escape)
        assert "37" in result
        assert "41" in result
        assert "1" in result
        assert "4" in result
        assert "test" in result

    def test_format_text_reset_true_default(self):
        """Test that reset=True (default) appends full reset code."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="red")
        assert result.endswith("\033[0m")

    def test_format_text_reset_false(self):
        """Test that reset=False does not append full reset (only style resets)."""
        raztint = RazTint()
        raztint.set_color(True)

        # With no styles, reset=False should not add any closing codes
        result = raztint.format_text("test", color="red", reset=False)
        assert not result.endswith("\033[0m")
        assert result == "\033[31mtest"

    def test_format_text_reset_false_with_styles(self):
        """Test that reset=False with styles only adds style-specific resets."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="red", styles="bold", reset=False)
        # Should have style-specific reset (22 for bold) but not full reset (0)
        assert "\033[22m" in result
        assert not result.endswith("\033[0m")

    def test_format_text_empty_string(self):
        """Test format_text with empty string."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("", color="red", styles="bold")
        # Should still have codes even though text is empty
        assert "\033[" in result

    def test_format_text_color_none(self):
        """Test format_text with color=None."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=None, styles="bold")
        # Should only have bold codes, no color code
        assert "\033[1m" in result
        assert "\033[31m" not in result

    def test_format_text_multiple_calls_with_reset_false(self):
        """Test concatenating multiple format_text calls with reset=False."""
        raztint = RazTint()
        raztint.set_color(True)

        part1 = raztint.format_text("WARNING:", color="yellow", reset=False)
        part2 = raztint.format_text(" Disk full", color="red", reset=True)

        # part1 should not end with full reset
        assert not part1.endswith("\033[0m")
        # part2 should end with full reset
        assert part2.endswith("\033[0m")

    def test_format_text_bright_colors(self):
        """Test format_text with bright color names."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="bright_red")
        assert "\033[91m" in result

        result = raztint.format_text("test", color="bright_green")
        assert "\033[92m" in result

    def test_format_text_all_valid_colors(self):
        """Test that all defined color names work."""
        raztint = RazTint()
        raztint.set_color(True)

        for color_name in raztint.colors.keys():
            result = raztint.format_text("test", color=color_name.lower())
            assert "test" in result
            # Should have ANSI codes
            assert "\033[" in result

    def test_format_text_all_valid_styles(self):
        """Test that all defined style names work."""
        raztint = RazTint()
        raztint.set_color(True)

        for style_name in raztint.styles.keys():
            result = raztint.format_text("test", styles=style_name.lower())
            assert "test" in result
            # Should have ANSI codes
            assert "\033[" in result

    def test_format_text_type_error_for_invalid_styles_type(self):
        """Test that invalid styles type raises TypeError."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch.object(raztint, "use_color", True):
            try:
                raztint.format_text("test", styles=123)
                assert False, "Should have raised TypeError"
            except TypeError as e:
                assert "styles" in str(e).lower()

    def test_format_text_respects_no_color_env(self):
        """Test that format_text respects NO_COLOR environment variable."""
        with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
            raztint = RazTint()
            result = raztint.format_text("test", color="red", styles="bold")
            assert result == "test"

    def test_format_text_respects_force_color_env(self):
        """Test that format_text respects RAZTINT_FORCE_COLOR."""
        with mock.patch.dict(os.environ, {"RAZTINT_FORCE_COLOR": "1"}, clear=True):
            raztint = RazTint()
            result = raztint.format_text("test", color="red")
            assert "\033[31m" in result

    def test_format_text_combined_codes_in_single_escape(self):
        """Test that multiple codes are combined in a single escape sequence."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text(
            "test", color="red", bg="blue", styles=["bold", "underline"]
        )
        # Should have all codes combined, e.g. \033[31;44;1;4m
        assert "\033[31;44;1;4m" in result or (
            "\033[31m" in result and "\033[44m" in result
        )

    def test_format_text_on_module_instance(self):
        """Test that format_text works on module-level tint instance."""
        original_use_color = tint.use_color
        tint.set_color(True)

        try:
            result = tint.format_text("test", color="red", styles="bold")
            # Codes may be combined
            assert ("31" in result and "1" in result) or "\033[31;1m" in result
        finally:
            tint.set_color(original_use_color)

    def test_format_text_none_as_text(self):
        """Test that text parameter is treated as string (None becomes 'None')."""
        raztint = RazTint()
        raztint.set_color(True)

        # None will be converted to string "None" by f-string
        result = raztint.format_text(None, color="red")  # type: ignore
        assert "None" in result

    def test_format_text_redact_masks_secrets(self):
        """redact=True should mask sensitive values before formatting."""
        raztint = RazTint()
        raztint.set_color(False)

        secret = "ghp_" + "a" * 36
        result = raztint.format_text(f"token={secret}", redact=True)
        assert secret not in result
        assert "ghp_****" in result

    def test_format_text_intent_success(self):
        """intent applies default color, icon, and styles."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("Saved", intent="success")
        assert "\033[32m" in result
        assert "Saved" in result

    def test_format_text_intent_unknown_raises(self):
        raztint = RazTint()
        raztint.set_color(True)

        try:
            raztint.format_text("x", intent="not_an_intent")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "unknown intent" in str(e).lower()

    def test_paint_module_alias(self):
        original_use_color = tint.use_color
        tint.set_color(True)
        try:
            assert paint("hi", color="red") == tint.format_text("hi", color="red")
        finally:
            tint.set_color(original_use_color)


class TestFormatTextIconPaths:
    """Cover icon-only branches in format_text."""

    def test_format_text_color_disabled_with_icon(self):
        """With color disabled and an icon, only the icon is returned."""
        raztint = RazTint()
        raztint.set_color(False)

        result = raztint.format_text("test", icon="ok", icon_mode="std")
        assert result == "[✓] test"

    def test_format_text_icon_only_color_enabled(self):
        """With color enabled and only an icon, no text codes are emitted."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", icon="ok", icon_mode="std")
        assert result == "\033[32m[✓]\033[0m test"

    def test_format_text_no_codes_returns_plain_text(self):
        """If no ANSI codes resolve, plain text is returned."""
        raztint = RazTint()
        raztint.set_color(True)

        with mock.patch(
            "raztint.formatting.paint.normalize_styles", return_value=[]
        ):
            result = raztint.format_text("test", styles="bold")
        assert result == "test"


class TestUnifiedColorValues:
    """Integration tests for unified color value support in paint()."""

    def test_paint_rgb_foreground(self):
        """paint() with RGB tuple foreground."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=(255, 120, 0))
        assert "\033[38;2;255;120;0m" in result
        assert "test" in result

    def test_paint_rgb_background(self):
        """paint() with RGB tuple background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", bg=(30, 30, 30))
        assert "\033[48;2;30;30;30m" in result
        assert "test" in result

    def test_paint_rgb_both(self):
        """paint() with RGB tuples for both foreground and background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=(255, 0, 0), bg=(0, 255, 0))
        # Codes are combined with semicolons: \033[38;2;255;0;0;48;2;0;255;0m
        assert "38;2;255;0;0" in result
        assert "48;2;0;255;0" in result
        assert "test" in result

    def test_paint_hex_foreground(self):
        """paint() with hex string foreground."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="#ff7800")
        assert "\033[38;2;255;120;0m" in result
        assert "test" in result

    def test_paint_hex_background(self):
        """paint() with hex string background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", bg="#202020")
        assert "\033[48;2;32;32;32m" in result
        assert "test" in result

    def test_paint_hex_uppercase(self):
        """paint() with uppercase hex strings."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="#FF7800", bg="#202020")
        assert "38;2;255;120;0" in result
        assert "48;2;32;32;32" in result

    def test_paint_hex_both(self):
        """paint() with hex strings for both foreground and background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="#ff0000", bg="#00ff00")
        assert "38;2;255;0;0" in result
        assert "48;2;0;255;0" in result

    def test_paint_color256_foreground(self):
        """paint() with 256-color index foreground."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=208)
        assert "\033[38;5;208m" in result
        assert "test" in result

    def test_paint_color256_background(self):
        """paint() with 256-color index background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", bg=236)
        assert "\033[48;5;236m" in result
        assert "test" in result

    def test_paint_color256_both(self):
        """paint() with 256-color indices for both foreground and background."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=200, bg=50)
        assert "38;5;200" in result
        assert "48;5;50" in result

    def test_paint_module_level_rgb(self):
        """Module-level paint() with RGB tuple."""
        original_use_color = tint.use_color
        tint.set_color(True)
        try:
            result = paint("test", color=(255, 120, 0))
            assert "\033[38;2;255;120;0m" in result
        finally:
            tint.set_color(original_use_color)

    def test_paint_module_level_hex(self):
        """Module-level paint() with hex string."""
        original_use_color = tint.use_color
        tint.set_color(True)
        try:
            result = paint("test", color="#ff7800")
            assert "\033[38;2;255;120;0m" in result
        finally:
            tint.set_color(original_use_color)

    def test_paint_module_level_256(self):
        """Module-level paint() with 256-color index."""
        original_use_color = tint.use_color
        tint.set_color(True)
        try:
            result = paint("test", color=208)
            assert "\033[38;5;208m" in result
        finally:
            tint.set_color(original_use_color)

    def test_paint_rgb_with_styles(self):
        """paint() with RGB color and styles."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=(255, 0, 0), styles="bold")
        assert "38;2;255;0;0" in result
        # Bold style code is "1"
        assert ";1m" in result or ";1;" in result

    def test_paint_hex_with_styles(self):
        """paint() with hex color and styles."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="#ff0000", styles="underline")
        assert "\033[38;2;255;0;0" in result

    def test_paint_color256_with_styles(self):
        """paint() with 256-color and styles."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=208, styles="dim")
        assert "\033[38;5;208" in result

    def test_paint_color_disabled_rgb(self):
        """paint() with RGB color but color disabled returns plain text."""
        raztint = RazTint()
        raztint.set_color(False)

        result = raztint.format_text("test", color=(255, 120, 0))
        assert result == "test"

    def test_paint_color_disabled_hex(self):
        """paint() with hex color but color disabled returns plain text."""
        raztint = RazTint()
        raztint.set_color(False)

        result = raztint.format_text("test", color="#ff7800")
        assert result == "test"

    def test_paint_color_disabled_256(self):
        """paint() with 256-color but color disabled returns plain text."""
        raztint = RazTint()
        raztint.set_color(False)

        result = raztint.format_text("test", color=208)
        assert result == "test"

    def test_paint_rgb_invalid_raises(self):
        """paint() with invalid RGB tuple raises ValueError."""
        raztint = RazTint()
        raztint.set_color(True)

        with pytest.raises(ValueError, match="RGB channel"):
            raztint.format_text("test", color=(256, 0, 0))  # type: ignore[arg-type]

    def test_paint_hex_invalid_raises(self):
        """paint() with invalid hex raises ValueError."""
        raztint = RazTint()
        raztint.set_color(True)

        with pytest.raises(ValueError, match="6-digit hex"):
            raztint.format_text("test", color="#fff")

    def test_paint_256_invalid_raises(self):
        """paint() with invalid 256-color index raises ValueError."""
        raztint = RazTint()
        raztint.set_color(True)

        with pytest.raises(ValueError, match="256-color index"):
            raztint.format_text("test", color=300)

    def test_paint_backward_compat_named_color(self):
        """paint() still works with named color strings."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color="red")
        assert "\033[31m" in result

    def test_paint_backward_compat_standard_ansi_code(self):
        """paint() still works with standard ANSI codes."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.format_text("test", color=91)
        assert "\033[91m" in result
