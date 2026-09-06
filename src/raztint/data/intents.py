from typing import NamedTuple

from .types import ColorName, IconName, StyleName


class IntentConfig(NamedTuple):
    color: ColorName
    icon: IconName | None
    styles: StyleName | list[StyleName] | None


INTENTS: dict[str, IntentConfig] = {
    "success": IntentConfig(color="green", icon="ok", styles="bold"),
    "error": IntentConfig(color="red", icon="err", styles="bold"),
    "warning": IntentConfig(color="yellow", icon="warn", styles=None),
    "pending": IntentConfig(color="cyan", icon="pending", styles="italic"),
    "debug": IntentConfig(color="white", icon="debug", styles="dim"),
    "info": IntentConfig(color="blue", icon="info", styles=None),
}


def _get_intents(
    name: str | None = None,
) -> dict[str, object] | dict[str, dict[str, object]]:
    if name is not None:
        name = name.lower()
        config = INTENTS.get(name)

        if config is None:
            raise ValueError(
                f"Unknown intent: {name!r}. Valid intents: {', '.join(sorted(INTENTS))}"
            )

        return {
            "color": config.color,
            "icon": config.icon,
            "styles": (
                [config.styles]
                if isinstance(config.styles, str)
                else list(config.styles or [])
            ),
        }

    return {
        name: {
            "color": config.color,
            "icon": config.icon,
            "styles": (
                [config.styles]
                if isinstance(config.styles, str)
                else list(config.styles or [])
            ),
        }
        for name, config in INTENTS.items()
    }
