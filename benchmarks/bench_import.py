import importlib
import sys

import pyperf


def benchmark_import_time():
    for name in list(sys.modules):
        if name == "raztint" or name.startswith("raztint."):
            del sys.modules[name]
    importlib.import_module("raztint")


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_package_import", benchmark_import_time)
