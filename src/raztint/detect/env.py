import os
import sys
from collections.abc import Callable
from functools import lru_cache

from ..data.types import IconMode
from .debug import debug
from .fonts import has_nerd_fonts

TRUTHY_VALUES = frozenset({"1", "true", "yes", "on"})
_NERD_PROBE = "[󰄬]"


def env_enabled(name: str) -> bool:
    return os.getenv(name, "").lower() in TRUTHY_VALUES


def enable_windows_vt_mode() -> bool:
    import ctypes

    windll = getattr(ctypes, "windll", None)
    if windll is None or getattr(windll, "kernel32", None) is None:
        debug("Windows VT: windll/kernel32 not available")
        return False

    handle = windll.kernel32.GetStdHandle(-11)
    if handle in (0, -1):
        debug(f"Windows VT: invalid handle {handle!r}")
        return False

    mode = ctypes.c_uint32()
    if not windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        debug("Windows VT: GetConsoleMode failed")
        return False

    success = bool(windll.kernel32.SetConsoleMode(handle, mode.value | 0x0004))
    debug(f"Windows VT: SetConsoleMode -> {success}")
    return success


def supports_color() -> bool:
    if os.getenv("NO_COLOR") is not None or os.getenv("RAZTINT_NO_COLOR") is not None:
        debug("Color disabled by NO_COLOR/RAZTINT_NO_COLOR")
        return False

    if env_enabled("RAZTINT_FORCE_COLOR"):
        debug("Color forced by RAZTINT_FORCE_COLOR")
        return True

    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        debug("Color disabled: stdout is not a TTY")
        return False

    if os.name == "nt":
        debug("Color detection: Windows path")
        return enable_windows_vt_mode()

    term = os.getenv("TERM", "")
    result = bool(term and term.lower() != "dumb")
    debug(f"Color detection: TERM={term!r} -> {result}")
    return result


@lru_cache(maxsize=8)
def _encoding_supports_nerd(encoding: str) -> bool:
    try:
        _NERD_PROBE.encode(encoding)
        return True
    except Exception:
        return False


def clear_env_cache() -> None:
    """Clear cached encoding probes (for tests)."""
    _encoding_supports_nerd.cache_clear()


def get_icon_mode(*, nerd_font_detector: Callable[[], bool] | None = None) -> IconMode:
    if nerd_font_detector is None:
        nerd_font_detector = has_nerd_fonts

    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    if not _encoding_supports_nerd(encoding):
        debug(f"Icon mode: encoding {encoding!r} cannot encode Nerd icons, using ascii")
        return "ascii"

    if env_enabled("RAZTINT_USE_NERD_ICONS"):
        debug("Icon mode forced to 'nerd' via RAZTINT_USE_NERD_ICONS")
        return "nerd"

    if env_enabled("RAZTINT_NO_NERD_ICONS"):
        debug("Icon mode forced to 'std' via RAZTINT_NO_NERD_ICONS")
        return "std"

    if nerd_font_detector():
        debug("Icon mode: nerd fonts detected, using 'nerd'")
        return "nerd"

    debug("Icon mode: defaulting to 'std'")
    return "std"
