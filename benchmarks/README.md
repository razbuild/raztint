# RazTint Performance Benchmark Suite

This directory contains an internal pyperf-based modular suite to monitor computation efficiency and catch performance regressions.

## Running the Benchmarks

To run an individual benchmark file configuration independently, install `pyperf` and run the script target:

```bash
pip install pyperf
python benchmarks/bench_import.py
