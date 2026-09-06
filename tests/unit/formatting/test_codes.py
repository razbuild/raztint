import pytest

from raztint.data import BACKGROUND_COLORS, COLORS, STYLES
from raztint.formatting.codes import (
    get_background_code,
    get_color_code,
    get_style_codes,
    normalize_styles,
)


class TestFormattingCodes:
    def test_get_color_code_by_name(self) -> None:
        assert get_color_code("red", COLORS) == "31"

    def test_get_color_code_by_int(self) -> None:
        assert get_color_code(91, COLORS) == "91"

    def test_get_color_code_none(self) -> None:
        assert get_color_code(None, COLORS) is None

    def test_get_color_code_invalid_name(self) -> None:
        with pytest.raises(ValueError, match="Unknown color"):
            get_color_code("nope", COLORS)

    def test_get_color_code_invalid_int(self) -> None:
        with pytest.raises(ValueError, match="256-color index"):
            get_color_code(256, COLORS)

    def test_get_background_code_prefixed_and_short(self) -> None:
        assert get_background_code("bg_red", BACKGROUND_COLORS) == "41"
        assert get_background_code("red", BACKGROUND_COLORS) == "41"

    def test_get_background_code_invalid(self) -> None:
        with pytest.raises(ValueError, match="Unknown background"):
            get_background_code("nope", BACKGROUND_COLORS)

    def test_get_style_codes(self) -> None:
        assert get_style_codes("bold", STYLES) == ("1", "22")

    def test_normalize_styles_list_and_string(self) -> None:
        assert normalize_styles("Bold") == ["bold"]
        assert normalize_styles(["Underline"]) == ["underline"]

    def test_normalize_styles_invalid_type(self) -> None:
        with pytest.raises(TypeError, match="styles must be"):
            normalize_styles(42)


class TestColorValueTypes:
    # RGB tuple support
    def test_get_color_code_rgb_tuple(self) -> None:
        """RGB tuple for foreground color."""
        code = get_color_code((255, 120, 0), COLORS)
        assert code == "38;2;255;120;0"

    def test_get_background_code_rgb_tuple(self) -> None:
        """RGB tuple for background color."""
        code = get_background_code((30, 30, 30), BACKGROUND_COLORS)
        assert code == "48;2;30;30;30"

    def test_get_color_code_rgb_tuple_black(self) -> None:
        """RGB tuple for black."""
        code = get_color_code((0, 0, 0), COLORS)
        assert code == "38;2;0;0;0"

    def test_get_color_code_rgb_tuple_white(self) -> None:
        """RGB tuple for white."""
        code = get_color_code((255, 255, 255), COLORS)
        assert code == "38;2;255;255;255"

    def test_get_color_code_rgb_invalid_channel_low(self) -> None:
        """RGB tuple with channel below 0."""
        with pytest.raises(ValueError, match="RGB channel.*0-255"):
            get_color_code((-1, 100, 100), COLORS)

    def test_get_color_code_rgb_invalid_channel_high(self) -> None:
        """RGB tuple with channel above 255."""
        with pytest.raises(ValueError, match="RGB channel.*0-255"):
            get_color_code((256, 100, 100), COLORS)

    def test_get_color_code_rgb_invalid_type(self) -> None:
        """RGB tuple with non-int value."""
        with pytest.raises(ValueError, match="RGB channel"):
            get_color_code(("255", 100, 100), COLORS)  # type: ignore[arg-type]

    # Hex string support
    def test_get_color_code_hex(self) -> None:
        """Hex color string for foreground."""
        code = get_color_code("#ff7800", COLORS)
        assert code == "38;2;255;120;0"

    def test_get_color_code_hex_uppercase(self) -> None:
        """Hex color string uppercase."""
        code = get_color_code("#FF7800", COLORS)
        assert code == "38;2;255;120;0"

    def test_get_background_code_hex(self) -> None:
        """Hex color string for background."""
        code = get_background_code("#202020", BACKGROUND_COLORS)
        assert code == "48;2;32;32;32"

    def test_get_color_code_hex_black(self) -> None:
        """Hex color for black."""
        code = get_color_code("#000000", COLORS)
        assert code == "38;2;0;0;0"

    def test_get_color_code_hex_white(self) -> None:
        """Hex color for white."""
        code = get_color_code("#FFFFFF", COLORS)
        assert code == "38;2;255;255;255"

    def test_get_color_code_hex_invalid_length(self) -> None:
        """Hex color with invalid length."""
        with pytest.raises(ValueError, match="6-digit hex string"):
            get_color_code("#fff", COLORS)

    def test_get_color_code_hex_invalid_chars(self) -> None:
        """Hex color with invalid characters."""
        with pytest.raises(ValueError, match="Invalid hex color"):
            get_color_code("#gggggg", COLORS)

    # 256-color index support
    def test_get_color_code_256_index(self) -> None:
        """256-color palette index for foreground."""
        code = get_color_code(208, COLORS)
        assert code == "38;5;208"

    def test_get_color_code_256_index_zero(self) -> None:
        """256-color index 0."""
        code = get_color_code(0, COLORS)
        assert code == "38;5;0"

    def test_get_color_code_256_index_max(self) -> None:
        """256-color index 255."""
        code = get_color_code(255, COLORS)
        assert code == "38;5;255"

    def test_get_background_code_256_index(self) -> None:
        """256-color palette index for background."""
        code = get_background_code(236, BACKGROUND_COLORS)
        assert code == "48;5;236"

    def test_get_color_code_256_index_invalid_low(self) -> None:
        """256-color index below 0."""
        with pytest.raises(ValueError, match="256-color index.*0-255"):
            get_color_code(-1, COLORS)

    def test_get_color_code_256_index_invalid_high(self) -> None:
        """256-color index above 255."""
        with pytest.raises(ValueError, match="256-color index.*0-255"):
            get_color_code(256, COLORS)

    # Standard ANSI codes (30-37, 90-97 for FG; 40-47, 100-107 for BG)
    def test_get_color_code_standard_ansi_low(self) -> None:
        """Standard ANSI foreground code (30-37)."""
        assert get_color_code(30, COLORS) == "30"
        assert get_color_code(37, COLORS) == "37"

    def test_get_color_code_standard_ansi_high(self) -> None:
        """Bright ANSI foreground code (90-97)."""
        assert get_color_code(90, COLORS) == "90"
        assert get_color_code(97, COLORS) == "97"

    def test_get_background_code_standard_ansi_low(self) -> None:
        """Standard ANSI background code (40-47)."""
        assert get_background_code(40, BACKGROUND_COLORS) == "40"
        assert get_background_code(47, BACKGROUND_COLORS) == "47"

    def test_get_background_code_standard_ansi_high(self) -> None:
        """Bright ANSI background code (100-107)."""
        assert get_background_code(100, BACKGROUND_COLORS) == "100"
        assert get_background_code(107, BACKGROUND_COLORS) == "107"

    # Type validation
    def test_get_color_code_invalid_type(self) -> None:
        """Invalid color type."""
        with pytest.raises(TypeError, match="must be str, int, tuple"):
            get_color_code(["red"], COLORS)  # type: ignore[arg-type]

    def test_get_background_code_invalid_type(self) -> None:
        """Invalid background color type."""
        with pytest.raises(TypeError, match="must be str, int, tuple"):
            get_background_code(["red"], BACKGROUND_COLORS)  # type: ignore[arg-type]

    # Backward compatibility: named colors still work
    def test_get_color_code_named_lowercase(self) -> None:
        """Named color lowercase."""
        assert get_color_code("red", COLORS) == "31"

    def test_get_color_code_named_uppercase(self) -> None:
        """Named color uppercase."""
        assert get_color_code("RED", COLORS) == "31"

    def test_get_background_code_named_with_prefix(self) -> None:
        """Named background with bg_ prefix."""
        assert get_background_code("bg_red", BACKGROUND_COLORS) == "41"

    def test_get_background_code_named_without_prefix(self) -> None:
        """Named background without bg_ prefix."""
        assert get_background_code("red", BACKGROUND_COLORS) == "41"
