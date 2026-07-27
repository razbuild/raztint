# API Reference

[← Documentation index](index.md)

---

## `paint()` / `format_text()`

`paint` is a module-level alias for `tint.format_text()`. Both accept identical parameters.

```python
paint(
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
) -> str
```

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Text to format. |
| `color` | `ColorValue \| None` | Foreground color: named string, hex string, RGB tuple, or ANSI-256 integer. |
| `bg` | `ColorValue \| None` | Background color (same types as `color`). |
| `styles` | `StyleName \| list[StyleName] \| None` | Style name or list. |
| `reset` | `bool` | Full reset after text. `False` emits style-specific resets only. |
| `icon` | `IconArg` | Icon key: `"ok"`, `"err"`, `"warn"`, `"info"`, `"pending"`, `"debug"`. Uses `UNSET` sentinel to inherit from intent. |
| `icon_mode` | `IconMode \| None` | `"auto"`, `"nerd"`, `"std"`, or `"ascii"`. `None` uses instance default. |
| `redact` | `bool` | Mask sensitive data before formatting. |
| `redact_rules` | `list[MaskRule] \| None` | Custom rules (defaults to `DEFAULT_RULES`). |
| `intent` | `IntentName \| None` | Semantic preset; fills unset `color`, `icon`, `styles`. |

**Returns:** Formatted string with ANSI codes when color is enabled. When disabled, returns plain text (icon prefix still included).

**Raises:** `ValueError` for unknown names; `TypeError` for invalid `styles` type.

### Color values

`ColorValue` (`str | int | tuple[int, int, int]`) is inferred by Python type:

| Type | Format | Example |
|---|---|---|
| `str` starting with `#` | Hex RGB | `"#ff7800"` |
| `str` (other) | Named color | `"red"` |
| `int` 30-37, 90-97 | Standard ANSI fg | `31` |
| `int` 40-47, 100-107 | Standard ANSI bg | `41` |
| `int` (0-255) | 256-color index | `208` |
| `tuple[int, int, int]` | TrueColor RGB | `(255, 120, 0)` |

The `bg` parameter also accepts named colors without a `bg_` prefix.

### `icon_mode` values

| Value | Behavior |
|---|---|
| `None` | Uses instance default (`tint.icon_mode`) |
| `"auto"` | Cascades: Nerd → Unicode → ASCII at call time |
| `"nerd"` | Nerd Font icon; falls back to `std` then `ascii` |
| `"std"` | Unicode icon; falls back to `ascii` |
| `"ascii"` | Always ASCII |

### Examples

```python
from raztint import paint

# Named colors
print(paint("Success", color="green"))
print(paint("Error", color="red", styles="bold"))

# 256-color, TrueColor, hex
print(paint("Orange", color=208))
print(paint("Orange", color=(255, 120, 0)))
print(paint("Orange", color="#ff7800"))

# Background
print(paint("Alert", color="white", bg="red"))
print(paint("Dark bg", bg=(30, 30, 30)))
print(paint("Dark bg", bg="#1e1e1e"))

# Combined
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))
print(paint("File saved.", color="green", styles="bold", icon="ok"))

# Intents
print(paint("Done!", intent="success"))
print(paint("Failed", intent="error"))

# Redaction
print(paint("token=ghp_XXXXXXXX", intent="debug", redact=True))
```

---

## Icon functions

| Function | Meaning |
|---|---|
| `ok()` | Success |
| `err()` | Error |
| `warn()` | Warning |
| `info()` | Information |
| `pending()` | In-progress / waiting |
| `debug()` | Diagnostic output |

Fallback order: Nerd Font -> Unicode -> ASCII. See [Icons & Detection](icons-and-detection.md).

---

## `redact()`

```python
redact(
    text: str,
    rules: tuple[MaskRule, ...] | list[MaskRule] | None = None,
) -> str
```

When `rules` is `None`, `DEFAULT_RULES` are applied. See [Security & Redaction](redaction.md).

---

## `RazTint` class

```python
from raztint import RazTint

t = RazTint()
```

| Method | Description |
|---|---|
| `color(text, fg_code)` | Apply raw ANSI foreground code |
| `background(text, bg_code)` | Apply raw ANSI background code |
| `style(text, on_code, off_code)` | Apply raw style on/off codes |
| `format_text(...)` | Same as `paint()` |
| `set_color(enabled)` | Enable or disable color |

Icon helpers (`ok`, `err`, `warn`, `info`, `pending`, `debug`) are available on every instance.

```python
t = RazTint()
t.set_color(False)
print(t.format_text("Plain text", color="red"))
```

| Attribute | Type | Description |
|---|---|---|
| `use_color` | `bool` | Whether ANSI output is enabled |
| `icon_mode` | `IconMode` | Detected default icon mode |
| `colors` | `dict[str, str]` | Foreground name -> ANSI code |
| `backgrounds` | `dict[str, str]` | Background name -> ANSI code |
| `styles` | `dict[str, tuple[str, str]]` | Style name -> (on, off) codes |
| `icons` | `dict[str, dict[str, str]]` | Icon registry |

---

## Typed literals

| Type | Values |
|---|---|
| `ColorName` | `black`, `red`, `green`, `blue`, `magenta`, `cyan`, `white`, `gray`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white` |
| `BackgroundColorName` | Same as `ColorName` |
| `StyleName` | `bold`, `dim`, `italic`, `underline`, `strikethrough` |
| `IconName` | `ok`, `err`, `warn`, `info`, `pending`, `debug` |
| `IconMode` | `auto`, `nerd`, `std`, `ascii` |
| `IntentName` | `success`, `error`, `warning`, `pending`, `debug`, `info` |