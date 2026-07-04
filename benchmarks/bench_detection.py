import pyperf
from raztint.env import EnvironmentDetector

def benchmark_environment_capability_detection():
    detector = EnvironmentDetector()
    # Cycle capability detection checks rapidly
    for _ in range(100):
        detector.detect_color_support()
        detector.get_terminal_dimensions()

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_environment_detection", benchmark_environment_capability_detection)
