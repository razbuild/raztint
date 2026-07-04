import pyperf
from raztint.icons import IconRegistry # Assumes standard module layout

def benchmark_icon_fallback_logic():
    registry = IconRegistry()
    # Mock a dense array of icon lookups to cycle the cache
    icon_queries = ["home", "user", "settings", "trash_fallback", "missing_node"] * 30
    
    for query in icon_queries:
        registry.get_icon(query, fallback_style="ascii")

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_icon_resolution", benchmark_icon_fallback_logic)
