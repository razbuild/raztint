from .core import RazTint

__version__ = "0.3.0"

tint = RazTint()

ok = tint.ok  # type: ignore
err = tint.err  # type: ignore
warn = tint.warn  # type: ignore
info = tint.info  # type: ignore

black = tint.black  # type: ignore
red = tint.red  # type: ignore
green = tint.green  # type: ignore
yellow = tint.yellow  # type: ignore
blue = tint.blue  # type: ignore
magenta = tint.magenta  # type: ignore
cyan = tint.cyan  # type: ignore
white = tint.white  # type: ignore
gray = tint.gray  # type: ignore
bright_red = tint.bright_red  # type: ignore
bright_green = tint.bright_green  # type: ignore
bright_yellow = tint.bright_yellow  # type: ignore
bright_blue = tint.bright_blue  # type: ignore
bright_magenta = tint.bright_magenta  # type: ignore
bright_cyan = tint.bright_cyan  # type: ignore
bright_white = tint.bright_white  # type: ignore

bold = tint.bold  # type: ignore
dim = tint.dim  # type: ignore
italic = tint.italic  # type: ignore
underline = tint.underline  # type: ignore
strikethrough = tint.strikethrough  # type: ignore

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
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
    "bold",
    "dim",
    "italic",
    "underline",
    "strikethrough",
    "__version__",
]
