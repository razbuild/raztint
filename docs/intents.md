# Intents

[← Documentation index](index.md)

Intents are semantic presets that map a message category to a color, icon, and style. They reduce repetitive `paint()` calls for common CLI output patterns.

> **Breaking change (v0.9.0):** The `danger` intent was renamed to `error`. Replace all `intent="danger"` usages with `intent="error"`.

## Built-in intents

| Intent | Color | Icon | Styles | Typical use |
|---|---|---|---|---|
| `success` | green | ok | bold | Completed operations |
| `error` | red | err | bold | Errors and failures |
| `warning` | yellow | warn | — | Caution messages |
| `info` | blue | info | — | Informational notes |
| `pending` | cyan | pending | italic | In-progress / waiting |
| `debug` | white | debug | dim | Verbose / diagnostic |

## Usage

```python
from raztint import paint

print(paint("File saved.", intent="success"))
print(paint("Connection refused.", intent="error"))
print(paint("Disk space low.", intent="warning"))
print(paint("Starting worker...", intent="pending"))
print(paint("cache hit ratio=0.92", intent="debug"))
print(paint("Version 2.1.0", intent="info"))
```

### Migration

```python
# Before (<= 0.8.x)
paint("Connection refused.", intent="danger")

# After (>= 0.9.0)
paint("Connection refused.", intent="error")
```

## Override behavior

Explicit parameters take precedence over intent defaults. Unset parameters inherit from the intent:

```python
# Uses success defaults: green + ok + bold
print(paint("Done.", intent="success"))

# Keeps success color and icon, overrides style
print(paint("Done.", intent="success", styles="underline"))

# Keeps success color/style, suppresses icon
print(paint("Done.", intent="success", icon=None))
```

The `icon` parameter uses a sentinel default (`UNSET`) so `icon=None` explicitly suppresses the icon while omitting `icon` inherits the intent's icon.

## Inspecting the registry

```python
from raztint import INTENTS, IntentConfig

cfg: IntentConfig = INTENTS["success"]
print(cfg.color)   # "green"
print(cfg.icon)    # "ok"
print(cfg.styles)  # "bold"
```

`IntentConfig` is a `NamedTuple` with fields `color`, `icon`, and `styles`.

## Error handling

An unknown intent raises `ValueError`:

```python
paint("x", intent="not_an_intent")  # ValueError
```

Valid names are listed in the error message and match the `IntentName` literal type.