import pyperf
from raztint.intents import IntentResolver # Assumes standard module layout

def benchmark_semantic_intent_resolution():
    resolver = IntentResolver()
    # Populate a complex simulation pattern matrix of intents
    intents = ["info", "warning", "error", "success", "critical"] * 20
    
    for intent in intents:
        resolver.resolve(intent)

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_intent_resolution", benchmark_semantic_intent_resolution)
