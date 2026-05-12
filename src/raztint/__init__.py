from importlib.metadata import version

from .core import RazTint

__version__ = version("raztint")

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

bg_black = tint.bg_black  # type: ignore
bg_red = tint.bg_red  # type: ignore
bg_green = tint.bg_green  # type: ignore
bg_yellow = tint.bg_yellow  # type: ignore
bg_blue = tint.bg_blue  # type: ignore
bg_magenta = tint.bg_magenta  # type: ignore
bg_cyan = tint.bg_cyan  # type: ignore
bg_white = tint.bg_white  # type: ignore
bg_gray = tint.bg_gray  # type: ignore
bg_bright_red = tint.bg_bright_red  # type: ignore
bg_bright_green = tint.bg_bright_green  # type: ignore
bg_bright_yellow = tint.bg_bright_yellow  # type: ignore
bg_bright_blue = tint.bg_bright_blue  # type: ignore
bg_bright_magenta = tint.bg_bright_magenta  # type: ignore
bg_bright_cyan = tint.bg_bright_cyan  # type: ignore
bg_bright_white = tint.bg_bright_white  # type: ignore

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
    "bg_black",
    "bg_red",
    "bg_green",
    "bg_yellow",
    "bg_blue",
    "bg_magenta",
    "bg_cyan",
    "bg_white",
    "bg_gray",
    "bg_bright_red",
    "bg_bright_green",
    "bg_bright_yellow",
    "bg_bright_blue",
    "bg_bright_magenta",
    "bg_bright_cyan",
    "bg_bright_white",
    "bold",
    "dim",
    "italic",
    "underline",
    "strikethrough",
    "__version__",
]
