# Icons & Detection

[← Documentation index](index.md)

RazTint picks the best icon rendering mode for the current terminal and optionally scans the OS for installed Nerd Fonts.

---

## Icon functions

```python
from raztint import ok, err, warn, info

print(ok(), "Operation completed")
print(err(), "An error happened")
print(warn(), "Be careful")
print(info(), "For your information")
```

---

## Icon modes

| Mode | ok | err | warn | info | Condition |
|---|---|---|---|---|---|
| Nerd | 󰄬 | 󰅖 | 󰈅 | 󰙎 | Nerd Font detected or forced |
| Std | ✓ | ✗ | ! | i | UTF-8 supported, no Nerd Font |
| ASCII | OK | ERR | WARN | INFO | Fallback |

> Icons may not render correctly in GitHub preview depending on your browser font.

---

## Detection logic

RazTint determines an instance's default icon mode at initialization:

### 1. ASCII mode

Used when stdout encoding cannot represent the Nerd Font probe character. In practice, this is the fallback mode for terminals that cannot reliably display the richer icon sets.

### 2. Nerd Font mode

Enabled when any of the following is true:

- `RAZTINT_USE_NERD_ICONS` is set to `1`, `true`, `yes`, or `on`
- `NERDFONTS` or `NERD_FONTS` environment variable is set
- `FONT_NAME` or `TERM_FONT` contains `"nerd"` or `"nf-"`
- A Nerd Font is detected via system checks:
  - **Linux:** `fc-list` (fontconfig)
  - **macOS:** `system_profiler` and font directories
  - **Windows:** `C:\Windows\Fonts` via PowerShell

Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` to skip OS scanning and rely only on environment hints.

### 3. Standard Unicode mode

Used when UTF-8 encoding works and either:

- `RAZTINT_NO_NERD_ICONS` is set (explicitly disables Nerd Fonts), or
- Nerd Fonts are not detected and not forced

---

## Overriding icon mode per call

```python
from raztint import paint

print(paint("Done!", color="green", icon="ok", icon_mode="nerd"))
print(paint("Done!", color="green", icon="ok", icon_mode="std"))
print(paint("Done!", color="green", icon="ok", icon_mode="ascii"))
print(paint("Done!", color="green", icon="ok", icon_mode="auto"))
```

| `icon_mode` | Behavior |
|---|---|
| `None` | Use instance default (`tint.icon_mode`) |
| `"auto"` | Try nerd → std → ascii at call time |
| `"nerd"` | Nerd icon, fallback to std then ascii |
| `"std"` | Unicode icon, fallback to ascii |
| `"ascii"` | Always ASCII |

---

## Color detection

Color support is determined by checking (in order):

1. `NO_COLOR` or `RAZTINT_NO_COLOR` — disables colors
2. `RAZTINT_FORCE_COLOR` — forces colors even when not a TTY
3. Whether stdout is a TTY (`sys.stdout.isatty()`)
4. On Windows: Virtual Terminal processing is enabled
5. `TERM` is set and not `"dumb"`

When color is disabled, `paint()` returns the icon symbol for the active mode plus unstyled text.
Toggle at runtime:

```python
from raztint import tint

tint.set_color(False)
print(tint.red("plain text"))
```

---

## Installing Nerd Fonts

Download from the official [Nerd Fonts site](https://www.nerdfonts.com/font-downloads), install the font, and set your terminal to use it. RazTint will detect it on the next run (unless scanning is skipped).

---

## Debugging

Enable detection logs to stderr:

```bash
RAZTINT_DEBUG=1 python your_script.py
```

See [Configuration](configuration.md) for all environment variables.

---

## See also

- [Configuration](configuration.md)
- [API Reference Icon functions](api-reference.md#icon-functions)
