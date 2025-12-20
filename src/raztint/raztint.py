import os
import sys
from collections.abc import Callable
from functools import lru_cache

from raztint.colors import COLORS
from raztint.icons import ICONS


class RazTint:
    """A zero-dependency Python library for ANSI coloring and smart CLI icons.

    RazTint provides automatic environment detection for colors and icons,
    with support for Nerd Fonts, Unicode, and ASCII fallbacks.
    """

    COLORS = COLORS
    ICONS = ICONS

    def __init__(self) -> None:
        self.use_color: bool = self._supports_color()
        self.icon_mode: str = self._get_icon_mode()

        for name, code in self.COLORS.items():
            setattr(self, name.lower(), self._make_color_func(code))

        for name, data in self.ICONS.items():
            color_key = data.get("color", "WHITE")
            color_code = self.COLORS.get(color_key, "37")
            setattr(
                self,
                name,
                self._make_icon_func(data, color_code),
            )

    def _make_color_func(self, code: str) -> Callable[[str], str]:
        return lambda text: self.color(text, code)

    def _make_icon_func(self, data: dict[str, str], code: str) -> Callable[[], str]:
        def fn() -> str:
            if self.icon_mode == "nerd":
                symbol = data["nerd"]
            elif self.icon_mode == "std":
                symbol = data["std"]
            else:
                symbol = data["ascii"]

            return self.color(symbol, code)

        return fn

    def color(self, text: str, fg_code: str) -> str:
        """Apply ANSI color code to text.

        Args:
            text: The text to colorize
            fg_code: ANSI foreground color code (e.g., "31" for red)

        Returns:
            Colored text with ANSI escape sequences if color is enabled,
            otherwise returns plain text.
        """
        if not self.use_color:
            return text
        return f"\033[{fg_code}m{text}\033[0m"

    def set_color(self, enabled: bool) -> None:
        """Enable or disable color output programmatically.

        Args:
            enabled: True to enable colors, False to disable
        """
        self.use_color = enabled

    def _supports_color(self) -> bool:
        if os.getenv("NO_COLOR") or os.getenv("RAZTINT_NO_COLOR"):
            return False

        force = os.getenv("RAZTINT_FORCE_COLOR", "").lower()
        if force in ("1", "true", "yes", "on"):
            return True

        stream = sys.stdout
        if not hasattr(stream, "isatty") or not stream.isatty():
            return False
        if os.name == "nt":
            return self._enable_windows_vt_mode()
        term = os.getenv("TERM", "")
        return bool(term and term.lower() != "dumb")

    @classmethod
    def _get_icon_mode(cls) -> str:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        try:
            "[󰄬]".encode(encoding)
        except Exception:
            return "ascii"

        # Check for explicit nerd fonts preference
        force_nerd = os.getenv("RAZTINT_USE_NERD_ICONS", "").lower()
        if force_nerd in ("1", "true", "yes", "on"):
            return "nerd"

        # Check for explicit disable
        force_no_nerd = os.getenv("RAZTINT_NO_NERD_ICONS", "").lower()
        if force_no_nerd in ("1", "true", "yes", "on"):
            return "std"

        # Auto-detect nerd fonts
        if cls._has_nerd_fonts():
            return "nerd"

        # Default to standard icons
        return "std"

    @classmethod
    @lru_cache(maxsize=1)
    def _has_nerd_fonts(cls) -> bool:
        """Detect if nerd fonts are available in the terminal."""
        # Check environment variables that indicate nerd fonts
        nerd_env = os.getenv("NERDFONTS") or os.getenv("NERD_FONTS")
        if nerd_env and nerd_env.lower() in ("1", "true", "yes", "on"):
            return True

        # Check font name from environment
        font_name = os.getenv("FONT_NAME", "").lower()
        if font_name and any(
            name in font_name
            for name in [
                "nerd",
                "nf-",
                "hack nerd",
                "fira code nerd",
                "jetbrains mono nerd",
                "meslo nerd",
                "cascadia code nerd",
            ]
        ):
            return True

        # Check terminal font setting
        term_font = os.getenv("TERM_FONT", "").lower()
        if term_font and any(
            name in term_font
            for name in [
                "nerd",
                "nf-",
                "hack nerd",
                "fira code nerd",
                "jetbrains mono nerd",
                "meslo nerd",
                "cascadia code nerd",
            ]
        ):
            return True

        return bool(cls._check_installed_nerd_fonts())

    @staticmethod
    @lru_cache(maxsize=1)
    def _check_installed_nerd_fonts() -> bool:
        """Check if nerd fonts are installed on the system."""
        import subprocess

        if os.name == "nt":
            # Windows: Check registry or font directory

            try:
                powershell_path = "powershell"
                result = subprocess.run(
                    [
                        powershell_path,
                        "-Command",
                        "Get-ChildItem 'C:\\Windows\\Fonts'"
                        " | Where-Object {$_.Name -like '*Nerd*'} "
                        " | Select-Object -First 1",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return True
            except FileNotFoundError:
                return False
            except Exception:
                return False

        elif sys.platform == "darwin":
            # macOS: Check via system_profiler or font directory
            try:
                result = subprocess.run(
                    ["system_profiler", "SPFontsDataType"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0:
                    output = result.stdout.lower()
                    if any(name.lower() in output for name in ["nerd", "nf-"]):
                        return True
            except Exception:
                pass

            # Also check common font directories
            font_dirs = [
                os.path.expanduser("~/Library/Fonts"),
                "/Library/Fonts",
                "/System/Library/Fonts",
            ]
            for font_dir in font_dirs:
                if os.path.isdir(font_dir):
                    try:
                        for item in os.listdir(font_dir):
                            if "nerd" in item.lower() or "nf-" in item.lower():
                                return True
                    except Exception:
                        continue

        else:
            # Linux: Use fc-list (fontconfig)
            try:
                result = subprocess.run(
                    ["fc-list", ":", "family"],
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0:
                    output = result.stdout.lower()
                    nerd_indicators = ["nerd", "nf-", "hack nerd", "fira code nerd"]
                    if any(indicator in output for indicator in nerd_indicators):
                        return True
            except Exception:
                pass

        return False

    def _enable_windows_vt_mode(self) -> bool:
        import ctypes

        windll = getattr(ctypes, "windll", None)
        if windll is None:
            return False

        kernel32 = getattr(windll, "kernel32", None)
        if kernel32 is None:
            return False

        handle = kernel32.GetStdHandle(-11)
        if handle in (0, -1):
            return False

        mode = ctypes.c_uint32()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False

        enable_virtual_terminal_processing = 0x0004
        success = kernel32.SetConsoleMode(
            handle, mode.value | enable_virtual_terminal_processing
        )
        return bool(success)
