# Configuration

[Documentation home](index.md)

Use environment variables to control RazTint in CI, provide user overrides, or troubleshoot terminal detection.

## Environment variables

| Variable | Value | Description |
|---|---|---|
| `NO_COLOR` | any | Disables all color output ([standard spec](https://no-color.org/)). |
| `RAZTINT_NO_COLOR` | any | RazTint-specific override to disable colors. |
| `RAZTINT_FORCE_COLOR` | `1`, `true`, `yes`, `on` | Forces color output even if not a TTY. |
| `RAZTINT_USE_NERD_ICONS` | `1`, `true`, `yes`, `on` | Forces Nerd Font icons. |
| `RAZTINT_NO_NERD_ICONS` | `1`, `true`, `yes`, `on` | Disables Nerd Font icons and uses standard Unicode when possible. |
| `RAZTINT_SKIP_SYSTEM_FONT_SCAN` | `1`, `true`, `yes`, `on` | Skips system font scanning and uses environment hints only. |
| `RAZTINT_DEBUG` | `1`, `true`, `yes`, `on` | Logs detection decisions to stderr. |

Additional hints for font detection:

| Variable | Effect |
|---|---|
| `NERDFONTS`, `NERD_FONTS` | Treat as Nerd Font available |
| `FONT_NAME`, `TERM_FONT` | If value contains `nerd` or `nf-`, enable Nerd mode |

## Common scenarios

```bash
# Force colors in CI (off by default when not a TTY)
RAZTINT_FORCE_COLOR=1 pytest --tb=short

# Disable colors entirely
NO_COLOR=1 python app.py

# Disable Nerd Fonts, keep Unicode icons
RAZTINT_NO_NERD_ICONS=1 python app.py

# Faster startup: skip the font scan
RAZTINT_SKIP_SYSTEM_FONT_SCAN=1 python app.py

# Debug detection decisions
RAZTINT_DEBUG=1 python app.py
```

## Programmatic control

```python
from raztint import RazTint, tint

# Shared module instance
tint.set_color(False)
print(tint.use_color)   # False
print(tint.icon_mode)   # "nerd", "std", or "ascii"

# Scoped instance
local = RazTint()
local.set_color(True)
```

Encoding probes and system font scans are cached. Use `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in slow or sandboxed environments.
