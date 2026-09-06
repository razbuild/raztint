from importlib.metadata import version

from .core import RazTint, TransientLine
from .data import (
    INTENTS,
    BackgroundColorName,
    ColorName,
    IconMode,
    IconName,
    IntentConfig,
    IntentName,
    StyleName,
)
from .security import DEFAULT_RULES, MaskRule, redact

__version__ = version("raztint")

tint = RazTint()

ok = tint.ok
err = tint.err
warn = tint.warn
info = tint.info
pending = tint.pending
debug = tint.debug
paint = tint.format_text
intents = tint.intents
transient = tint.transient
case = tint.case

__all__ = [
    "RazTint",
    "TransientLine",
    "tint",
    "ok",
    "err",
    "warn",
    "info",
    "pending",
    "debug",
    "paint",
    "redact",
    "MaskRule",
    "DEFAULT_RULES",
    "INTENTS",
    "IntentConfig",
    "ColorName",
    "BackgroundColorName",
    "StyleName",
    "IconName",
    "IconMode",
    "IntentName",
    "intents",
    "case",
    "__version__",
]
