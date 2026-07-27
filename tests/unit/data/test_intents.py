from raztint.data.intents import INTENTS, IntentConfig


def test_intents_registry_keys() -> None:
    assert set(INTENTS) == {
        "success",
        "error",
        "warning",
        "pending",
        "debug",
        "info",
    }


def test_intent_config_shape() -> None:
    cfg = INTENTS["success"]
    assert isinstance(cfg, IntentConfig)
    assert cfg.color == "green"
    assert cfg.icon == "ok"
    assert cfg.styles == "bold"
