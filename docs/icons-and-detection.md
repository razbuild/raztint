# Icons and Detection

[Documentation home](index.md)

RazTint detects whether color and richer icon glyphs are usable in the current environment. The result becomes the default for a `RazTint` instance, while individual `paint()` calls can choose an icon mode explicitly.

## Icon modes

| Mode | `ok` | `err` | `warn` | `info` | `pending` | `debug` |
|---|---|---|---|---|---|---|
| `nerd` | `[󰄬]` | `[󰅖]` | `[]` | `[]` | `[󱦟]` | `[󰃤]` |
| `std` | `[✓]` | `[✗]` | `[!]` | `[i]` | `[PENDING]` | `[DEBUG]` |
| `ascii` | `[OK]` | `[ERR]` | `[WARN]` | `[INFO]` | `[PENDING]` | `[DEBUG]` |

| `icon_mode` value | Behavior |
|---|---|
| `None` | Uses the instance default (`tint.icon_mode`). |
| `"auto"` | Uses a Nerd Font icon when available, otherwise standard Unicode, then ASCII. |
| `"nerd"` | Uses a Nerd Font icon when defined, otherwise standard Unicode, then ASCII. |
| `"std"` | Uses the standard Unicode icon when defined, otherwise ASCII. |
| `"ascii"` | Always uses ASCII. |

```python
from raztint import paint

print(paint("Done!", color="green", icon="ok", icon_mode="ascii"))
```

## How icon detection works

At initialization, RazTint checks whether stdout's encoding can represent a Nerd Font probe. If not, it uses `ascii` mode. Otherwise, it chooses in this order:

1. `RAZTINT_USE_NERD_ICONS` forces `nerd` mode.
2. `RAZTINT_NO_NERD_ICONS` forces `std` mode.
3. Environment hints or a system font scan can enable `nerd` mode.
4. RazTint uses `std` mode when no Nerd Font is found.

The environment hints are `NERDFONTS` or `NERD_FONTS` with a truthy value, and `FONT_NAME` or `TERM_FONT` containing a Nerd Font indicator. On Linux and other POSIX systems, the scan uses `fc-list`; macOS checks font directories and can use `system_profiler`; Windows uses PowerShell. Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` to rely only on environment hints.

## How color detection works

Color is disabled when `NO_COLOR` or `RAZTINT_NO_COLOR` is present, even if it has an empty value. Otherwise, `RAZTINT_FORCE_COLOR` enables color when it has a truthy value (`1`, `true`, `yes`, or `on`). Without an override, color is enabled only when stdout is a TTY and:

- Windows Virtual Terminal processing can be enabled on Windows, or
- `TERM` is set to a value other than `dumb` on other platforms.

When color is disabled, RazTint still returns icons and text, but omits ANSI escape codes.

## Troubleshoot detection

Set `RAZTINT_DEBUG=1` before running your command to write detection decisions to stderr.

```bash
RAZTINT_DEBUG=1 python your_script.py
```

See [Configuration](configuration.md) for all supported environment variables.
