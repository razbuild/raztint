"""ANSI style codes for text styling.

Each style has an enable code and a disable (reset) code.
Using style-specific reset codes preserves any existing color styling.
"""

STYLES: dict[str, tuple[str, str]] = {
    "BOLD": ("1", "22"),
    "DIM": ("2", "22"),
    "ITALIC": ("3", "23"),
    "UNDERLINE": ("4", "24"),
    "STRIKETHROUGH": ("9", "29"),
}