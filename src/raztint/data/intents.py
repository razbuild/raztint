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
