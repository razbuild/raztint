"""Literal types for IDE autocompletion (Pylance, Pyright, ty)."""

from typing import Literal

# Foreground color names accepted by paint().
ColorName = Literal[
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
]

# Background color names (with or without ``bg_`` prefix in paint()).
BackgroundColorName = Literal[
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
]

StyleName = Literal["bold", "dim", "italic", "underline", "strikethrough"]

IconName = Literal["ok", "err", "warn", "info", "pending", "debug"]

IconMode = Literal["auto", "nerd", "std", "ascii"]

IntentName = Literal["success", "danger", "warning", "pending", "debug", "info"]
