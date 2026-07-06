import pyperf

from raztint.core.ansi import apply_color
from raztint.data.colors import COLORS
from raztint.icons.registry import ICONS
from raztint.icons.resolve import resolve_icon


class _MockIconHost:
    """Minimal stand-in for the real IconHost protocol implementation,
    built only to exercise resolve_icon() in isolation for benchmarking.
    """

    icons = ICONS
    icon_mode = "auto"
    colors = COLORS

    @staticmethod
    def color(symbol: str, color_code: str) -> str:
        return apply_color(symbol, color_code, use_color=True)


def benchmark_icon_fallback_logic():
    ctx = _MockIconHost()
    # Cycle through every real icon name to exercise the "auto" fallback branch
    icon_queries = ["ok", "err", "warn", "info", "pending", "debug"] * 25
    for query in icon_queries:
        resolve_icon(ctx, query, has_nerd_fonts=lambda: False)


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_icon_resolution", benchmark_icon_fallback_logic)
