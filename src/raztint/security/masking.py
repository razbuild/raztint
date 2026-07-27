import re
from typing import NamedTuple


class MaskRule(NamedTuple):
    pattern: str
    name: str
    replacement: str


DEFAULT_RULES: tuple[MaskRule, ...] = (
    MaskRule(r"(ghp|gho|ghu|ghs|ghr)_\S+", "github_token", r"\1_****"),
    MaskRule(r"sk-[A-Za-z0-9]{48}", "openai_key", "sk-****"),
    MaskRule(r"xox[baprs]-[A-Za-z0-9\-]+", "slack_token", "xox*-****"),
    MaskRule(
        r"eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+",
        "jwt",
        "[JWT:REDACTED]",
    ),
    MaskRule(
        r"(?i)(Bearer\s+)[A-Za-z0-9\-_\.]+",
        "bearer_token",
        r"\1[REDACTED]",
    ),
    MaskRule(r"(://[^:]+:)([^@]+)(@)", "url_credentials", r"\1****\3"),
    MaskRule(
        r"\b(\d{4})[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?(\d{4})\b",
        "credit_card",
        r"\1-****-****-\2",
    ),
    MaskRule(
        r"(?i)((?:password|passwd|secret|api_?key|token)\s*[=:]\s*)(?!\S*\*{4})(\S+)",
        "generic_secret",
        r"\1****",
    ),
)

_COMPILED_DEFAULT: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(rule.pattern), rule.replacement) for rule in DEFAULT_RULES
)
_PATTERN_CACHE: dict[str, re.Pattern[str]] = {
    rule.pattern: compiled
    for rule, (compiled, _) in zip(DEFAULT_RULES, _COMPILED_DEFAULT, strict=True)
}


def _compile(pattern: str) -> re.Pattern[str]:
    try:
        return _PATTERN_CACHE[pattern]
    except KeyError:
        compiled = re.compile(pattern)
        _PATTERN_CACHE[pattern] = compiled
        return compiled


def redact(
    text: str, rules: tuple[MaskRule, ...] | list[MaskRule] | None = None
) -> str:
    if rules is None:
        compiled_rules = _COMPILED_DEFAULT
    else:
        compiled_rules = tuple(
            (_compile(rule.pattern), rule.replacement) for rule in rules
        )
    result = text
    for pattern, replacement in compiled_rules:
        result = pattern.sub(replacement, result)
    return result
