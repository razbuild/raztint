from collections.abc import Callable

from ..data.types import (
    BackgroundColorName,
    ColorName,
    IconMode,
    IntentName,
    StyleName,
)
from ..formatting.paint import UNSET, IconArg
from ..security.masking import MaskRule

_TextFn = Callable[[str], str]
_IconFn = Callable[[], str]

class RazTint:
    colors: dict[str, str]
    backgrounds: dict[str, str]
    icons: dict[str, dict[str, str]]
    styles: dict[str, tuple[str, str]]
    use_color: bool
    icon_mode: IconMode

    ok: _IconFn
    err: _IconFn
    warn: _IconFn
    info: _IconFn
    black: _TextFn
    red: _TextFn
    green: _TextFn
    yellow: _TextFn
    blue: _TextFn
    magenta: _TextFn
    cyan: _TextFn
    white: _TextFn
    gray: _TextFn
    bright_red: _TextFn
    bright_green: _TextFn
    bright_yellow: _TextFn
    bright_blue: _TextFn
    bright_magenta: _TextFn
    bright_cyan: _TextFn
    bright_white: _TextFn
    bg_black: _TextFn
    bg_red: _TextFn
    bg_green: _TextFn
    bg_yellow: _TextFn
    bg_blue: _TextFn
    bg_magenta: _TextFn
    bg_cyan: _TextFn
    bg_white: _TextFn
    bg_gray: _TextFn
    bg_bright_red: _TextFn
    bg_bright_green: _TextFn
    bg_bright_yellow: _TextFn
    bg_bright_blue: _TextFn
    bg_bright_magenta: _TextFn
    bg_bright_cyan: _TextFn
    bg_bright_white: _TextFn
    bold: _TextFn
    dim: _TextFn
    italic: _TextFn
    underline: _TextFn
    strikethrough: _TextFn

    def __init__(self) -> None: ...
    @staticmethod
    def _has_nerd_fonts() -> bool: ...
    def color(self, text: str, fg_code: str) -> str: ...
    def background(self, text: str, bg_code: str) -> str: ...
    def style(self, text: str, on_code: str, off_code: str) -> str: ...
    def set_color(self, enabled: bool) -> None: ...
    def _resolve_icon(self, icon_name: str, mode: str | None = None) -> str: ...
    def format_text(
        self,
        text: str,
        color: ColorName | int | None = None,
        bg: BackgroundColorName | int | None = None,
        styles: StyleName | list[StyleName] | None = None,
        reset: bool = True,
        icon: IconArg = UNSET,
        icon_mode: IconMode | None = None,
        redact: bool = False,
        redact_rules: list[MaskRule] | None = None,
        intent: IntentName | None = None,
    ) -> str: ...
    def rgb(self, text: str, r: int, g: int, b: int) -> str: ...
    def bg_rgb(self, text: str, r: int, g: int, b: int) -> str: ...
    def hex_color(self, text: str, hex_str: str) -> str: ...
    def bg_hex_color(self, text: str, hex_str: str) -> str: ...
    def color256(self, text: str, index: int) -> str: ...
    def bg_color256(self, text: str, index: int) -> str: ...
