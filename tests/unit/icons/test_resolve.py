import os
from unittest import mock

import pytest

from raztint.core import RazTint
from raztint.icons.resolve import resolve_icon


class TestResolveIcon:
    def test_unknown_icon_raises(self, raztint_color_on: RazTint) -> None:
        with pytest.raises(ValueError, match="Unknown icon"):
            resolve_icon(
                raztint_color_on,
                "missing",
                has_nerd_fonts=lambda: False,
            )

    def test_ascii_mode(self, raztint_color_off: RazTint) -> None:
        raztint_color_off.icon_mode = "ascii"
        result = resolve_icon(raztint_color_off, "err", has_nerd_fonts=lambda: False)
        assert result == "[ERR]"

    def test_auto_mode_respects_force_nerd_env(self, raztint_color_on: RazTint) -> None:
        with mock.patch.dict(os.environ, {"RAZTINT_USE_NERD_ICONS": "1"}, clear=True):
            result = resolve_icon(
                raztint_color_on,
                "ok",
                mode="auto",
                has_nerd_fonts=lambda: False,
            )
        assert "[󰄬]" in result

    def test_nerd_fallback_to_std(self, raztint_color_on: RazTint) -> None:
        raztint_color_on.icons = {
            "OK": {"nerd": "", "std": "[✓]", "ascii": "[OK]", "color": "GREEN"},
        }
        result = resolve_icon(
            raztint_color_on, "ok", mode="nerd", has_nerd_fonts=lambda: True
        )
        assert result.startswith("\033[") and "[✓]" in result

    def test_auto_mode_std_fallback(self, raztint_color_on: RazTint) -> None:
        raztint_color_on.icons = {
            "OK": {"nerd": "", "std": "[✓]", "ascii": "[OK]", "color": "GREEN"},
        }
        result = resolve_icon(
            raztint_color_on, "ok", mode="auto", has_nerd_fonts=lambda: False
        )
        assert result.startswith("\033[") and "[✓]" in result

    def test_auto_mode_ascii_fallback(self, raztint_color_on: RazTint) -> None:
        raztint_color_on.icons = {
            "OK": {"nerd": "", "std": "", "ascii": "[OK]", "color": "GREEN"},
        }
        result = resolve_icon(
            raztint_color_on, "ok", mode="auto", has_nerd_fonts=lambda: False
        )
        assert result.startswith("\033[") and "[OK]" in result

    def test_std_mode(self, raztint_color_on: RazTint) -> None:
        raztint_color_on.icons = {
            "OK": {"nerd": "[󰄬]", "std": "[✓]", "ascii": "[OK]", "color": "GREEN"},
        }
        result = resolve_icon(
            raztint_color_on, "ok", mode="std", has_nerd_fonts=lambda: True
        )
        assert result.startswith("\033[") and "[✓]" in result

    def test_std_mode_ascii_fallback(self, raztint_color_on: RazTint) -> None:
        raztint_color_on.icons = {
            "OK": {"nerd": "[󰄬]", "std": "", "ascii": "[OK]", "color": "GREEN"},
        }
        result = resolve_icon(
            raztint_color_on, "ok", mode="std", has_nerd_fonts=lambda: True
        )
        assert result.startswith("\033[") and "[OK]" in result
