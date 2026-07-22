# API Reference

[← Documentation index](index.md)

---

## `paint()` / `format_text()`

The main entry point for combining colors, backgrounds, styles, icons, intents, and redaction.

`paint` is a module-level alias for `tint.format_text()`. Both accept identical parameters.

**Signature:**

```python
paint(
    text: str,
    color: ColorName | int | None = None,
    bg: BackgroundColorName | int | None = None,
    styles: StyleName | list[StyleName] | None = None,
    reset: bool = True,
    icon: IconName | None = None,
    icon_mode: IconMode | None = None,
    redact: bool = False,
    redact_rules: list[MaskRule] | None = None,
    intent: IntentName | None = None,
) -> str
```

**Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | The text to format. |
| `color` | `ColorName \| int \| None` | Foreground color name (e.g. `"red"`) or ANSI code (e.g. `31`). |
| `bg` | `BackgroundColorName \| int \| None` | Background color name (e.g. `"bg_red"`, `"red"`) or ANSI code (e.g. `41`). |
| `styles` | `StyleName \| list[StyleName] \| None` | Style name or list of style names. |
| `reset` | `bool` | If `True` (default), full reset after text. If `False`, style-specific resets are emitted only when styles are used; otherwise no reset is appended. |
| `icon` | `IconName \| None` | Icon key to prepend: `"ok"`, `"err"`, `"warn"`, `"info"`. |
| `icon_mode` | `IconMode \| None` | Override icon mode: `"auto"`, `"nerd"`, `"std"`, or `"ascii"`. |
| `redact` | `bool` | If `True`, mask sensitive data in `text` before formatting. |
| `redact_rules` | `list[MaskRule] \| None` | Custom redaction rules (defaults to `DEFAULT_RULES`). |
| `intent` | `IntentName \| None` | Semantic preset; fills unset `color`, `icon`, and `styles`. |

**`icon_mode` values:**

| Value | Behavior |
|---|---|
| `None` | Uses `tint.icon_mode` — whatever the environment detected at startup |
| `"auto"` | Cascades: Nerd Font → Unicode → ASCII at call time |
| `"nerd"` | Nerd Font icon; falls back to `std` then `ascii` if unavailable |
| `"std"` | Unicode icon; falls back to `ascii` if unavailable |
| `"ascii"` | Always ASCII |

**Returns:** Formatted string with ANSI codes if color is enabled. When color is disabled, text is returned unchanged unless an icon is requested, in which case the plain icon prefix is still included.

**Raises:**

- `ValueError` — unknown color, background, style, icon, or intent name
- `TypeError` — `styles` is not `str`, `list[str]`, or `None`

**Examples:**

```python
from raztint import paint

print(paint("Success", color="green"))
print(paint("Error", color="red", styles="bold"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))
print(paint("File saved.", color="green", styles="bold", icon="ok"))
print(paint("Done!", color="green", icon="ok", icon_mode="auto"))
print(paint("Saved.", intent="success"))
print(paint(f"token= ghp_XXXXXXXX", intent="debug", redact=True))
```
## Formatting colors, backgrounds, and styles

Use `paint()` for named foreground colors, backgrounds, and styles:

```python
print(paint("Error", color="red"))
print(paint("Alert", color="white", bg="red"))
print(paint("Important", styles=["bold", "underline"]))
```

The old foreground, background, and style convenience helpers were removed so `paint()` is the single source of truth for formatting behavior.

---

## Icon functions

Return status symbols based on environment detection:

| Function | Meaning |
|---|---|
| `ok()` | Success |
| `err()` | Error |
| `warn()` | Warning |
| `info()` | Information |

Fallback order: Nerd Font → Unicode → ASCII. See [Icons & Detection](icons-and-detection.md).

To combine an icon with formatted text in one call, use `paint(..., icon="ok")` instead.

---

## `redact()`

Mask sensitive data using regex rules. See [Security & Redaction](redaction.md).

```python
from raztint import redact, MaskRule

safe = redact("password=secret")
custom = redact("SECRET-123", rules=[MaskRule(r"SECRET-\d+", "custom", "SECRET-***")])
```

---

## `RazTint` class

### Constructor

```python
from raztint import RazTint

t = RazTint()
```

### Methods

| Method | Description |
|---|---|
| `color(text, fg_code)` | Apply a raw ANSI foreground code |
| `background(text, bg_code)` | Apply a raw ANSI background code |
| `style(text, on_code, off_code)` | Apply a raw style on/off pair |
| `format_text(...)` | Same as `paint()` |
| `set_color(enabled)` | Enable or disable color output |

Status icon helpers (`ok`, `err`, `warn`, `info`, `pending`, `debug`) are available on the instance. Use `format_text()` for colors, backgrounds, and styles.

**Example:**

```python
from raztint import RazTint

t = RazTint()
colored = t.color("Hello", "31")  # red via raw code
t.set_color(False)
print(t.format_text("Plain text", color="red"))
```

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `use_color` | `bool` | Whether ANSI output is enabled |
| `icon_mode` | `IconMode` | Detected default icon mode: `"nerd"`, `"std"`, or `"ascii"` |
| `colors` | `dict[str, str]` | Foreground color name → ANSI code |
| `backgrounds` | `dict[str, str]` | Background color name → ANSI code |
| `styles` | `dict[str, tuple[str, str]]` | Style name → (on, off) codes |
| `icons` | `dict[str, dict[str, str]]` | Icon registry |

---

## Typed literals

RazTint exports `Literal` type aliases for IDE autocompletion:

| Type | Values |
|---|---|
| `ColorName` | `black`, `red`, `green`, … |
| `BackgroundColorName` | `bg_red`, `red`, … (with or without `bg_` prefix) |
| `StyleName` | `bold`, `dim`, `italic`, `underline`, `strikethrough` |
| `IconName` | `ok`, `err`, `warn`, `info` |
| `IconMode` | `auto`, `nerd`, `std`, `ascii` |
| `IntentName` | `success`, `danger`, `warning`, `pending`, `debug`, `info` |

---

## Module exports

Everything available from `import raztint`:

```python
from raztint import (
    RazTint, tint,
    ok, err, warn, info, pending, debug,
    paint,
    rgb, bg_rgb, hex_color, bg_hex_color, color256, bg_color256,
    redact, MaskRule, DEFAULT_RULES,
    INTENTS, IntentConfig,
    ColorName, BackgroundColorName, StyleName, IconName, IconMode, IntentName,
    __version__,
)
```
