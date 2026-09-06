from collections.abc import Callable

from .protocols import FormatTarget


def register_dynamic_methods(instance: FormatTarget) -> None:
    """Attach color, background, style, and icon callables to a RazTint instance."""
    colors = instance.colors
    backgrounds = instance.backgrounds
    styles = instance.styles
    icons = instance.icons

    for name, code in colors.items():
        setattr(instance, name.lower(), _make_color_func(instance, code))

    for name, code in backgrounds.items():
        setattr(instance, name.lower(), _make_background_func(instance, code))

    for name, (on_code, off_code) in styles.items():
        setattr(instance, name.lower(), _make_style_func(instance, on_code, off_code))

    for name, data in icons.items():
        color_key = data.get("color", "WHITE")
        color_code = colors.get(color_key, "37")
        setattr(instance, name.lower(), _make_icon_func(instance, data, color_code))


def _make_color_func(instance: FormatTarget, code: str) -> Callable[[str], str]:
    def fn(text: str) -> str:
        return instance.color(text, code)

    return fn


def _make_background_func(
    instance: FormatTarget,
    code: str,
) -> Callable[[str], str]:
    def fn(text: str) -> str:
        return instance.background(text, code)

    return fn


def _make_style_func(
    instance: FormatTarget,
    on_code: str,
    off_code: str,
) -> Callable[[str], str]:
    def fn(text: str) -> str:
        return instance.style(text, on_code, off_code)

    return fn


def _make_icon_func(
    instance: FormatTarget,
    data: dict[str, str],
    code: str,
) -> Callable[[], str]:
    def fn() -> str:
        if instance.icon_mode == "nerd":
            symbol = data["nerd"]
        elif instance.icon_mode == "std":
            symbol = data["std"]
        else:
            symbol = data["ascii"]

        return instance.color(symbol, code)

    return fn
