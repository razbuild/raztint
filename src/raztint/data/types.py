from typing import Literal

# Color value: named color string, 256-color index, RGB tuple, or hex string.
ColorValue = str | int | tuple[int, int, int]

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

IntentName = Literal["success", "error", "warning", "pending", "debug", "info"]
