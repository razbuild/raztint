import pyperf

from raztint.core.ansi import apply_color, apply_rgb


def benchmark_ansi_truecolor_pipeline():
    # Simulate a dense color string processing matrix
    sample_text = "MatrixRenderingTest" * 10
    # Run transformations across the standard ANSI path and the TrueColor (RGB) path
    for _ in range(50):
        apply_color(sample_text, "33", use_color=True)
        apply_rgb(sample_text, 12, 34, 56, use_color=True)


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_rendering_pipeline", benchmark_ansi_truecolor_pipeline)
