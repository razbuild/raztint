# Tutorial

[← Documentation index](index.md)

A walk-through for new users. By the end you'll understand *why* RazTint works the way it does, not just *how* to call it.

## Philosophy

> [!NOTE]
> RazTint believes terminal styling should be *zero-friction*: no dependencies, no configuration files, no guessing the user's environment. It figures out the rest so you can focus on your CLI logic.

Three design rules flow from that:

1. **Zero dependencies** - the standard library is enough.
2. **Smart auto-detection** - colors and icons adapt to the terminal at import time.
3. **One function** - `paint()` covers almost every case.

## How environment detection works

RazTint checks the environment once at import time and caches the result. See [Icons & Detection](icons-and-detection.md) for the full detection logic.

```python
from raztint import tint

print(tint.icon_mode)      # "nerd", "std", or "ascii"
print(tint.use_color)      # True / False
tint.set_color(False)      # disable color at runtime
```

## Step by step

### 1. Colors

```python
from raztint import paint

print(paint("Everything is fine.", color="green"))
print(paint("Something went wrong.", color="red"))
print(paint("Disk space is low.", color="yellow"))
```

### 2. Styles

```python
print(paint("Important", styles="bold"))
print(paint("Verbose log line", styles="dim"))
print(paint("Error - see below", color="red", styles="underline"))
```

### 3. Icon helpers

```python
from raztint import ok, err, warn, info, pending, debug

print(f"{ok()}  File saved.")
print(f"{err()} Connection refused.")
print(f"{warn()} Disk space low.")
```

### 4. `paint()` with icons

```python
print(paint("Done!", color="green", styles="bold"))
print(paint("Connection failed.", color="red", icon="err"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))
```

### 5. Intents

> **Breaking change (v0.9.0):** `intent="danger"` was renamed to `intent="error"`.

Semantic presets replace manual color + icon + style selections:

```python
print(paint("Deployment complete.",   intent="success"))
print(paint("Invalid credentials.",   intent="error"))
print(paint("Disk space low.",        intent="warning"))
print(paint("Waiting for worker...",  intent="pending"))
print(paint("cache hit ratio=0.92",   intent="debug"))
print(paint("Server version 2.1.0",   intent="info"))

# Explicit parameters override intent defaults
print(paint("Done.", intent="success", icon=None))
```

Migration:

```python
# Before (<= 0.8.x)
paint("Invalid credentials.", intent="danger")

# After (>= 0.9.0)
paint("Invalid credentials.", intent="error")
```

### 6. Redaction

```python
from raztint import paint, redact

# Standalone
safe = redact("password=hunter2 api_key=ghp_abc123")
print(safe)
# password=**** api_key=****

# Combined with paint()
raw = "Connecting with token=sk-abc123 to postgres://user:pass@db.internal"
print(paint(raw, intent="debug", redact=True))
```

Covered by default: passwords, GitHub tokens, OpenAI keys, Slack tokens, JWTs, Bearer headers, URL credentials, credit-card numbers.

## Best practices

**Use intents for all user-facing messages.** They keep output consistent and let you change the visual style in one place.

```python
# Preferred
print(paint(f"Processed {n} files.", intent="success"))

# Avoid - couples style to business logic
print(paint(f"Processed {n} files.", color="green", styles="bold", icon="ok"))
```

**Suppress icons in unit tests.** Force ASCII mode for stable test output:

```bash
RAZTINT_NO_NERD_ICONS=1 pytest
```

**Use `reset=False` for inline multi-segment lines:**

```python
label  = paint("BUILD FAILED:", color="red", styles="bold", reset=False)
detail = paint(" see errors above", color="red")
print(label + detail)
```

**Create a scoped instance for library code.** Avoid mutating the module-level `tint` singleton:

```python
from raztint import RazTint

_t = RazTint()
_t.set_color(False)   # library output always plain
```

## Known limitations

- **Python 3.10+.** Older versions are not supported.
- **Font detection relies on OS tools.** Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in sandboxed environments.
- **Strict `NO_COLOR` compliance.** When `NO_COLOR` is set, all colour output is suppressed.

## See also

- [Getting Started](getting-started.md) - all `paint()` parameters and color types
- [API Reference](api-reference.md) - full function signatures and type aliases
- [Intents](intents.md) - intent registry and override behavior
- [Security & Redaction](redaction.md) - custom mask rules
- [examples/paint_demo.py](../examples/paint_demo.py) - runnable feature showcase
- [examples/real_world_cli.py](../examples/real_world_cli.py) - simulated CLI integration