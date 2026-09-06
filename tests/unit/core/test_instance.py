import os
from unittest import mock

import pytest

from raztint import err, info, ok, tint, warn
from raztint.core import RazTint
from raztint.core.transient import TransientLine
from raztint.data import BACKGROUND_COLORS, STYLES


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
        """Background color methods exist on the module-level singleton instance."""
        original_use_color = tint.use_color
        tint.set_color(True)

        try:
            assert tint.bg_red("test") == "\033[41mtest\033[49m"
            assert tint.bg_blue("test") == "\033[44mtest\033[49m"
        finally:
            tint.set_color(original_use_color)

    def test_module_level_icon_helpers_are_distinct(self):
        """Module-level ok/err/warn/info must not all alias tint.ok."""
        original_icon_mode = tint.icon_mode
        original_use_color = tint.use_color
        raztint = RazTint()
        raztint.icon_mode = "std"
        raztint.set_color(False)
        tint.icon_mode = "std"
        tint.set_color(False)

        try:
            assert ok() == raztint.ok()
            assert err() == raztint.err()
            assert warn() == raztint.warn()
            assert info() == raztint.info()
            assert ok() != err()
        finally:
            tint.icon_mode = original_icon_mode
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
                assert raztint.debug() == "[DEBUG]"
                assert raztint.pending() == "[PENDING]"

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
            assert hasattr(raztint, style_name.lower()), (
                f"Missing style method: {style_name}"
            )

    def test_style_disabled_returns_plain_text(self):
        """When color is disabled, style methods should return plain text."""
        raztint = RazTint()
        raztint.set_color(False)
        for style_name in STYLES:
            method = getattr(raztint, style_name.lower())
            assert method("test") == "test", (
                f"Style {style_name} should return plain text"
            )

    def test_style_enabled_uses_correct_ansi_codes(self):
        """Each style should wrap text with its specific on/off ANSI codes."""
        raztint = RazTint()
        raztint.set_color(True)

        for style_name, (on_code, off_code) in STYLES.items():
            method = getattr(raztint, style_name.lower())
            result = method("test")
            assert f"\033[{on_code}m" in result
            assert f"\033[{off_code}m" in result
            assert "\033[0m" not in result, (
                f"{style_name} should use targeted reset, not \\033[0m"
            )

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


def test_private_resolve_icon():
    raztint = RazTint()

    with mock.patch(
        "raztint.core.instance.resolve_icon",
        return_value="[✓]",
    ) as mocked:
        assert raztint._resolve_icon("ok") == "[✓]"

    mocked.assert_called_once()


class TestTransient:
    """Test cases for RazTint.transient()."""

    def test_transient_delegates_to_transient_line(self):
        raztint = RazTint()

        with mock.patch("raztint.core.instance.TransientLine") as mocked_cls:
            sentinel = mock.Mock()
            mocked_cls.return_value = sentinel

            result = raztint.transient("loading...")

        mocked_cls.assert_called_once_with("loading...")
        assert result is sentinel

    def test_transient_returns_transient_line_instance(self):
        """Without mocking, transient() should return a real TransientLine."""
        raztint = RazTint()
        result = raztint.transient("loading...")
        assert isinstance(result, TransientLine)


class TestIntents:
    """Test cases for RazTint.intents()."""

    def test_intents_with_no_name_returns_all(self):
        """Calling with no name should delegate to _get_intents(None)."""
        raztint = RazTint()

        with mock.patch("raztint.core.instance._get_intents") as mocked:
            mocked.return_value = {"ok": {"color": "GREEN"}}
            result = raztint.intents()

        mocked.assert_called_once_with(None)
        assert result == {"ok": {"color": "GREEN"}}

    def test_intents_with_name_forwards_it(self):
        """Calling with a name should delegate to _get_intents(name)."""
        raztint = RazTint()

        with mock.patch("raztint.core.instance._get_intents") as mocked:
            mocked.return_value = {"color": "RED"}
            result = raztint.intents("err")

        mocked.assert_called_once_with("err")
        assert result == {"color": "RED"}

    def test_intents_unmocked_returns_known_intent(self):
        """Sanity check against the real intents data, without mocking."""
        raztint = RazTint()
        assert raztint.intents("success") == raztint.intents()["success"]


class TestCase:
    """Test cases for RazTint.case()."""

    def test_case_formats_matching_value(self):
        """A matching key should format its (text, intent) pair via format_text."""
        raztint = RazTint()
        cases = {"success": ("Done!", "success"), "failure": ("Failed!", "error")}

        with mock.patch.object(raztint, "format_text") as mocked_format:
            mocked_format.return_value = "formatted"
            result = raztint.case("success", cases)

        mocked_format.assert_called_once_with("Done!", intent="success")
        assert result == "formatted"

    def test_case_selects_correct_pair_among_several(self):
        """Each key should route to its own (text, intent) pair."""
        raztint = RazTint()
        cases = {"success": ("Done!", "success"), "failure": ("Failed!", "error")}

        with mock.patch.object(raztint, "format_text") as mocked_format:
            mocked_format.return_value = "formatted"
            raztint.case("failure", cases)

        mocked_format.assert_called_once_with("Failed!", intent="error")

    def test_case_raises_value_error_for_unknown_key(self):
        """A value with no entry in cases should raise a clear ValueError."""
        raztint = RazTint()
        cases = {"success": ("Done!", "success")}

        with pytest.raises(ValueError, match=r"No case defined for 'missing'"):
            raztint.case("missing", cases)

    def test_case_error_message_includes_repr_of_value(self):
        """The ValueError message should use repr() of the offending value."""
        raztint = RazTint()
        cases = {1: ("one", "success")}

        with pytest.raises(ValueError, match=r"No case defined for 2"):
            raztint.case(2, cases)

    def test_case_does_not_swallow_unrelated_keyerror(self):
        """A missing key should surface as ValueError, not a bare KeyError."""
        raztint = RazTint()

        with pytest.raises(ValueError):
            raztint.case("anything", {})

    def test_case_unmocked_returns_formatted_text(self):
        """End-to-end: case() should return whatever format_text produces."""
        raztint = RazTint()
        cases = {"success": ("Done!", "success")}

        assert raztint.case("success", cases) == raztint.format_text(
            "Done!", intent="success"
        )


class TestPreview:
    """Test cases for RazTint.preview()."""

    def test_preview_includes_header_and_platform(self):
        import sys

        raztint = RazTint()
        output = raztint.preview()

        assert "RazTint" in output
        assert "Platform" in output
        assert sys.platform in output

    def test_preview_reflects_color_enabled(self):
        raztint = RazTint()
        raztint.set_color(True)

        assert "Color       enabled" in raztint.preview()

    def test_preview_reflects_color_disabled(self):
        raztint = RazTint()
        raztint.set_color(False)

        assert "Color       disabled" in raztint.preview()

    def test_preview_reflects_icon_mode(self):
        raztint = RazTint()
        raztint.icon_mode = "nerd"

        assert "Icon mode   nerd" in raztint.preview()

    def test_preview_uses_term_env_var_when_set(self):
        raztint = RazTint()

        with mock.patch.dict(os.environ, {"TERM": "xterm-256color"}, clear=False):
            assert "Terminal    xterm-256color" in raztint.preview()

    def test_preview_falls_back_to_unknown_terminal_when_term_unset(self):
        raztint = RazTint()

        env = dict(os.environ)
        env.pop("TERM", None)
        with mock.patch.dict(os.environ, env, clear=True):
            assert "Terminal    unknown" in raztint.preview()

    def test_preview_uses_stdout_encoding_when_available(self):
        raztint = RazTint()
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "utf-8"

        with mock.patch("sys.stdout", fake_stdout):
            assert "Encoding    utf-8" in raztint.preview()

    def test_preview_falls_back_to_unknown_encoding_when_missing(self):
        raztint = RazTint()

        class StreamWithoutEncoding:
            pass

        with mock.patch("sys.stdout", StreamWithoutEncoding()):
            assert "Encoding    unknown" in raztint.preview()

    def test_preview_falls_back_to_unknown_encoding_when_empty(self):
        """An empty-string encoding is falsy and should also fall back."""
        raztint = RazTint()
        fake_stdout = mock.Mock()
        fake_stdout.encoding = ""

        with mock.patch("sys.stdout", fake_stdout):
            assert "Encoding    unknown" in raztint.preview()
