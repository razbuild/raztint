# Getting Started

[← Documentation index](index.md)

## `paint()` parameters

`paint()` is the unified styling function - an alias for `tint.format_text()`. Color values are inferred by their Python type:

| Python type | Color format | Example |
|---|---|---|
| `str` starting with `#` | Hex RGB | `"#ff7800"` |
| `str` (other) | Named color | `"red"`, `"green"`, `"bright_blue"` |
| `int` in 30-37 or 90-97 | Standard ANSI foreground code | `31` |
| `int` in 40-47 or 100-107 | Standard ANSI background code | `41` |
| `int` (other, 0-255) | 256-color palette index | `208` |
| `tuple[int, int, int]` | 24-bit TrueColor RGB | `(255, 120, 0)` |

```python
from raztint import paint

# Named colors
print(paint("Done!", color="green", styles="bold"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))

# 256-color palette
print(paint("Orange", color=208))
print(paint("Background gray", bg=236))

# TrueColor RGB
print(paint("Orange", color=(255, 120, 0)))
print(paint("Dark bg", bg=(30, 30, 30)))

# Hex colors
print(paint("Orange", color="#ff7800"))
print(paint("Dark bg", bg="#1e1e1e"))

# Combined with icon
print(paint("File saved.", color="green", styles="bold", icon="ok"))
print(paint("Connection failed.", color="red", icon="err"))

# Override icon mode per call
print(paint("Done!", color="green", icon="ok", icon_mode="nerd"))
print(paint("Done!", color="green", icon="ok", icon_mode="ascii"))
```

### Concatenation with `reset=False`

Disable the trailing reset on intermediate parts when chaining styled segments:

```python
part1 = paint("WARNING:", color="yellow", reset=False)
part2 = paint(" Disk full", color="red")
print(part1 + part2)
```

## The `tint` singleton

`tint` is a pre-instantiated `RazTint` for convenience:

```python
from raztint import tint

print(tint.format_text("text", color="red"))
print(tint.ok(), "hello")
print(tint.use_color)   # True if ANSI output is enabled
print(tint.icon_mode)   # "nerd", "std", or "ascii"
```

## Class-based usage

Create your own instance for isolated settings:

```python
from raztint import RazTint

t = RazTint()
t.set_color(False)
print(t.format_text("Plain text", color="blue"))
```

Each instance has its own `use_color` and `icon_mode`.

## Icon helpers

Six status icons auto-adapt to the terminal:

```python
from raztint import ok, err, warn, info, pending, debug

print(f"{ok()} File saved.")
print(f"{err()} Connection failed.")
print(f"{warn()} Disk space low.")
print(f"{info()} Analysis in progress.")
print(f"{pending()} Waiting for response...")
print(f"{debug()} Cache hit ratio=0.92")
```

## Intents

Semantic presets that set color, icon, and style together:

```python
from raztint import paint

print(paint("Saved.", intent="success"))
print(paint("Invalid input.", intent="danger"))
print(paint("Waiting for worker...", intent="pending"))
```

Explicit `color`, `icon`, or `styles` override the intent defaults. See [Intents](intents.md).

## Redaction

```python
from raztint import paint, redact

# Standalone
safe = redact("password=supersecret")

# Combined with formatting
print(paint("token=ghp_secret", intent="debug", redact=True))
```

See [Security & Redaction](redaction.md).

## Next steps

- [API Reference](api-reference.md) - full parameter lists and type aliases
- [Configuration](configuration.md) - environment variables for CI and overrides
- [Icons & Detection](icons-and-detection.md) - how icon modes are chosen