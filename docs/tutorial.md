# RazTint Tutorial

[← Documentation index](index.md)

A friendly walk-through for new users. By the end you will understand *why* RazTint works the way it does, not just *how* to call it.

---

## Philosophy

> 💡 RazTint believes terminal styling should be *zero-friction*: no dependencies, no configuration files, no guessing the user's environment. It figures out the rest so you can focus on your CLI logic.

Three design rules flow from that:

1. **Zero dependencies** — the standard library is enough.
2. **Smart auto-detection** — colors and icons adapt to the terminal at import time.
3. **Minimal decisions for the developer** — one function (`paint()`) covers almost every case.

---

## How environment detection works

RazTint checks the environment once at import time and caches the result.

### Color detection

Checked in this order:

1. `NO_COLOR` or `RAZTINT_NO_COLOR` set → colors off.
2. `RAZTINT_FORCE_COLOR=1` → colors on (useful in CI).
3. `sys.stdout.isatty()` → on when running in a real terminal.
4. Windows Virtual Terminal processing enabled → on.
5. `TERM` set and not `"dumb"` → on.

When colors are off, every color function returns plain text.

### The three-tier icon system

| Mode | ok | err | warn | info | When active |
|---|---|---|---|---|---|
| `nerd` | 󰄬 | 󰅖 | 󰈅 | 󰙎 | Nerd Font detected or forced |
| `std` | ✓ | ✗ | ! | i | UTF-8 works, no Nerd Font |
| `ascii` | OK | ERR | WARN | INFO | Fallback for all other terminals |

RazTint picks `nerd` when any of these is true:

- `RAZTINT_USE_NERD_ICONS=1`
- `NERDFONTS` or `NERD_FONTS` env variable is set
- `FONT_NAME` or `TERM_FONT` contains `nerd` or `nf-`
- A Nerd Font is found via `fc-list` (Linux), `system_profiler` (macOS), or PowerShell (Windows)

It picks `std` when UTF-8 encoding works and no Nerd Font is found. It falls back to `ascii` otherwise.

You can inspect or override the detected mode at runtime:

```python
from raztint import tint

print(tint.icon_mode)      # "nerd", "std", or "ascii"
print(tint.use_color)      # True / False

tint.set_color(False)      # disable color for this instance
```

Or force a mode via environment:

```bash
RAZTINT_USE_NERD_ICONS=1 python app.py    # force nerd
RAZTINT_NO_NERD_ICONS=1  python app.py    # force std (not ascii)
NO_COLOR=1               python app.py    # strip all color
```

---

## Caching and performance

Detection runs once per `RazTint` instance at construction. Font scanning is additionally wrapped in `lru_cache`, so repeated instantiation does not re-scan the OS.

In environments where `fc-list` or `system_profiler` is slow (sandboxes, containers):

```bash
RAZTINT_SKIP_SYSTEM_FONT_SCAN=1 python app.py
```

Nerd mode still activates from environment variable hints even when scanning is skipped.

---

## Step-by-step: from zero to real CLI output

### Step 1 — Install

```bash
pip install raztint
```

### Step 2 — Color helpers

The simplest way: import a color function and call it.

```python
from raztint import green, red, yellow, blue

print(green("Everything is fine."))
print(red("Something went wrong."))
print(yellow("Disk space is low."))
print(blue("Connecting to host..."))
```

### Step 3 — Style helpers

```python
from raztint import bold, italic, underline, dim

print(bold("Important"))
print(dim("Verbose log line — not critical"))
print(underline(red("Error — see below")))   # compose freely
```

### Step 4 — Icon helpers

Icons auto-adapt to the terminal — you never choose the mode at call time.

```python
from raztint import ok, err, warn, info

print(f"{ok()}  File saved.")
print(f"{err()} Connection refused.")
print(f"{warn()} Disk space low.")
print(f"{info()} Analysis in progress...")
```

### Step 5 — `paint()` for everything in one call

```python
from raztint import paint

print(paint("Done!", color="green", styles="bold"))
print(paint("Connection failed.", color="red", icon="err"))
print(paint("Alert", color="white", bg="bg_red", styles=["bold", "underline"]))
```

`paint()` is an alias for `tint.format_text()`. Both names work identically.

### Step 6 — Intents

Intents are semantic presets. Instead of spelling out color + icon + style every time, use a name:

```python
from raztint import paint

print(paint("Deployment complete.",   intent="success"))
print(paint("Invalid credentials.",   intent="danger"))
print(paint("Disk space low.",        intent="warning"))
print(paint("Waiting for worker...",  intent="pending"))
print(paint("cache hit ratio=0.92",   intent="debug"))
print(paint("Server version 2.1.0",   intent="info"))
```

Explicit parameters always override the intent's defaults:

```python
# success = green + ok icon + bold, but here we suppress the icon
print(paint("Done.", intent="success", icon=None))
```

### Step 7 — Redaction

Never let secrets reach the terminal log:

```python
from raztint import paint, redact

# Standalone — mask before using elsewhere
safe = redact("password=hunter2 api_key=ghp_abc123")
print(safe)
# password=**** api_key=****

# Combined with paint() — mask and format in one call
raw = "Connecting with token=sk-abc123 to postgres://user:pass@db.internal"
print(paint(raw, intent="debug", redact=True))
```

Covered by default: passwords, generic secrets, GitHub tokens, OpenAI keys, Slack tokens, JWTs, Bearer headers, URL credentials, credit-card numbers.

---

## Best practices for real projects

**Use intents for all user-facing messages.** They keep output consistent and let you change the visual style in one place.

```python
# Preferred
print(paint(f"Processed {n} files.", intent="success"))

# Avoid — couples style to business logic
print(paint(f"Processed {n} files.", color="green", styles="bold", icon="ok"))
```

**Suppress icons in unit tests.** Force ASCII mode so test output is stable across environments:

```bash
RAZTINT_NO_NERD_ICONS=1 pytest
# or set TERM=dumb in CI to strip color too
```

**Use `reset=False` for inline multi-segment lines** so styles carry across joins:

```python
label  = paint("BUILD FAILED:", color="red", styles="bold", reset=False)
detail = paint(" see errors above", color="red")
print(label + detail)
```

**Create a scoped instance for library code.** Avoid mutating the module-level `tint` singleton:

```python
from raztint import RazTint

_t = RazTint()
_t.set_color(False)   # library output always plain — caller controls terminal
```

---

## Known limitations

- **Python 3.10+.** Older versions are not supported.
- **Font detection relies on OS tools.** `fc-list` on Linux, `system_profiler` on macOS, PowerShell on Windows. Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in sandboxed environments.
- **Strict `NO_COLOR` compliance.** When `NO_COLOR` is set, all colour output is suppressed regardless of other settings.

---

## See also

- [Getting Started](getting-started.md) — API reference with all function signatures
- [Icons & Detection](icons-and-detection.md) — full detection logic
- [Configuration](configuration.md) — all environment variables
- [Intents](intents.md) — full intent registry
- [Security & Redaction](redaction.md) — custom mask rules
- [`examples/basic_usage.py`](../examples/basic_usage.py) — runnable quick-start script
- [`examples/format_text_demo.py`](../examples/format_text_demo.py) — full `paint()` showcase
- [`examples/real_world_cli.py`](../examples/real_world_cli.py) — simulated CLI integration
