import pyperf

from raztint.data.intents import INTENTS


def benchmark_semantic_intent_resolution():
    # Populate a complex simulation pattern matrix of intents
    # Note: only keys that actually exist in INTENTS are used
    # ("error" -> "danger", "critical" has no equivalent and was dropped)
    intents = ["info", "warning", "danger", "success", "pending"] * 20
    for intent in intents:
        INTENTS[intent]


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_intent_resolution", benchmark_semantic_intent_resolution)
