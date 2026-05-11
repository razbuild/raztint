from collections.abc import Callable

from .colors import COLORS
from .env_detect import get_icon_mode, supports_color
from .icons import ICONS
from .styles import STYLES


class RazTint:
    """A zero-dependency Python library for ANSI coloring and smart CLI icons."""

    def __init__(self) -> None:
        self.colors = COLORS
        self.icons = ICONS
        self.styles = STYLES

        self.use_color: bool = supports_color()
        self.icon_mode: str = get_icon_mode()

        for name, code in self.colors.items():
            setattr(self, name.lower(), self._make_color_func(code))

        for name, (on, off) in self.styles.items():
            setattr(self, name.lower(), self._make_style_func(on, off))

        for name, data in self.icons.items():
            color_key = data.get("color", "WHITE")
            color_code = self.colors.get(color_key, "37")
            setattr(
                self,
                name,
                self._make_icon_func(data, color_code),
            )

    @staticmethod
    def _has_nerd_fonts() -> bool:
        """Backward-compatible nerd font detection hook."""
        from .font_detect import has_nerd_fonts

        return has_nerd_fonts()

    def _make_color_func(self, code: str) -> Callable[[str], str]:
        return lambda text: self.color(text, code)

    def _make_style_func(self, on: str, off: str) -> Callable[[str], str]:
        return lambda text: self.style(text, on, off)

    def _make_icon_func(self, data: dict[str, str], code: str) -> Callable[[], str]:
        def fn() -> str:
            if self.icon_mode == "nerd":
                symbol = data["nerd"]
            elif self.icon_mode == "std":
                symbol = data["std"]
            else:
                symbol = data["ascii"]

            return self.color(symbol, code)

        return fn

    def color(self, text: str, fg_code: str) -> str:
        """Apply ANSI color code to text."""
        if not self.use_color:
            return text
        return f"\033[{fg_code}m{text}\033[0m"

    def style(self, text: str, on_code: str, off_code: str) -> str:
        """Apply ANSI style to text with style-specific reset.

        Uses a targeted reset code (e.g. 22, 23, 24) instead of the
        generic \033[0m so that any previously applied colors are preserved.
        """
        if not self.use_color:
            return text
        return f"\033[{on_code}m{text}\033[{off_code}m"

    def set_color(self, enabled: bool) -> None:
        """Enable or disable color output programmatically."""
        self.use_color = enabled
