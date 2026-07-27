# Icons & Detection

[← Documentation index](index.md)

RazTint picks the best icon rendering mode for the current terminal and optionally scans the OS for installed Nerd Fonts.

## Icon modes

| Mode | ok | err | warn | info | pending | debug | Condition |
|---|---|---|---|---|---|---|---|
| Nerd | 󰄬 | 󰅖 | 󰈅 | 󰙎 | 󱦟 | 󰃤 | Nerd Font detected or forced |
| Std | ✓ | ✗ | ! | i | PENDING | DEBUG | UTF-8, no Nerd Font |
| ASCII | OK | ERR | WARN | INFO | PENDING | DEBUG | Fallback |

## Detection logic

RazTint determines the default icon mode at initialization:

1. **ASCII** — stdout encoding cannot represent the Nerd Font probe character.
2. **Nerd Font** — enabled when any of:
   - `RAZTINT_USE_NERD_ICONS` is set to `1`, `true`, `yes`, or `on`
   - `NERDFONTS` or `NERD_FONTS` is set
   - `FONT_NAME` or `TERM_FONT` contains `"nerd"` or `"nf-"`
   - A Nerd Font is detected via system scan (`fc-list` on Linux, `system_profiler` on macOS, PowerShell on Windows)
3. **Standard Unicode** — UTF-8 works and either `RAZTINT_NO_NERD_ICONS` is set or no Nerd Font is found.

Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` to skip OS scanning and rely only on environment hints.

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

## Color detection

Color support is checked in this order:

1. `NO_COLOR` or `RAZTINT_NO_COLOR` set → colors off.
2. `RAZTINT_FORCE_COLOR=1` → colors on.
3. `sys.stdout.isatty()` → on in a real terminal.
4. Windows: Virtual Terminal processing enabled → on.
5. `TERM` set and not `"dumb"` → on.

When color is disabled, `paint()` returns the icon symbol plus unstyled text.

```python
from raztint import tint

tint.set_color(False)
print(tint.format_text("plain text", color="red"))
```

## Installing Nerd Fonts

Download from [Nerd Fonts](https://www.nerdfonts.com/font-downloads), install the font, and set your terminal to use it. RazTint detects it on the next run.

## Debugging

```bash
RAZTINT_DEBUG=1 python your_script.py
```

Detection logs go to stderr. See [Configuration](configuration.md) for all environment variables.