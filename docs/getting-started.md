# Getting Started

[← Documentation index](https://github.com/razbuild/raztint/blob/master/docs/index.md)

You can use RazTint in three ways: call `paint()` for formatting, import status icon helpers, or create a `RazTint` instance for scoped control.

---

## Functional usage

You can use RazTint in three ways: call `paint()` for formatting, import status icon helpers, or create a `RazTint` instance for scoped control.

```python
from raztint import err, info, ok, paint, warn, pending, debug

print(paint("Success! The operation completed.", color="green"))
print(paint("Critical Error: Database not found.", color="red"))
print(paint("This is bold text.", styles="bold"))
print(paint("Underlined red text.", color="red", styles="underline"))
print(paint("Red text on a blue background.", color="red", bg="blue"))

# Icons (auto-adapts to Nerd Font / Unicode / ASCII)
print(f"{ok()} File saved successfully.")
print(f"{err()} Connection failed.")
print(f"{info()} Analysis in progress...")
print(f"{warn()} Disk space low.")
print(f"{pending()} Waiting for response...")
print(f"{debug()} Cache hit ratio=0.92")
```

---

## Using `paint()`

`paint()` combines color, background, styles, and an icon in a single call. It is an alias for `tint.format_text()`.

```python
from raztint import paint

# Color + style
print(paint("Done!", color="green", styles="bold"))

# Color + background + multiple styles
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))

# With icon (uses environment-detected mode)
print(paint("File saved.", color="green", styles="bold", icon="ok"))
print(paint("Connection failed.", color="red", icon="err"))

# Override icon mode explicitly
print(paint("Done!", color="green", icon="ok", icon_mode="nerd"))
print(paint("Done!", color="green", icon="ok", icon_mode="std"))
print(paint("Done!", color="green", icon="ok", icon_mode="ascii"))
print(paint("Done!", color="green", icon="ok", icon_mode="auto"))
```

### Combining formatting

```python
from raztint import paint

print(paint("Important message", color="red", styles=["bold", "underline"]))
print(paint("Important message", color="red", styles=["bold", "underline"], icon="err"))
```

### Concatenation with `reset=False`

When chaining styled segments, disable the trailing reset on intermediate parts:

```python
from raztint import paint

part1 = paint("WARNING:", color="yellow", reset=False)
part2 = paint(" Disk full", color="red")
print(part1 + part2)
```

---

## The `tint` singleton

`tint` is a pre-instantiated `RazTint` for convenience:

```python
from raztint import tint

print(tint.format_text("text", color="red"))
print(tint.ok(), "hello")
print(tint.format_text("Done!", color="green", icon="ok"))
```

Inspect runtime state:

```python
print(tint.use_color)   # True if ANSI output is enabled
print(tint.icon_mode)   # "nerd", "std", or "ascii"
```

---

## Class-based usage

Create your own instance when you need isolated or dynamic settings:

```python
from raztint import RazTint

t = RazTint()
t.set_color(False)
print(t.format_text("Plain text color disabled for this instance.", color="blue"))
```

Each instance carries its own `use_color` and `icon_mode` state.

---

## Intents

Apply semantic presets with a single parameter. See [Intents](https://github.com/razbuild/raztint/blob/master/docs/intents.md) for the full registry.

```python
from raztint import paint

print(paint("Saved.", intent="success"))
print(paint("Invalid input.", intent="danger"))
print(paint("Waiting for worker...", intent="pending"))
```

Explicit `color`, `icon`, or `styles` arguments override the intent defaults.

---

## Redaction

Mask secrets before they reach the terminal. See [Security & Redaction](https://github.com/razbuild/raztint/blob/master/docs/redaction.md).

```python
from raztint import paint, redact

# Standalone
safe = redact("password=supersecret")

# Combined with formatting
raw = "Connected as user:pass@db.internal token=ghp_secret"
print(paint(raw, intent="debug", redact=True))
```

---

## Next steps

- [API Reference](https://github.com/razbuild/raztint/blob/master/docs/api-reference.md) — full parameter lists and helper tables
- [Configuration](https://github.com/razbuild/raztint/blob/master/docs/configuration.md) — environment variables for CI and overrides
- [Icons & Detection](https://github.com/razbuild/raztint/blob/master/docs/icons-and-detection.md) — how icon modes are chosen