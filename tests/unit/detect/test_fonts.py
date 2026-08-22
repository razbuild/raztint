import os
from unittest import mock

from raztint.detect.fonts import (
    _check_mac_font_dirs,
    check_installed_nerd_fonts,
    has_nerd_fonts,
)


class TestHasNerdFonts:
    def setup_method(self) -> None:
        has_nerd_fonts.cache_clear()
        check_installed_nerd_fonts.cache_clear()

    def teardown_method(self) -> None:
        has_nerd_fonts.cache_clear()
        check_installed_nerd_fonts.cache_clear()

    def test_env_variable_enables_nerd_fonts(self) -> None:
        with mock.patch.dict(os.environ, {"NERDFONTS": "1"}, clear=True):
            assert has_nerd_fonts() is True

    def test_font_name_indicator(self) -> None:
        with mock.patch.dict(os.environ, {"FONT_NAME": "Hack Nerd Font"}, clear=True):
            assert has_nerd_fonts() is True

    def test_term_font_indicator(self) -> None:
        with mock.patch.dict(
            os.environ, {"TERM_FONT": "JetBrains Mono Nerd"}, clear=True
        ):
            assert has_nerd_fonts() is True

    def test_skip_system_font_scan_env(self) -> None:
        with mock.patch.dict(
            os.environ, {"RAZTINT_SKIP_SYSTEM_FONT_SCAN": "1"}, clear=True
        ):
            with mock.patch(
                "raztint.detect.fonts.check_installed_nerd_fonts",
                side_effect=AssertionError("should not be called"),
            ):
                assert has_nerd_fonts() is False


class TestCheckInstalledNerdFonts:
    def setup_method(self) -> None:
        check_installed_nerd_fonts.cache_clear()

    def teardown_method(self) -> None:
        check_installed_nerd_fonts.cache_clear()

    @mock.patch("raztint.detect.fonts.os.name", "nt")
    def test_windows_detection_uses_powershell(self) -> None:
        with mock.patch("raztint.detect.fonts.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "Some Nerd Font"
            assert check_installed_nerd_fonts() is True
            assert run.call_args is not None

    @mock.patch("raztint.detect.fonts.os.name", "nt")
    def test_windows_detection_handles_powershell_errors(self) -> None:
        with mock.patch(
            "raztint.detect.fonts.subprocess.run",
            side_effect=OSError("powershell not found"),
        ):
            assert check_installed_nerd_fonts() is False

    @mock.patch("raztint.detect.fonts.sys.platform", "linux")
    def test_posix_detection_handles_fc_list_errors(self) -> None:
        with mock.patch(
            "raztint.detect.fonts.subprocess.run",
            side_effect=OSError("fc-list not found"),
        ):
            assert check_installed_nerd_fonts() is False

    @mock.patch("raztint.detect.fonts.sys.platform", "darwin")
    def test_macos_detection_uses_system_profiler(self) -> None:
        # Explicitly clear CI so we exercise the non-CI (real scan) path.
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch(
                "raztint.detect.fonts._check_mac_font_dirs", return_value=False
            ):
                with mock.patch("raztint.detect.fonts.subprocess.run") as run:
                    run.return_value.returncode = 0
                    run.return_value.stdout = "Some nerd Font"
                    assert check_installed_nerd_fonts() is True
                    assert run.call_args is not None

    @mock.patch("raztint.detect.fonts.sys.platform", "darwin")
    def test_macos_skips_system_profiler_in_ci(self) -> None:
        # In CI, system_profiler is slow and pointless, so it should never
        # be invoked once the fast directory scan comes back empty.
        with mock.patch.dict(os.environ, {"CI": "true"}, clear=True):
            with mock.patch(
                "raztint.detect.fonts._check_mac_font_dirs", return_value=False
            ):
                with mock.patch("raztint.detect.fonts.subprocess.run") as run:
                    assert check_installed_nerd_fonts() is False
                    run.assert_not_called()

    @mock.patch("raztint.detect.fonts.sys.platform", "linux")
    def test_posix_detection_uses_fc_list(self) -> None:
        with mock.patch("raztint.detect.fonts.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "Hack Nerd Font"
            assert check_installed_nerd_fonts() is True
            assert run.call_args is not None


class TestCheckMacFontDirs:
    @mock.patch("raztint.detect.fonts._MAC_FONT_DIRS", ("/mock/fonts",))
    def test_skips_missing_dirs(self) -> None:
        with mock.patch("raztint.detect.fonts.os.path.isdir", return_value=False):
            assert _check_mac_font_dirs() is False

    @mock.patch("raztint.detect.fonts._MAC_FONT_DIRS", ("/mock/fonts",))
    def test_finds_nerd_font_in_font_dir(self) -> None:
        with mock.patch("raztint.detect.fonts.os.path.isdir", return_value=True):
            with mock.patch(
                "raztint.detect.fonts.os.listdir",
                return_value=["Hack Nerd Font.ttf"],
            ):
                assert _check_mac_font_dirs() is True

    @mock.patch("raztint.detect.fonts._MAC_FONT_DIRS", ("/mock/fonts",))
    def test_handles_listing_errors(self) -> None:
        with mock.patch("raztint.detect.fonts.os.path.isdir", return_value=True):
            with mock.patch(
                "raztint.detect.fonts.os.listdir",
                side_effect=PermissionError("denied"),
            ):
                assert _check_mac_font_dirs() is False
