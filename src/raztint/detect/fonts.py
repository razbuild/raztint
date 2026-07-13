import os
import re
import subprocess
import sys
from functools import lru_cache

from .debug import debug

_NERD_INDICATORS = (
    "nerd",
    "nf-",
    "hack nerd",
    "fira code nerd",
    "jetbrains mono nerd",
    "meslo nerd",
    "cascadia code nerd",
)


_NERD_SUFFIX_RE = re.compile(r"\bnf\b")

_MAC_FONT_DIRS = (
    os.path.expanduser("~/Library/Fonts"),
    "/Library/Fonts",
    "/System/Library/Fonts",
)


def _has_indicator(text: str) -> bool:
    if any(indicator in text for indicator in _NERD_INDICATORS):
        return True
    return bool(_NERD_SUFFIX_RE.search(text))


def _check_mac_font_dirs() -> bool:
    """Fast path: scan known font directories before falling back to system_profiler."""
    for font_dir in _MAC_FONT_DIRS:
        if not os.path.isdir(font_dir):
            continue
        try:
            if any(_has_indicator(f.lower()) for f in os.listdir(font_dir)):
                debug(f"Font detection (macOS): nerd font found in {font_dir}")
                return True
        except Exception as exc:
            debug(f"Font detection (macOS) failed for {font_dir}: {exc!r}")
    return False


def _check_mac_system_profiler() -> bool:
    """Slow path (~1-2s): only used if the fast directory scan finds nothing."""
    try:
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0 and _has_indicator(result.stdout.lower()):
            debug("Font detection (macOS): nerd font found via system_profiler")
            return True
    except Exception as exc:
        debug(f"Font detection (macOS system_profiler) failed: {exc!r}")
    return False


def _check_windows_fonts() -> bool:
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                (
                    "Get-ChildItem 'C:\\Windows\\Fonts' | "
                    "Where-Object {$_.Name -like '*[Nn]erd*' -or "
                    "$_.Name -like '* NF*'} | "
                    "Select-Object -First 1"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=2,
        )
        has_fonts = result.returncode == 0 and bool(result.stdout.strip())
        debug(
            f"Font detection (Windows): returncode={result.returncode}, "
            f"has_fonts={has_fonts}"
        )
        return has_fonts
    except Exception as exc:
        debug(f"Font detection (Windows) failed: {exc!r}")
        return False


def _check_posix_fonts() -> bool:
    try:
        result = subprocess.run(
            ["fc-list", ":", "family"], capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0:
            found = _has_indicator(result.stdout.lower())
            debug(
                f"Font detection (POSIX): returncode={result.returncode}, found={found}"
            )
            return found
    except Exception as exc:
        debug(f"Font detection (POSIX) failed: {exc!r}")
    return False


@lru_cache(maxsize=1)
def check_installed_nerd_fonts() -> bool:
    """Check if nerd fonts are installed on the system."""
    if os.name == "nt":
        return _check_windows_fonts()

    if sys.platform == "darwin":
        return _check_mac_font_dirs() or _check_mac_system_profiler()

    return _check_posix_fonts()


@lru_cache(maxsize=1)
def has_nerd_fonts() -> bool:
    """Detect if nerd fonts are available in the terminal."""
    nerd_env = os.getenv("NERDFONTS") or os.getenv("NERD_FONTS")
    if nerd_env and nerd_env.lower() in ("1", "true", "yes", "on"):
        debug("Nerd fonts: enabled via NERDFONTS/NERD_FONTS")
        return True

    for var_name in ("FONT_NAME", "TERM_FONT"):
        value = os.getenv(var_name, "").lower()
        if value and _has_indicator(value):
            debug(f"Nerd fonts: enabled via {var_name}={value!r}")
            return True

    if os.getenv("RAZTINT_SKIP_SYSTEM_FONT_SCAN", "").lower() in (
        "1",
        "true",
        "yes",
        "on",
    ):
        debug(
            "Nerd fonts: skipping system font scan due to RAZTINT_SKIP_SYSTEM_FONT_SCAN"
        )
        return False

    return check_installed_nerd_fonts()
