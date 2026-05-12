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
