# Intents

[Documentation home](index.md)

Intents are semantic presets for common command-line messages. Each preset supplies a color, icon, and optional style, so callers describe what the message means instead of repeating presentation details.

## Built-in intents

| Intent | Color | Icon | Style | Typical use |
|---|---|---|---|---|
| `success` | `green` | `ok` | `bold` | Completed operations |
| `error` | `red` | `err` | `bold` | Errors and failures |
| `warning` | `yellow` | `warn` | None | Caution messages |
| `info` | `blue` | `info` | None | Informational messages |
| `pending` | `cyan` | `pending` | `italic` | Work in progress |
| `debug` | `white` | `debug` | `dim` | Diagnostic output |

## Use an intent

```python
from raztint import paint

print(paint("File saved.", intent="success"))
print(paint("Connection refused.", intent="error"))
print(paint("Disk space is low.", intent="warning"))
print(paint("Starting worker...", intent="pending"))
```

## Override a preset

Explicit `color`, `icon`, and `styles` arguments override the corresponding intent defaults. Arguments you do not provide continue to use the preset.

```python
# Uses the success preset: green, ok icon, and bold.
print(paint("Done.", intent="success"))

# Keeps the success color and icon, but changes the style.
print(paint("Done.", intent="success", styles="underline"))

# Keeps the success color and style, but removes the icon.
print(paint("Done.", intent="success", icon=None))
```

`icon` normally uses an internal unset value. Omitting it inherits the intent icon; passing `None` intentionally suppresses that icon.

## Inspect the registry

`INTENTS` contains the built-in configurations. `IntentConfig` has `color`, `icon`, and `styles` fields.

```python
from raztint import INTENTS, IntentConfig

config: IntentConfig = INTENTS["success"]
print(config.color)   # green
print(config.icon)    # ok
print(config.styles)  # bold
```

An unknown intent raises `ValueError`. Valid names are listed in the error message and in the `IntentName` type.

## Upgrading from 0.8 and earlier

In RazTint 0.9, `danger` was renamed to `error`.

```python
# Before
paint("Connection refused.", intent="danger")

# After
paint("Connection refused.", intent="error")
```
