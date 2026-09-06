# Getting Started 🚀

[Documentation home](index.md)

RazTint formats strings for command-line applications. It can add ANSI colors, styles, and status icons, then returns an ordinary `str` that you can pass to `print()`, a logger, or another string API.

## 📦 Requirements and installation

RazTint requires Python 3.10 or later.

```bash
pip install raztint

# Or add it to a uv project.
uv add raztint
```

To work from a source checkout:

```bash
git clone https://github.com/razbuild/raztint.git
cd raztint
uv sync
```

## 🎯 Print a semantic message

Start with an intent. An intent selects a suitable color, icon, and style for a message category.

```python
from raztint import paint

print(paint("Build passed.", intent="success"))
print(paint("Connection failed.", intent="error"))
print(paint("Disk space is low.", intent="warning"))
```

See [Intents](intents.md) for the complete preset list and override behavior.

## 🎨 Format text directly

Use `paint()` when you need a specific presentation rather than a semantic preset.

```python
from raztint import paint

print(paint("Done!", color="green", styles="bold"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))
print(paint("File saved.", color="green", icon="ok"))
```

`color` and `bg` accept a named color, a six-digit hex value, an RGB tuple, or an ANSI/256-color integer:

```python
print(paint("Orange", color=208))
print(paint("Orange", color=(255, 120, 0)))
print(paint("Orange", color="#ff7800"))
```

For all accepted values and parameters, see the [API Reference](api-reference.md).

## 🔤 Icons

The status helpers return an icon that adapts to the terminal. RazTint uses a Nerd Font icon when available, then standard Unicode, then ASCII.

```python
from raztint import err, ok, warn

print(f"{ok()} File saved.")
print(f"{err()} Connection failed.")
print(f"{warn()} Disk space is low.")
```

You can set `icon_mode` for one `paint()` call when a stable representation is useful:

```python
print(paint("Build passed.", intent="success", icon_mode="ascii"))
```

Read [Icons and Detection](icons-and-detection.md) for the available modes and detection rules.

## 🔒 Redact sensitive text

Set `redact=True` to mask supported secret patterns before formatting occurs.

```python
from raztint import paint

print(paint("password=1234", intent="debug", redact=True))
```

Use `redact()` directly when no formatting is needed. [Security and Redaction](redaction.md) describes the built-in patterns and custom rules.

## 🧩 Shared instance or your own instance

`paint()` and the icon helpers use the shared `tint` instance. Create `RazTint()` when one part of an application needs independent color settings.

```python
from raztint import RazTint, tint

tint.set_color(False)  # Changes the shared instance.

plain_output = RazTint()
plain_output.set_color(False)
print(plain_output.format_text("No ANSI codes", color="blue"))
```

## 🔀 Render by application state

Use `case()` when the output depends on an application state. Map each state to text and a semantic intent.

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

The selected intent supplies the corresponding color, icon, and style.

For more details, see the [API Reference](api-reference.md).

## ⏳ Temporary terminal output

Use `transient()` for output that should remain visible while an operation is running, then disappear when it finishes.

```python
import time

from raztint import tint

with tint.transient("Working..."):
    time.sleep(2)

print("Done!")
```

You can also update or erase a transient line manually:

```python
line = tint.transient("Connecting...")

line.update("Connected")
line.erase()
```

Transient output is active only on TTY streams. When output is redirected or piped, it performs no terminal control operations.

For the full API, see the [API Reference](api-reference.md).

See [Configuration](configuration.md) for environment variables and runtime controls.
