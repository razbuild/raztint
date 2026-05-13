import os
from unittest import mock

from raztint import bg_blue, bg_red, tint
from raztint.colors import BACKGROUND_COLORS
from raztint.core import RazTint
from raztint.styles import STYLES


class TestColorizer:
    """Test cases for RazTint."""

    def test_colorizer_initialization(self):
        """Test RazTint initialization and attribute existence."""
        raztint = RazTint()
        assert hasattr(raztint, "use_color")
        assert hasattr(raztint, "icon_mode")
        assert raztint.icon_mode in ["nerd", "std", "ascii"]

    def test_methods_existence(self):
        """Test that dynamic methods are created."""
        raztint = RazTint()

        # Colors
        assert hasattr(raztint, "black")
        assert hasattr(raztint, "red")
        assert hasattr(raztint, "green")
        assert hasattr(raztint, "yellow")
        assert hasattr(raztint, "blue")
        assert hasattr(raztint, "magenta")
        assert hasattr(raztint, "cyan")
        assert hasattr(raztint, "white")
        assert hasattr(raztint, "gray")

        # Background colors
        assert hasattr(raztint, "bg_red")
        assert hasattr(raztint, "bg_blue")
        assert hasattr(raztint, "bg_bright_white")

        # Icons
        assert hasattr(raztint, "ok")
        assert hasattr(raztint, "err")
        assert hasattr(raztint, "warn")
        assert hasattr(raztint, "info")

    def test_color_method_disabled(self):
        """Test color method returns plain text when disabled."""
        raztint = RazTint()
        raztint.set_color(False)

        assert raztint.color("test", "31") == "test"
        assert raztint.red("test") == "test"

    def test_color_method_enabled(self):
        """Test color method returns ANSI codes when enabled."""
        raztint = RazTint()
        raztint.set_color(True)

        result = raztint.red("test")
        assert "\033[31m" in result
        assert "test" in result
        assert "\033[0m" in result

    def test_background_methods_exist(self):
        """Test that dynamic background color methods are created."""
        raztint = RazTint()
        for background_name in BACKGROUND_COLORS:
            assert hasattr(raztint, background_name.lower())

    def test_background_method_disabled(self):
        """Test background method returns plain text when disabled."""
        raztint = RazTint()
        raztint.set_color(False)

        assert raztint.background("test", "41") == "test"
        assert raztint.bg_red("test") == "test"

    def test_background_method_enabled_uses_background_reset(self):
        """Test background colors use ANSI background codes and reset 49."""
        raztint = RazTint()
        raztint.set_color(True)

        assert raztint.bg_red("test") == "\033[41mtest\033[49m"
        assert raztint.bg_gray("test") == "\033[100mtest\033[49m"

    def test_background_preserves_outer_foreground_color(self):
        """Background reset should not clear an outer foreground color."""
        raztint = RazTint()
        raztint.set_color(True)

        assert (
            raztint.red(raztint.bg_blue("test"))
            == "\033[31m\033[44mtest\033[49m\033[0m"
        )

    def test_module_level_background_helpers(self):
        """Module-level singleton exposes background helpers."""
        original_use_color = tint.use_color
        tint.set_color(True)

        try:
            assert bg_red("test") == "\033[41mtest\033[49m"
            assert bg_blue("test") == "\033[44mtest\033[49m"
        finally:
            tint.set_color(original_use_color)

    def test_env_no_color(self):
        """Test NO_COLOR environment variable."""
        with mock.patch.dict(os.environ, {"NO_COLOR": "1"}):
            raztint = RazTint()
            assert raztint.use_color is False

    def test_env_force_color_valid(self):
        for val in ["1", "true", "True", "yes", "on"]:
            with mock.patch.dict(os.environ, {"RAZTINT_FORCE_COLOR": val}, clear=True):
                raztint = RazTint()
                assert raztint.use_color is True

    def test_env_force_color_invalid(self):
        """Test RAZTINT_FORCE_COLOR with falsy values (Bug fix test)."""
        with mock.patch("sys.stdout.isatty", return_value=False) as mock_stdout:
            mock_stdout.isatty.return_value = False

            for val in ["0", "false", "off"]:
                with mock.patch.dict(
                    os.environ, {"RAZTINT_FORCE_COLOR": val}, clear=True
                ):
                    raztint = RazTint()
                    assert raztint.use_color is False, f"Failed for value: {val}"

    @mock.patch("sys.platform", "linux")
    def test_icon_mode_linux_default(self):
        """Test default icon mode on Linux (should be 'std')."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(RazTint, "_has_nerd_fonts", return_value=False):
                raztint = RazTint()
                assert raztint.icon_mode == "std"
                assert "[✓]" in raztint.ok()

    @mock.patch("os.name", "nt")
    @mock.patch("sys.platform", "win32")
    def test_icon_mode_windows_default(self):
        """Test default icon mode on Windows (should be 'std')."""
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch.object(RazTint, "_has_nerd_fonts", return_value=False):
                raztint = RazTint()
                assert raztint.icon_mode == "std"
                assert "[✓]" in raztint.ok()

    def test_icon_mode_force_nerd(self):
        """Test forcing nerd fonts via environment variable."""
        with mock.patch.dict(os.environ, {"RAZTINT_USE_NERD_ICONS": "1"}):
            raztint = RazTint()
            assert raztint.icon_mode == "nerd"
            assert "[󰄬]" in raztint.ok()

    def test_icon_render_std(self):
        """Test specific output for Standard mode."""
        raztint = RazTint()
        raztint.icon_mode = "std"
        raztint.set_color(False)

        assert raztint.ok() == "[✓]"
        assert raztint.err() == "[✗]"
        assert raztint.warn() == "[!]"
        assert raztint.info() == "[i]"

    def test_icon_mode_ascii_fallback(self):
        """Test fallback to ASCII if encoding fails."""

        fake_stdout = mock.Mock()
        fake_stdout.encoding = "ascii"
        fake_stdout.isatty.return_value = True

        with mock.patch("sys.stdout", fake_stdout):
            with mock.patch.dict(os.environ, {"RAZTINT_USE_NERD_ICONS": "1"}):
                raztint = RazTint()
                raztint.set_color(False)

                assert raztint.icon_mode == "ascii"
                assert raztint.ok() == "[OK]"
                assert raztint.err() == "[ERR]"
                assert raztint.warn() == "[WARN]"
                assert raztint.info() == "[INFO]"

    def test_set_color_method(self):
        """Test toggling color via set_color."""
        raztint = RazTint()
        raztint.set_color(True)
        assert raztint.use_color is True

        raztint.set_color(False)
        assert raztint.use_color is False

    def test_style_methods_exist(self):
        """Check that dynamic style methods are created from STYLES."""
        raztint = RazTint()
        for style_name in STYLES:
            assert hasattr(
                raztint, style_name.lower()
            ), f"Missing style method: {style_name}"

    def test_style_disabled_returns_plain_text(self):
        """When color is disabled, style methods should return plain text."""
        raztint = RazTint()
        raztint.set_color(False)
        for style_name in STYLES:
            method = getattr(raztint, style_name.lower())
            assert (
                method("test") == "test"
            ), f"Style {style_name} should return plain text"

    def test_style_enabled_uses_correct_ansi_codes(self):
        """Each style should wrap text with its specific on/off ANSI codes."""
        raztint = RazTint()
        raztint.set_color(True)

        for style_name, (on_code, off_code) in STYLES.items():
            method = getattr(raztint, style_name.lower())
            result = method("test")
            assert f"\033[{on_code}m" in result
            assert f"\033[{off_code}m" in result
            assert (
                "\033[0m" not in result
            ), f"{style_name} should use targeted reset, not \\033[0m"

    def test_style_method_direct(self):
        """Direct call to style() method should behave consistently."""
        raztint = RazTint()
        raztint.set_color(False)
        assert raztint.style("test", "1", "22") == "test"

        raztint.set_color(True)
        result = raztint.style("test", "1", "22")
        assert result.startswith("\033[1m")
        assert "test" in result
        assert result.endswith("\033[22m")

    def test_style_does_not_reset_color(self):
        """Verify that applying a style after a color preserves the color."""
        raztint = RazTint()
        raztint.set_color(True)

        combined = raztint.red(raztint.bold("test"))
        assert "\033[31m" in combined
        assert "\033[1m" in combined
        assert "\033[22m" in combined
        assert combined.endswith("\033[0m")
        style_part = combined[
            combined.index("\033[1m") : combined.index("\033[22m") + len("\033[22m")
        ]
        assert "\033[0m" not in style_part


class TestFormatText:
    """Test cases for the format_text method."""

    def test_format_text_exists(self):
        """Test that format_text method exists on RazTint."""
        raztint = RazTint()
        assert hasattr(raztint, "format_text")
        assert callable(raztint.format_text)

    def test_format_text_module_level_export(self):
        """Test that format_text is exported at module level."""
        from raztint import format_text

        assert callable(format_text)

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

        result = raztint.format_text("test", color="RED")
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
                raztint.format_text("test", color=50)
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "invalid" in str(e).lower()

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
                raztint.format_text("test", bg=50)
                assert False, "Should have raised ValueError"
            except ValueError as e:
                assert "invalid" in str(e).lower()

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
