# Security and Redaction

[Documentation home](index.md)

RazTint includes a lightweight regex-based redaction layer for masking secrets before they appear in terminal output or logs.

## `redact()`

```python
from raztint import redact

safe = redact("password=supersecret api_key=ghp_abc123xyz")
```

When `rules` is `None`, `DEFAULT_RULES` are applied. Rules run in order; each pattern is compiled once and cached.

## Built-in rules

| Rule name | Pattern (summary) | Replacement |
|---|---|---|
| `github_token` | GitHub token prefixes, including `ghp_` and `gho_` | Original prefix followed by `****` |
| `openai_key` | OpenAI `sk-` keys (48 chars) | `sk-****` |
| `slack_token` | Slack `xox*` tokens | `xox*-****` |
| `jwt` | JSON Web Tokens | `[JWT:REDACTED]` |
| `bearer_token` | `Bearer <token>` headers | `Bearer [REDACTED]` |
| `url_credentials` | Credentials in URLs (`user:pass@`) | `user:****@` |
| `credit_card` | 16-digit card numbers | `4111-****-****-1111` |
| `generic_secret` | `password=`, `secret=`, `api_key=`, and similar assignments | Value replaced with `****` |

```python
from raztint import DEFAULT_RULES

for rule in DEFAULT_RULES:
    print(rule.name, rule.pattern)
```

## Custom rules

Define your own with `MaskRule`:

```python
from raztint import MaskRule, redact

rules = [
    MaskRule(r"SECRET-\d+", "custom", "SECRET-***"),
    MaskRule(r"myapp_[A-Za-z0-9]{32}", "app_token", "myapp_****"),
]

safe = redact("SECRET-12345 deployed", rules=rules)
```

| Field | Description |
|---|---|
| `pattern` | Regex string (supports groups in `replacement`) |
| `name` | Identifier for debugging |
| `replacement` | Substitution string (may use `\1`, `\2`, and similar group references) |

## Redaction in `paint()`

```python
from raztint import paint

raw = "Connected as user:pass@db.internal token=ghp_secret"
print(paint(raw, intent="debug", redact=True))

# Custom rules
from raztint import MaskRule

rules = [MaskRule(r"INTERNAL-\w+", "internal", "INTERNAL-***")]
print(paint("key=INTERNAL-abc", redact=True, redact_rules=rules))
```

Redaction runs **before** ANSI formatting, so masked output never exposes the original secret in the styled string.

## Limitations

- Regex redaction is best-effort, not a security guarantee. Review patterns for your threat model.
- Already-masked values (e.g. `****`) are not double-processed.
- For structured logging pipelines, consider redacting at the logging layer as well.
