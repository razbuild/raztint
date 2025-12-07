from .raztint import RazTint

__version__ = "0.1.0"

tint = RazTint()

ok = tint.ok
err = tint.err
warn = tint.warn
info = tint.info

black = tint.black
red = tint.red
green = tint.green
yellow = tint.yellow
blue = tint.blue
magenta = tint.magenta
cyan = tint.cyan
white = tint.white
gray = tint.gray

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
