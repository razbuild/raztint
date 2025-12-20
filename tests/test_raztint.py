import os
from unittest import mock

from raztint.raztint import RazTint


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
