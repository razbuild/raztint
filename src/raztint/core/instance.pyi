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
    pending: _IconFn
    debug: _IconFn

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
