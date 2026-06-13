from typing import cast

from ..core.protocols import DynamicInstance, FormatTarget, IconHost
from ..data import BACKGROUND_COLORS, COLORS, STYLES
from ..data.types import (
    BackgroundColorName,
    ColorName,
    IconMode,
    IntentName,
    StyleName,
)
from ..detect import supports_color
from ..formatting.paint import UNSET, IconArg
from ..formatting.paint import format_text as paint_text
from ..icons.registry import ICONS
from ..icons.resolve import resolve_icon
from ..security.masking import MaskRule
from .ansi import apply_background, apply_color, apply_style
from .builder import register_dynamic_methods
from .extended import color256_bg, color256_fg, hex_bg, hex_fg, rgb_bg, rgb_fg


class RazTint:
    """A zero-dependency Python library for ANSI coloring and smart CLI icons."""

    def __init__(self) -> None:
        self.colors = COLORS
        self.backgrounds = BACKGROUND_COLORS
        self.icons = ICONS
        self.styles = STYLES

        self.use_color: bool = supports_color()
        self.icon_mode: IconMode = self._get_icon_mode()

        register_dynamic_methods(cast(DynamicInstance, self))

    @staticmethod
    def _has_nerd_fonts() -> bool:
        from ..detect.fonts import has_nerd_fonts

        return has_nerd_fonts()

    @classmethod
    def _get_icon_mode(cls) -> IconMode:
        from ..detect.env import get_icon_mode

        return get_icon_mode(nerd_font_detector=cls._has_nerd_fonts)

    def color(self, text: str, fg_code: str) -> str:
        return apply_color(text, fg_code, use_color=self.use_color)

    def background(self, text: str, bg_code: str) -> str:
        return apply_background(text, bg_code, use_color=self.use_color)

    def style(self, text: str, on_code: str, off_code: str) -> str:
        return apply_style(text, on_code, off_code, use_color=self.use_color)

    def set_color(self, enabled: bool) -> None:
        self.use_color = enabled

    def _resolve_icon(self, icon_name: str, mode: str | None = None) -> str:
        return resolve_icon(
            cast(IconHost, self),
            icon_name,
            mode=mode,
            has_nerd_fonts=self._has_nerd_fonts,
        )

    # ── Extended color methods ────────────────────────────────────────────────

    def rgb(self, text: str, r: int, g: int, b: int) -> str:
        """Apply a 24-bit True Color foreground via RGB channels."""
        return rgb_fg(text, r, g, b, use_color=self.use_color)

    def bg_rgb(self, text: str, r: int, g: int, b: int) -> str:
        """Apply a 24-bit True Color background via RGB channels."""
        return rgb_bg(text, r, g, b, use_color=self.use_color)

    def hex_color(self, text: str, hex_str: str) -> str:
        """Apply a 24-bit True Color foreground via hex string (e.g. '#FF6432')."""
        return hex_fg(text, hex_str, use_color=self.use_color)

    def bg_hex_color(self, text: str, hex_str: str) -> str:
        """Apply a 24-bit True Color background via hex string."""
        return hex_bg(text, hex_str, use_color=self.use_color)

    def color256(self, text: str, index: int) -> str:
        """Apply a 256-color palette foreground (index 0-255)."""
        return color256_fg(text, index, use_color=self.use_color)

    def bg_color256(self, text: str, index: int) -> str:
        """Apply a 256-color palette background (index 0-255)."""
        return color256_bg(text, index, use_color=self.use_color)

    # ── format_text ───────────────────────────────────────────────────────────

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
    ) -> str:
        return paint_text(
            cast(FormatTarget, self),
            text,
            color=color,
            bg=bg,
            styles=styles,
            reset=reset,
            icon=icon,
            icon_mode=icon_mode,
            redact=redact,
            redact_rules=redact_rules,
            intent=intent,
        )
