import os
from unittest import mock

from raztint.detect.env import enable_windows_vt_mode, get_icon_mode, supports_color


class TestSupportsColor:
    def test_no_color_env_disables_color_even_if_tty(self) -> None:
        with mock.patch.dict(os.environ, {"NO_COLOR": "1"}, clear=True):
            fake_stdout = mock.Mock()
            fake_stdout.isatty.return_value = True
            with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
                assert supports_color() is False

    def test_force_color_overrides_non_tty(self) -> None:
        with mock.patch.dict(os.environ, {"RAZTINT_FORCE_COLOR": "1"}, clear=True):
            fake_stdout = mock.Mock()
            fake_stdout.isatty.return_value = False
            with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
                assert supports_color() is True

    def test_non_tty_disables_color(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            fake_stdout = mock.Mock()
            fake_stdout.isatty.return_value = False
            with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
                assert supports_color() is False

    def test_term_dumb_disables_color(self) -> None:
        with mock.patch.dict(os.environ, {"TERM": "dumb"}, clear=True):
            fake_stdout = mock.Mock()
            fake_stdout.isatty.return_value = True
            with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
                assert supports_color() is False

    @mock.patch("raztint.detect.env.os.name", "nt")
    def test_windows_path_uses_vt_mode(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            fake_stdout = mock.Mock()
            fake_stdout.isatty.return_value = True
            with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
                with mock.patch(
                    "raztint.detect.env.enable_windows_vt_mode", return_value=True
                ) as mocked_vt:
                    assert supports_color() is True
                    mocked_vt.assert_called_once()


class TestGetIconMode:
    def test_ascii_fallback_when_encoding_cannot_handle_nerd(self) -> None:
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "ascii"
        with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
            with mock.patch.dict(os.environ, {}, clear=True):
                assert get_icon_mode() == "ascii"

    def test_force_nerd_icons_env(self) -> None:
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "utf-8"
        with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
            with mock.patch.dict(
                os.environ, {"RAZTINT_USE_NERD_ICONS": "1"}, clear=True
            ):
                assert get_icon_mode() == "nerd"

    def test_force_std_icons_env(self) -> None:
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "utf-8"
        with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
            with mock.patch.dict(
                os.environ, {"RAZTINT_NO_NERD_ICONS": "1"}, clear=True
            ):
                with mock.patch(
                    "raztint.detect.env.has_nerd_fonts",
                    side_effect=AssertionError("should not be called"),
                ):
                    assert get_icon_mode() == "std"

    def test_nerd_mode_when_fonts_detected(self) -> None:
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "utf-8"
        with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
            with mock.patch.dict(os.environ, {}, clear=True):
                with mock.patch("raztint.detect.env.has_nerd_fonts", return_value=True):
                    assert get_icon_mode() == "nerd"

    def test_std_mode_when_no_fonts_detected(self) -> None:
        fake_stdout = mock.Mock()
        fake_stdout.encoding = "utf-8"
        with mock.patch("raztint.detect.env.sys.stdout", fake_stdout):
            with mock.patch.dict(os.environ, {}, clear=True):
                with mock.patch(
                    "raztint.detect.env.has_nerd_fonts", return_value=False
                ):
                    assert get_icon_mode() == "std"


def test_enable_windows_vt_mode_handles_missing_windll() -> None:
    fake_ctypes = mock.Mock()
    fake_ctypes.windll = None
    with mock.patch.dict("sys.modules", {"ctypes": fake_ctypes}):
        assert enable_windows_vt_mode() is False


def test_enable_windows_vt_mode_handles_invalid_stdout_handle() -> None:
    fake_ctypes = mock.Mock()
    fake_ctypes.windll.kernel32.GetStdHandle.return_value = -1
    with mock.patch.dict("sys.modules", {"ctypes": fake_ctypes}):
        assert enable_windows_vt_mode() is False


def test_enable_windows_vt_mode_handles_get_console_mode_failure() -> None:
    fake_ctypes = mock.Mock()
    fake_ctypes.c_uint32.return_value = mock.Mock(value=0)
    fake_ctypes.byref.side_effect = lambda value: value
    fake_ctypes.windll.kernel32.GetStdHandle.return_value = 42
    fake_ctypes.windll.kernel32.GetConsoleMode.return_value = 0
    with mock.patch.dict("sys.modules", {"ctypes": fake_ctypes}):
        assert enable_windows_vt_mode() is False


def test_enable_windows_vt_mode_returns_false_when_set_console_mode_fails() -> None:
    fake_ctypes = mock.Mock()
    mode = mock.Mock(value=7)
    fake_ctypes.c_uint32.return_value = mode
    fake_ctypes.byref.side_effect = lambda value: value
    fake_ctypes.windll.kernel32.GetStdHandle.return_value = 42
    fake_ctypes.windll.kernel32.GetConsoleMode.return_value = 1
    fake_ctypes.windll.kernel32.SetConsoleMode.return_value = 0
    with mock.patch.dict("sys.modules", {"ctypes": fake_ctypes}):
        assert enable_windows_vt_mode() is False
