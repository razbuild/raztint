# Intents ✨

[Documentation home](index.md)

Intents are semantic presets for common command-line messages. Each preset supplies a color, icon, and optional style, so callers describe what the message means instead of repeating presentation details.

## 🎨 Built-in intents

| Intent | Color | Icon | Style | Typical use |
|---|---|---|---|---|
| `success` | `green` | `ok` | `bold` | Completed operations |
| `error` | `red` | `err` | `bold` | Errors and failures |
| `warning` | `yellow` | `warn` | None | Caution messages |
| `info` | `blue` | `info` | None | Informational messages |
| `pending` | `cyan` | `pending` | `italic` | Work in progress |
| `debug` | `white` | `debug` | `dim` | Diagnostic output |

## 🔍 Inspect intents

Use `intents()` to inspect the available semantic intents and their presentation defaults.

```python
from raztint import intents

print(intents("success"))
```

Output:

```text
{'color': 'green', 'icon': 'ok', 'styles': ['bold']}
```

To inspect all available intents:

```python
print(intents())
```

Output:

```text
{
    'success': {'color': 'green', 'icon': 'ok', 'styles': ['bold']},
    'error': {'color': 'red', 'icon': 'err', 'styles': ['bold']},
    'warning': {'color': 'yellow', 'icon': 'warn', 'styles': []},
    'pending': {'color': 'cyan', 'icon': 'pending', 'styles': ['italic']},
    'debug': {'color': 'white', 'icon': 'debug', 'styles': ['dim']},
    'info': {'color': 'blue', 'icon': 'info', 'styles': []},
}
```

The returned `styles` value is always a list. An unknown intent raises `ValueError`.

## 🖌️ Use an intent

```python
from raztint import paint

print(paint("File saved.", intent="success"))
print(paint("Connection refused.", intent="error"))
print(paint("Disk space is low.", intent="warning"))
print(paint("Starting worker...", intent="pending"))
```

## 🔧 Override a preset

Explicit `color`, `icon`, and `styles` arguments override the corresponding intent defaults. Arguments you don't provide continue to use the preset.

```python
# Uses the success preset: green, ok icon, and bold.
print(paint("Done.", intent="success"))

# Keeps the success color and icon, but changes the style.
print(paint("Done.", intent="success", styles="underline"))

# Keeps the success color and style, but removes the icon.
print(paint("Done.", intent="success", icon=None))
```

`icon` normally uses an internal unset value. Omitting it inherits the intent icon; passing `None` intentionally suppresses that icon.

## ⬆️ Upgrading from 0.8 and earlier

In RazTint 0.9, `danger` was renamed to `error`.

```python
# Before
paint("Connection refused.", intent="danger")

# After
paint("Connection refused.", intent="error")
```
