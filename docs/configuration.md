# Configuration

[← Documentation index](index.md)

Control RazTint behavior with environment variables. Useful for CI/CD pipelines, user overrides, and troubleshooting.

## Environment variables

| Variable | Value | Description |
|---|---|---|
| `NO_COLOR` | any | Disables all color output ([standard spec](https://no-color.org/)). |
| `RAZTINT_NO_COLOR` | any | RazTint-specific override to disable colors. |
| `RAZTINT_FORCE_COLOR` | `1`, `true`, `yes`, `on` | Forces color output even if not a TTY. |
| `RAZTINT_USE_NERD_ICONS` | `1`, `true`, `yes`, `on` | Forces Nerd Font icons. |
| `RAZTINT_NO_NERD_ICONS` | `1`, `true`, `yes`, `on` | Disables Nerd Fonts (falls back to Unicode). |
| `RAZTINT_SKIP_SYSTEM_FONT_SCAN` | `1`, `true`, `yes`, `on` | Skips OS font scanning; env hints only. |
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

# Faster startup -> skip font scan
RAZTINT_SKIP_SYSTEM_FONT_SCAN=1 python app.py

# Debug detection decisions
RAZTINT_DEBUG=1 python app.py
```

## Programmatic control

```python
from raztint import RazTint, tint

# Module singleton
tint.set_color(False)
print(tint.use_color)   # False
print(tint.icon_mode)   # "nerd", "std", or "ascii"

# Scoped instance
local = RazTint()
local.set_color(True)
```

Detection results are cached (`lru_cache` for encoding probes, module-level font scan). Overhead is negligible. Use `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in slow or sandboxed environments.