import importlib
import pyperf

def benchmark_import_time():
    # Force a fresh reload of the module to measure real import overhead
    if "raztint" in __import__("sys").modules:
        del __import__("sys").modules["raztint"]
    importlib.import_module("raztint")

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_package_import", benchmark_import_time)
