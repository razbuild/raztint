# API Reference 📚

[Documentation home](index.md)

## 🎨 `paint()` / `format_text()`

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
| `color` | `ColorValue \| None` | Foreground color: named string, hex string, RGB tuple, or ANSI/256-color integer. |
| `bg` | `ColorValue \| None` | Background color: named string, hex string, RGB tuple, or ANSI/256-color integer. |
| `styles` | `StyleName \| list[StyleName] \| None` | Style name or list. |
| `reset` | `bool` | Full reset after text. `False` emits style-specific resets only. |
| `icon` | `IconArg` | Icon key: `"ok"`, `"err"`, `"warn"`, `"info"`, `"pending"`, `"debug"`. Uses `UNSET` sentinel to inherit from intent. |
| `icon_mode` | `IconMode \| None` | `"auto"`, `"nerd"`, `"std"`, or `"ascii"`. `None` uses instance default. |
| `redact` | `bool` | Mask sensitive data before formatting. |
| `redact_rules` | `list[MaskRule] \| None` | Custom rules (defaults to `DEFAULT_RULES`). |
| `intent` | `IntentName \| None` | Semantic preset; fills unset `color`, `icon`, `styles`. |

**Returns:** A formatted string with ANSI codes when color is enabled. When color is disabled, it returns unstyled text and still includes an icon prefix when requested.

**Raises:** `ValueError` for invalid names or color values, and `TypeError` for unsupported argument types.

### Color values

`ColorValue` (`str | int | tuple[int, int, int]`) is inferred by Python type:

| Type | Format | Example |
|---|---|---|
| `str` starting with `#` | Hex RGB | `"#ff7800"` |
| `str` (other) | Named color | `"red"` |
| `int` for `color`: 30-37 or 90-97 | Standard ANSI foreground code | `31` |
| `int` for `bg`: 40-47 or 100-107 | Standard ANSI background code | `41` |
| Other `int` values from 0 to 255 | 256-color palette index | `208` |
| `tuple[int, int, int]` | TrueColor RGB | `(255, 120, 0)` |

The `bg` parameter accepts named colors with or without a `bg_` prefix.

### `icon_mode` values

| Value | Behavior |
|---|---|
| `None` | Uses instance default (`tint.icon_mode`) |
| `"auto"` | Uses Nerd Font, standard Unicode, or ASCII according to available support at call time |
| `"nerd"` | Uses a Nerd Font icon when defined, otherwise standard Unicode, then ASCII |
| `"std"` | Uses a standard Unicode icon when defined, otherwise ASCII |
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

## 🔤 Icon functions

| Function | Meaning |
|---|---|
| `ok()` | Success |
| `err()` | Error |
| `warn()` | Warning |
| `info()` | Information |
| `pending()` | In-progress / waiting |
| `debug()` | Diagnostic output |

For icon modes and fallback behavior, see [Icons and Detection](icons-and-detection.md).

## 🔀 `case()`

Render text based on a value and a semantic intent.

```python
case(
    value,
    cases: Mapping[Hashable, tuple[str, IntentName]],
) -> str
```

Each mapping entry contains the text to render and the semantic intent to apply.

```python
from raztint import case

status = "done"

print(case(
    status,
    {
        "done": ("Done", "success"),
        "pending": ("Pending", "warning"),
        "failed": ("Failed", "error"),
    },
))
```

The selected intent provides the corresponding color, icon, and style.

If `value` is not defined in `cases`, `case()` raises `ValueError`.

```python
case(
    "unknown",
    {
        "done": ("Done", "success"),
    },
)
# ValueError: No case defined for 'unknown'
```

## ⏳ `transient()`

Create temporary terminal output that can be updated or erased.

```python
transient(text: str) -> TransientLine
```

Use it as a context manager when the output should remain visible only while an operation is running.

```python
from raztint import tint

with tint.transient("Working..."):
    do_work()

print("Done!")
```

The transient line is automatically erased when the context exits, including when an exception occurs.

For manual control, use `update()` and `erase()`:

```python
line = tint.transient("Connecting...")

line.update("Connected")
line.erase()
```

Transient output is active only when the target stream is a TTY. On redirected or piped output, it performs no terminal control operations.

## 🔒 `redact()`

```python
redact(
    text: str,
    rules: tuple[MaskRule, ...] | list[MaskRule] | None = None,
) -> str
```

When `rules` is `None`, `DEFAULT_RULES` are applied. See [Security and Redaction](redaction.md).

## 🧩 `RazTint` class

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
| `preview()` | Inspect the current terminal environment and `RazTint` configuration |

Icon helpers (`ok`, `err`, `warn`, `info`, `pending`, `debug`) are available on every instance.

```python
t = RazTint()
t.set_color(False)
print(t.format_text("Plain text", color="red"))
```

### `preview()`

```python
from raztint import tint

print(tint.preview())
```

Example output:

```text
RazTint
────────────────────
Platform    linux
Terminal    xterm-256color
Encoding    utf-8
Color       enabled
Icon mode   auto
```

The output reflects the current instance state.

| Attribute | Type | Description |
|---|---|---|
| `use_color` | `bool` | Whether ANSI output is enabled |
| `icon_mode` | `IconMode` | Detected default icon mode |
| `colors` | `dict[str, str]` | Foreground name -> ANSI code |
| `backgrounds` | `dict[str, str]` | Background name -> ANSI code |
| `styles` | `dict[str, tuple[str, str]]` | Style name -> (on, off) codes |
| `icons` | `dict[str, dict[str, str]]` | Icon registry |

## 🏷️ Typed literals

| Type | Values |
|---|---|
| `ColorName` | `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `gray`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white` |
| `BackgroundColorName` | Same as `ColorName` |
| `StyleName` | `bold`, `dim`, `italic`, `underline`, `strikethrough` |
| `IconName` | `ok`, `err`, `warn`, `info`, `pending`, `debug` |
| `IconMode` | `auto`, `nerd`, `std`, `ascii` |
| `IntentName` | `success`, `error`, `warning`, `pending`, `debug`, `info` |
