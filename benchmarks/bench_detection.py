import pyperf

from raztint.detect.env import get_icon_mode, supports_color


def benchmark_environment_capability_detection():
    # Cycle capability detection checks rapidly
    for _ in range(100):
        supports_color()
        get_icon_mode()


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func(
        "raztint_environment_detection", benchmark_environment_capability_detection
    )
