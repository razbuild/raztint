# RazTint Performance Benchmark Suite

This directory contains a modular benchmark suite powered by `pyperf` to measure performance and detect regressions.

## Requirements

Install `pyperf`:

```bash
pip install pyperf
```

## Run a Benchmark

Run an individual benchmark:

```bash
python benchmarks/bench_import.py
```

Other available benchmarks:

- `bench_detection.py`
- `bench_icons.py`
- `bench_import.py`
- `bench_intents.py`
- `bench_rendering.py`
- `bench_security.py`

## Save Results

Store benchmark results for later analysis:

```bash
python benchmarks/bench_import.py -o import.json
```

## Compare Results

Compare two benchmark runs:

```bash
python -m pyperf compare_to old.json new.json
```

## Stable Measurements (Linux)

For more reproducible results on Linux:

```bash
sudo python -m pyperf system tune
python benchmarks/bench_import.py --rigorous
```

Restore the original system configuration when finished:

```bash
sudo python -m pyperf system reset
```

> **Note**
> Small timing variations are expected, especially on laptops and shared systems. Compare results from the same machine under similar conditions.