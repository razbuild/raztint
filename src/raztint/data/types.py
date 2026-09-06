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


# Color value: named color, 256-color index, or RGB tuple.
ColorValue = ColorName | str | int | tuple[int, int, int]

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
