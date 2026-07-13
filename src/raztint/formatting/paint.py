from typing import cast

from ..core.protocols import FormatTarget
from ..data import INTENTS
from ..data.types import (
    BackgroundColorName,
    ColorName,
    IconMode,
    IconName,
    IntentName,
    StyleName,
)
from ..icons.resolve import resolve_icon
from ..security.masking import MaskRule
from ..security.masking import redact as mask_sensitive
from .codes import (
    get_background_code,
    get_color_code,
    get_style_codes,
    normalize_styles,
)

_RESET_FULL = "\033[0m"


class UnsetType:
    """Sentinel type for parameters that inherit intent defaults."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType()
IconArg = IconName | None | UnsetType


def _icon_prefix(
    instance: FormatTarget,
    icon: IconName,
    icon_mode: IconMode | None,
) -> str:
    return resolve_icon(
        instance,
        icon,
        mode=icon_mode,
        has_nerd_fonts=instance._has_nerd_fonts,
    )


def format_text(
    instance: FormatTarget,
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
    """Format text with color, background, styles, and an optional icon."""
    if intent is not None:
        cfg = INTENTS.get(intent.lower())
        if cfg is None:
            raise ValueError(
                f"Unknown intent: {intent!r}. "
                f"Valid intents: {', '.join(sorted(INTENTS.keys()))}"
            )
        if color is None:
            color = cfg.color
        if icon is UNSET:
            icon = cfg.icon
        if styles is None:
            styles = cfg.styles

    if icon is UNSET:
        icon = None

    active_icon = cast(IconName | None, icon)

    if redact:
        text = mask_sensitive(text, redact_rules)

    use_color = instance.use_color
    has_icon = active_icon is not None

    if not use_color:
        if not has_icon:
            return text
        assert active_icon is not None
        return f"{_icon_prefix(instance, active_icon, icon_mode)} {text}"

    if not has_icon and color is None and bg is None and not styles:
        return text

    prefix = ""
    if has_icon:
        assert active_icon is not None
        prefix = f"{_icon_prefix(instance, active_icon, icon_mode)} "

    fg_code = get_color_code(color, instance.colors)
    bg_code = get_background_code(bg, instance.backgrounds)

    style_list = normalize_styles(styles)
    if not prefix and not fg_code and not bg_code and not style_list:
        return text

    codes: list[str] = []
    if fg_code:
        codes.append(fg_code)
    if bg_code:
        codes.append(bg_code)

    style_codes: list[tuple[str, str]] = []
    for style_name in style_list:
        on, off = get_style_codes(style_name, instance.styles)
        style_codes.append((on, off))
        codes.append(on)

    if not codes:
        return f"{prefix}{text}"

    opening = f"\033[{';'.join(codes)}m"
    if reset:
        closing = _RESET_FULL
    elif style_codes:
        closing = f"\033[{';'.join(off for _, off in style_codes)}m"
    else:
        closing = ""

    return f"{prefix}{opening}{text}{closing}"
