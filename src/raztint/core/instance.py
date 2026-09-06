import os
import sys
from collections.abc import Hashable, Mapping
from typing import TypeVar, cast

from ..core.protocols import FormatTarget, IconHost
from ..data import BACKGROUND_COLORS, COLORS, STYLES
from ..data.intents import _get_intents
from ..data.types import (
    ColorValue,
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
from .transient import TransientLine

T = TypeVar("T", bound=Hashable)


class RazTint:
    """A zero-dependency ANSI styling and icon library for CLI output."""

    def __init__(self) -> None:
        self.colors = COLORS
        self.backgrounds = BACKGROUND_COLORS
        self.icons = ICONS
        self.styles = STYLES

        self.use_color: bool = supports_color()
        self.icon_mode: IconMode = self._get_icon_mode()

        register_dynamic_methods(cast(FormatTarget, self))

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

    def intents(
        self, name: str | None = None
    ) -> dict[str, object] | dict[str, dict[str, object]]:
        return _get_intents(name)

    def transient(self, text: str) -> TransientLine:
        return TransientLine(text)

    def _resolve_icon(self, icon_name: str, mode: str | None = None) -> str:
        return resolve_icon(
            cast(IconHost, self),
            icon_name,
            mode=mode,
            has_nerd_fonts=self._has_nerd_fonts,
        )

    def case(
        self,
        value: T,
        cases: Mapping[T, tuple[str, IntentName]],
    ) -> str:
        try:
            text, intent = cases[value]
        except KeyError:
            raise ValueError(f"No case defined for {value!r}") from None

        return self.format_text(text, intent=intent)

    def format_text(
        self,
        text: str,
        color: ColorValue | None = None,
        bg: ColorValue | None = None,
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

    def preview(self) -> str:
        encoding = getattr(sys.stdout, "encoding", None) or "unknown"
        terminal = os.getenv("TERM") or "unknown"

        return (
            "RazTint\n"
            "────────────────────\n"
            f"Platform    {sys.platform}\n"
            f"Terminal    {terminal}\n"
            f"Encoding    {encoding}\n"
            f"Color       {'enabled' if self.use_color else 'disabled'}\n"
            f"Icon mode   {self.icon_mode}"
        )
