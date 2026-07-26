from ..data import BACKGROUND_LOOKUP, FOREGROUND_LOOKUP, STYLE_LOOKUP
from ..data.types import StyleName

_VALID_FG = range(30, 38), range(90, 98)
_VALID_BG = range(40, 48), range(100, 108)


def _parse_hex(hex_str: str) -> tuple[int, int, int]:
    """Parse hex color string to RGB tuple."""
    h = hex_str.lstrip("#")
    if len(h) != 6:
        raise ValueError(
            f"hex color expects a 6-digit hex string like '#FF6432', got {hex_str!r}"
        )
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_str!r}")
    return r, g, b


def _validate_rgb(r: int, g: int, b: int) -> None:
    """Validate RGB values are in range 0-255."""
    for name, val in (("r", r), ("g", g), ("b", b)):
        if not isinstance(val, int) or not (0 <= val <= 255):
            raise ValueError(f"RGB channel '{name}' must be an int 0-255, got {val!r}")


def _validate_color256_index(index: int) -> None:
    """Validate 256-color palette index."""
    if not isinstance(index, int) or not (0 <= index <= 255):
        raise ValueError(f"256-color index must be an int 0-255, got {index!r}")


def get_color_code(
    color: str | int | tuple[int, int, int] | None, colors: dict[str, str]
) -> str | None:
    """Resolve any color value to an ANSI foreground code.

    Handles:
    - None → None
    - str starting with "#" → hex RGB
    - str (other) → named color
    - int → 256-color index or standard ANSI code
    - tuple[int, int, int] → 24-bit RGB
    """
    if color is None:
        return None

    if isinstance(color, tuple):
        # RGB tuple
        r, g, b = color
        _validate_rgb(r, g, b)
        return f"38;2;{r};{g};{b}"

    if isinstance(color, int):
        # ANSI code (standard 30-37, 90-97 or 256-color 0-255)
        if any(color in r for r in _VALID_FG):
            # Standard ANSI foreground
            return str(color)
        # Try as 256-color index
        _validate_color256_index(color)
        return f"38;5;{color}"

    if isinstance(color, str):
        # Hex string or named color
        if color.startswith("#"):
            r, g, b = _parse_hex(color)
            return f"38;2;{r};{g};{b}"
        # Named color
        code = FOREGROUND_LOOKUP.get(color) or FOREGROUND_LOOKUP.get(color.upper())
        if code is not None:
            return code
        raise ValueError(
            f"Unknown color: {color!r}. "
            f"Valid colors: {', '.join(sorted(colors.keys()))}"
        )

    raise TypeError(
        "color must be str, int, tuple[int,int,int], or None, "
        f"got {type(color).__name__}"
    )


def get_background_code(
    bg: str | int | tuple[int, int, int] | None, backgrounds: dict[str, str]
) -> str | None:
    """Resolve any background color value to an ANSI background code.

    Handles:
    - None → None
    - str starting with "#" → hex RGB
    - str (other) → named color
    - int → 256-color index or standard ANSI code
    - tuple[int, int, int] → 24-bit RGB
    """
    if bg is None:
        return None

    if isinstance(bg, tuple):
        # RGB tuple
        r, g, b = bg
        _validate_rgb(r, g, b)
        return f"48;2;{r};{g};{b}"

    if isinstance(bg, int):
        # ANSI code (standard 40-47, 100-107 or 256-color 0-255)
        if any(bg in r for r in _VALID_BG):
            # Standard ANSI background
            return str(bg)
        # Try as 256-color index
        _validate_color256_index(bg)
        return f"48;5;{bg}"

    if isinstance(bg, str):
        # Hex string or named color
        if bg.startswith("#"):
            r, g, b = _parse_hex(bg)
            return f"48;2;{r};{g};{b}"
        # Named color
        code = BACKGROUND_LOOKUP.get(bg) or BACKGROUND_LOOKUP.get(bg.upper())
        if code is None and not bg.upper().startswith("BG_"):
            code = BACKGROUND_LOOKUP.get(f"BG_{bg.upper()}")
        if code is not None:
            return code
        raise ValueError(
            f"Unknown background color: {bg!r}. "
            f"Valid colors: {', '.join(sorted(backgrounds.keys()))}"
        )

    raise TypeError(
        f"bg must be str, int, tuple[int,int,int], or None, got {type(bg).__name__}"
    )


def get_style_codes(
    style_name: str, styles: dict[str, tuple[str, str]]
) -> tuple[str, str]:
    codes = STYLE_LOOKUP.get(style_name) or STYLE_LOOKUP.get(style_name.lower())
    if codes is not None:
        return codes
    raise ValueError(
        f"Unknown style: {style_name!r}. "
        f"Valid styles: {', '.join(sorted(styles.keys()))}"
    )


def normalize_styles(
    styles: StyleName | list[StyleName] | None,
) -> list[str]:
    if styles is None:
        return []
    if isinstance(styles, str):
        return [styles.lower()]
    if isinstance(styles, list):
        return [s.lower() for s in styles]
    raise TypeError(
        f"styles must be str, list[str], or None, got {type(styles).__name__}"
    )
