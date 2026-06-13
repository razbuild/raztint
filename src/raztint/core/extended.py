"""Validation and application helpers for extended colors (True Color & 256-color)."""

from .ansi import apply_bg_color256, apply_bg_rgb, apply_color256, apply_rgb


def _validate_rgb(r: int, g: int, b: int) -> None:
    for name, val in (("r", r), ("g", g), ("b", b)):
        if not isinstance(val, int) or not (0 <= val <= 255):
            raise ValueError(f"RGB channel '{name}' must be an int 0-255, got {val!r}")


def _validate_index(index: int) -> None:
    if not isinstance(index, int) or not (0 <= index <= 255):
        raise ValueError(f"256-color index must be an int 0-255, got {index!r}")


def _parse_hex(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    if len(h) != 6:
        raise ValueError(
            f"hex_color expects a 6-digit hex string like '#FF6432', got {hex_str!r}"
        )
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_str!r}")
    return r, g, b


def rgb_fg(text: str, r: int, g: int, b: int, *, use_color: bool) -> str:
    _validate_rgb(r, g, b)
    return apply_rgb(text, r, g, b, use_color=use_color)


def rgb_bg(text: str, r: int, g: int, b: int, *, use_color: bool) -> str:
    _validate_rgb(r, g, b)
    return apply_bg_rgb(text, r, g, b, use_color=use_color)


def hex_fg(text: str, hex_str: str, *, use_color: bool) -> str:
    r, g, b = _parse_hex(hex_str)
    return apply_rgb(text, r, g, b, use_color=use_color)


def hex_bg(text: str, hex_str: str, *, use_color: bool) -> str:
    r, g, b = _parse_hex(hex_str)
    return apply_bg_rgb(text, r, g, b, use_color=use_color)


def color256_fg(text: str, index: int, *, use_color: bool) -> str:
    _validate_index(index)
    return apply_color256(text, index, use_color=use_color)


def color256_bg(text: str, index: int, *, use_color: bool) -> str:
    _validate_index(index)
    return apply_bg_color256(text, index, use_color=use_color)
