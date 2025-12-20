from .raztint import RazTint

__version__ = "0.1.1"

tint = RazTint()

ok = tint.ok  # type: ignore[attr-defined]
err = tint.err  # type: ignore[attr-defined]
warn = tint.warn  # type: ignore[attr-defined]
info = tint.info  # type: ignore[attr-defined]

black = tint.black  # type: ignore[attr-defined]
red = tint.red  # type: ignore[attr-defined]
green = tint.green  # type: ignore[attr-defined]
yellow = tint.yellow  # type: ignore[attr-defined]
blue = tint.blue  # type: ignore[attr-defined]
magenta = tint.magenta  # type: ignore[attr-defined]
cyan = tint.cyan  # type: ignore[attr-defined]
white = tint.white  # type: ignore[attr-defined]
gray = tint.gray  # type: ignore[attr-defined]

__all__ = [
    "RazTint",
    "tint",
    "ok",
    "err",
    "warn",
    "info",
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "gray",
    "__version__",
]
