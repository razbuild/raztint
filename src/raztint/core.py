from collections.abc import Callable

from .colors import BACKGROUND_COLORS, COLORS
from .env_detect import get_icon_mode, supports_color
from .icons import ICONS
from .styles import STYLES


class RazTint:
    """A zero-dependency Python library for ANSI coloring and smart CLI icons."""

    def __init__(self) -> None:
        self.colors = COLORS
        self.backgrounds = BACKGROUND_COLORS
        self.icons = ICONS
        self.styles = STYLES

        self.use_color: bool = supports_color()
        self.icon_mode: str = get_icon_mode()

        for name, code in self.colors.items():
            setattr(self, name.lower(), self._make_color_func(code))

        for name, code in self.backgrounds.items():
            setattr(self, name.lower(), self._make_background_func(code))

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

    def _make_background_func(self, code: str) -> Callable[[str], str]:
        return lambda text: self.background(text, code)

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

    def background(self, text: str, bg_code: str) -> str:
        """Apply ANSI background color code to text."""
        if not self.use_color:
            return text
        return f"\033[{bg_code}m{text}\033[49m"

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

    def _get_color_code(self, color: str | int | None) -> str | None:
        """Get ANSI color code from color name or integer code.

        Args:
            color: Color name (e.g., "red", "bright_green"), integer ANSI code, or None.

        Returns:
            ANSI code string or None if color is None.

        Raises:
            ValueError: If color name is unknown or code is out of valid range.
        """
        if color is None:
            return None

        # If it's an integer, validate and return as string
        if isinstance(color, int):
            # Valid foreground colors: 30-37 (standard), 90-97 (bright)
            if (30 <= color <= 37) or (90 <= color <= 97):
                return str(color)
            raise ValueError(
                f"Invalid ANSI foreground color code: {color}. "
                f"Must be 30-37 (standard) or 90-97 (bright)."
            )

        # If it's a string, look it up in the color dictionary
        color_upper = color.upper()
        if color_upper in self.colors:
            return self.colors[color_upper]

        raise ValueError(
            f"Unknown color: {color!r}. "
            f"Valid colors: {', '.join(sorted(self.colors.keys()))}"
        )

    def _get_background_code(self, bg: str | int | None) -> str | None:
        """Get ANSI background color code from name or integer code.

        Args:
            bg: Background color name (e.g., "bg_red", "red", "bright_green"),
                integer ANSI code, or None.
                Accepts both "red" (converted to BG_RED) and "bg_red" formats.

        Returns:
            ANSI code string or None if bg is None.

        Raises:
            ValueError: If bg name is unknown or code is out of valid range.
        """
        if bg is None:
            return None

        # If it's an integer, validate and return as string
        if isinstance(bg, int):
            # Valid background colors: 40-47 (standard), 100-107 (bright)
            if (40 <= bg <= 47) or (100 <= bg <= 107):
                return str(bg)
            raise ValueError(
                f"Invalid ANSI background color code: {bg}. "
                f"Must be 40-47 (standard) or 100-107 (bright)."
            )

        # If it's a string, look it up in the background dictionary
        bg_upper = bg.upper()
        if bg_upper in self.backgrounds:
            return self.backgrounds[bg_upper]

        # Try converting foreground color name to background (e.g., "red" -> "BG_RED")
        bg_prefixed = f"BG_{bg_upper}"
        if bg_prefixed in self.backgrounds:
            return self.backgrounds[bg_prefixed]

        raise ValueError(
            f"Unknown background color: {bg!r}. "
            f"Valid colors: {', '.join(sorted(self.backgrounds.keys()))}"
        )

    def _get_style_codes(self, style_name: str) -> tuple[str, str]:
        """Get ANSI style codes (on, off) from style name.

        Args:
            style_name: Style name (e.g., "bold", "underline").

        Returns:
            Tuple of (on_code, off_code) strings.

        Raises:
            ValueError: If style name is unknown.
        """
        style_upper = style_name.upper()
        if style_upper in self.styles:
            return self.styles[style_upper]

        raise ValueError(
            f"Unknown style: {style_name!r}. "
            f"Valid styles: {', '.join(sorted(self.styles.keys()))}"
        )

    def _normalize_styles(self, styles: str | list[str] | None) -> list[str]:
        """Normalize styles argument to a list.

        Args:
            styles: A style name string, a list of style names, or None.

        Returns:
            A list of style names (normalized to lowercase).
        """
        if styles is None:
            return []
        if isinstance(styles, str):
            return [styles.lower()]
        if isinstance(styles, list):
            return [s.lower() for s in styles]
        raise TypeError(
            f"styles must be str, list[str], or None, got {type(styles).__name__}"
        )

    def format_text(
        self,
        text: str,
        color: str | int | None = None,
        bg: str | int | None = None,
        styles: str | list[str] | None = None,
        reset: bool = True,
    ) -> str:
        """Format text with color, background, and styles using a single call.

        This method provides a convenient way to apply multiple styles without
        deeply nested function calls. If color output is disabled (NO_COLOR,
        not a TTY, etc.), returns plain text.

        Args:
            text: The text to format.
            color: Foreground color name (e.g., "red", "bright_green") or
                ANSI code (31, 91).
            bg: Background color name (e.g., "bg_red") or ANSI code (41, 101).
            styles: Style name (e.g., "bold"), list of style names, or None.
            reset: If True, append a full reset code (\033[0m) after the text.
                   If False, only style-specific resets are applied (styles only).

        Returns:
            Formatted text with ANSI codes if color is enabled, plain text otherwise.

        Raises:
            ValueError: If color, bg, or style names are unknown.
            TypeError: If styles is not str, list[str], or None.

        Examples:
            # Single style and color
            result = tint.format_text("Error", color="red", styles="bold")

            # Multiple styles with background
            result = tint.format_text(
                "Alert",
                color="white",
                bg="red",
                styles=["bold", "underline"]
            )

            # Concatenation example (reset=False)
            part1 = tint.format_text("WARNING:", color="yellow", reset=False)
            part2 = tint.format_text(" Disk full", color="red")
            print(part1 + part2)
        """
        if not self.use_color:
            return text

        # Get color codes
        fg_code = self._get_color_code(color)
        bg_code = self._get_background_code(bg)

        # Normalize and validate styles
        style_list = self._normalize_styles(styles)
        style_codes: list[tuple[str, str]] = []
        for style_name in style_list:
            on, off = self._get_style_codes(style_name)
            style_codes.append((on, off))

        # Build the opening ANSI sequence
        codes: list[str] = []
        if fg_code:
            codes.append(fg_code)
        if bg_code:
            codes.append(bg_code)
        for on_code, _ in style_codes:
            codes.append(on_code)

        if not codes:
            # No formatting requested
            return text

        opening = f"\033[{';'.join(codes)}m"

        # Build the closing ANSI sequence
        if reset:
            # Full reset using \033[0m
            closing = "\033[0m"
        else:
            # Style-specific resets only (preserve colors)
            closing_codes: list[str] = []
            for _, off_code in style_codes:
                closing_codes.append(off_code)
            if closing_codes:
                closing = f"\033[{';'.join(closing_codes)}m"
            else:
                closing = ""

        return f"{opening}{text}{closing}"
