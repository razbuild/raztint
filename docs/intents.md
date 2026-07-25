# Intents

[← Documentation index](index.md)

Intents are semantic presets that map a message category to a default color, icon, and style. They reduce repetitive `paint()` calls for common CLI output patterns.

---

## Built-in intents

Defined in `raztint.data.intents.INTENTS`:

| Intent | Color | Icon | Styles | Typical use |
|---|---|---|---|---|
| `success` | green | ok | bold | Completed operations |
| `danger` | red | err | bold | Errors and failures |
| `warning` | yellow | warn | — | Caution messages |
| `info` | blue | info | — | Informational notes |
| `pending` | cyan | pending | italic | In-progress / waiting states |
| `debug` | white | debug | dim | Verbose or diagnostic output |

---

## Usage

Pass `intent` to `paint()` or `format_text()`:

```python
from raztint import paint

print(paint("File saved.", intent="success"))
print(paint("Connection refused.", intent="danger"))
print(paint("Disk space low.", intent="warning"))
print(paint("Starting worker...", intent="pending"))
print(paint("cache hit ratio=0.92", intent="debug"))
print(paint("Version 2.1.0", intent="info"))
```

---

## Override behavior

Explicit parameters take precedence over intent defaults. Unset parameters inherit from the intent:

```python
from raztint import paint

# Uses success defaults: green + ok + bold
print(paint("Done.", intent="success"))

# Keeps success color and icon, but adds underline instead of bold
print(paint("Done.", intent="success", styles="underline"))

# Keeps success color/style, but no icon
print(paint("Done.", intent="success", icon=None))
```

The `icon` parameter uses a sentinel default (`UNSET`) internally so that `icon=None` explicitly suppresses an icon while omitting `icon` inherits the intent's icon.

---

## Inspecting the registry

```python
from raztint import INTENTS, IntentConfig

cfg: IntentConfig = INTENTS["success"]
print(cfg.color)   # "green"
print(cfg.icon)    # "ok"
print(cfg.styles)  # "bold"
```

`IntentConfig` is a `NamedTuple` with fields `color`, `icon`, and `styles`.

---

## Error handling

An unknown intent raises `ValueError`:

```python
from raztint import paint

paint("x", intent="not_an_intent")  # ValueError: Unknown intent: 'not_an_intent'
```

Valid names are listed in the error message and match `IntentName` in `raztint.data.types`.

---

## See also

- [Getting Started Intents](getting-started.md#intents)
- [API Reference `paint()`](api-reference.md#paint--format_text)
