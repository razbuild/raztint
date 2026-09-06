from collections.abc import Callable, Hashable, Mapping
from typing import TypeVar

from .core.instance import RazTint as RazTint
from .core.transient import TransientLine as TransientLine
from .data import INTENTS as INTENTS
from .data import IntentConfig as IntentConfig
from .data.types import BackgroundColorName as BackgroundColorName
from .data.types import ColorName as ColorName
from .data.types import ColorValue as ColorValue
from .data.types import IconMode as IconMode
from .data.types import IconName as IconName
from .data.types import IntentName as IntentName
from .data.types import StyleName as StyleName
from .formatting.paint import UNSET, IconArg
from .security import DEFAULT_RULES as DEFAULT_RULES
from .security import MaskRule as MaskRule

__version__: str

tint: RazTint

T = TypeVar("T", bound=Hashable)
_IconFn = Callable[[], str]

def ok() -> str: ...
def err() -> str: ...
def warn() -> str: ...
def info() -> str: ...
def pending() -> str: ...
def debug() -> str: ...
def transient(text: str) -> TransientLine: ...
def case(
    value: T,
    cases: Mapping[T, tuple[str, IntentName]],
) -> str: ...
def intents(
    name: IntentName | None = None,
) -> dict[str, dict[str, object]]: ...
def redact(
    text: str,
    rules: tuple[MaskRule, ...] | list[MaskRule] | None = None,
) -> str: ...
def paint(
    text: str,
    color: ColorValue | None = None,
    bg: ColorValue | None = None,
    styles: StyleName | list[StyleName] | None = None,
    reset: bool = True,
    icon: IconArg = UNSET,
    icon_mode: IconMode | None = None,
    redact: bool = False,
    redact_rules: list[MaskRule] | None = None,
    intent: IntentName | None = None,
) -> str: ...

__all__: list[str]
