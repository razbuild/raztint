import pyperf
from raztint.render import Renderer # Assumes standard module layout for raztint

def benchmark_ansi_truecolor_pipeline():
    # Simulate a dense color string processing matrix
    renderer = Renderer()
    sample_text = "MatrixRenderingTest" * 10
    
    # Run transformations across ANSI, RGB, and TrueColor maps
    for _ in range(50):
        renderer.to_ansi(sample_text, color=(255, 128, 0))
        renderer.to_truecolor(sample_text, color=(12, 34, 56))

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_rendering_pipeline", benchmark_ansi_truecolor_pipeline)
