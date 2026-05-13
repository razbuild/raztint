from importlib.metadata import version

from .core import RazTint

__version__ = version("raztint")

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
bright_red = tint.bright_red
bright_green = tint.bright_green
bright_yellow = tint.bright_yellow
bright_blue = tint.bright_blue
bright_magenta = tint.bright_magenta
bright_cyan = tint.bright_cyan
bright_white = tint.bright_white

bg_black = tint.bg_black
bg_red = tint.bg_red
bg_green = tint.bg_green
bg_yellow = tint.bg_yellow
bg_blue = tint.bg_blue
bg_magenta = tint.bg_magenta
bg_cyan = tint.bg_cyan
bg_white = tint.bg_white
bg_gray = tint.bg_gray
bg_bright_red = tint.bg_bright_red
bg_bright_green = tint.bg_bright_green
bg_bright_yellow = tint.bg_bright_yellow
bg_bright_blue = tint.bg_bright_blue
bg_bright_magenta = tint.bg_bright_magenta
bg_bright_cyan = tint.bg_bright_cyan
bg_bright_white = tint.bg_bright_white

bold = tint.bold
dim = tint.dim
italic = tint.italic
underline = tint.underline
strikethrough = tint.strikethrough

format_text = tint.format_text

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
    "format_text",
    "__version__",
]
