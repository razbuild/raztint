![Logo](https://raw.githubusercontent.com/razbuild/raztint/master/assets/logo.png)

![GitHub License](https://img.shields.io/github/license/razbuild/raztint?logoColor=ffffff&logoSize=auto&label=License&labelColor=1b1b1b&color=ab0000&cacheSeconds=3600)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/razbuild/raztint/ci.yml?branch=master&event=push&logo=githubactions&logoColor=ffffff&logoSize=auto&label=Build&labelColor=1b1b1b&color=ffc500&cacheSeconds=3600)
![Codecov](https://img.shields.io/codecov/c/github/razbuild/raztint?logo=codecov&logoColor=ffffff&logoSize=auto&label=Coverage&labelColor=1b1b1b&color=0d55cd&cacheSeconds=3600)
![PyPI - Version](https://img.shields.io/pypi/v/raztint?pypiBaseUrl=https%3A%2F%2Fpypi.org&logo=pypi&logoColor=ffffff&logoSize=auto&label=PyPi&labelColor=1b1b1b&color=ab0000&cacheSeconds=3600)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Frazbuild%2Fraztint%2Fmaster%2Fpyproject.toml&logo=python&logoColor=ffffff&logoSize=auto&label=Python&labelColor=1b1b1b&color=ffc500&cacheSeconds=3600)

A zero-dependency Python library for ANSI coloring and smart CLI icons that automatically adapt to your environment.

---

## Table of Contents
- [Preview](#preview)
- [What is RazTint?](#what-is-raztint)
- [Why RazTint?](#why-raztint)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Icons & Detection](#icons--detection)
- [Performance & Debugging](#performance--debugging)
- [Development](#development)
- [Support](#support)
- [License](#license)

---
## Preview

| ASCII Icons                                                                          | Nerd Font Icons                                                                             | Unicode Icons                                                                            |
|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| ![ASCII](https://raw.githubusercontent.com/razbuild/raztint/master/assets/ascii.png) | ![Nerd Font](https://raw.githubusercontent.com/razbuild/raztint/master/assets/nerdfont.png) | ![Unicode](https://raw.githubusercontent.com/razbuild/raztint/master/assets/unicode.png) |

---

## What is RazTint?
RazTint is a zero-dependency Python library for colored terminal output and smart CLI icons that automatically adapt to your environment.

---

## Why RazTint?

Most CLI coloring libraries either pull in many dependencies (like `rich`) or 
need platform-specific workarounds. RazTint was built for developers who want:

- **A single-file copy-pasteable solution** without any dependency hell.
- **Smart icons** that look great whether the user has a Nerd Font installed or 
  not, without manual configuration.
- **Predictable cross-platform behavior** — it works identically on Linux, macOS, 
  and Windows, even in CI environments.
- **Minimal decisions to make** — just import and use; it auto-detects everything.

If you’ve ever included a 30-line color script in a small CLI tool, RazTint is 
that script, done right and fully tested.

---

## Features

- Zero external dependencies (Python ≥ 3.10 standard library only)
- Three-tiered icon fallback: Nerd Font → Unicode → ASCII, with environment-aware detection
- Full ANSI 16-color support for foreground and background text
- Automatic TTY and Windows VT detection
- Fully type-hinted public API
- Support for text styles: bold, dim, italic, underline, and strikethrough
- Configurable via environment variables (`NO_COLOR`, `RAZTINT_FORCE_COLOR`, ...)
- Debug mode for troubleshooting font/color detection (`RAZTINT_DEBUG=1`)
- Cached detection results for negligible runtime overhead

---

## Requirements

- Python 3.10 or newer

---

## Installation

### From PyPI

```bash
pip install raztint
```

### From source

```bash
git clone https://github.com/razbuild/raztint.git
cd raztint

pip install -e .  # -e allows you to modify the source code in place
```

---

## Quick Start

You can import functions directly for quick usage, or instantiate the class for more control.

### Functional Usage

The easiest way to use RazTint is importing the pre-instantiated helpers:

```python
from raztint import bg_blue, green, red, ok, err, info, warn, bold, underline

# Coloring text
print(green("Success! The operation completed."))
print(red("Critical Error: Database not found."))

# Styling text
print(bold("This is bold text."))
print(underline(red("This is underlined red text.")))
print(red(bg_blue("This is red text on a blue background.")))

# Using Icons (Auto-adapts to Nerd Font/Unicode/ASCII)
print(f"{ok()} File saved successfully.")
print(f"{err()} Connection failed.")
print(f"{info()} Analysis in progress...")
print(f"{warn()} Disk space low.")
```

### Using the `tint` Instance

```python
from raztint import tint

print(tint.red("text"))
print(tint.ok(), "hello")
```
`tint` is a pre-instantiated singleton of `RazTint` for convenience.

### Class-based Usage

Useful if you need to toggle color support dynamically within an application instance or want a scoped instance.

```python
from raztint import RazTint

tint = RazTint()

# Toggle features manually if needed
tint.set_color(False) 

print(tint.blue("This will be plain text now because color is disabled."))
```

---

## Icons & Detection

### Icon Functions

```python
from raztint import ok, err, warn, info

print(ok(), "Operation completed")
print(err(), "An error happened")
print(warn(), "Be careful")
print(info(), "For your information")
```

### Icon Modes
RazTint attempts to make your CLI look as good as possible by detecting the font capabilities of the terminal.

| Mode  | ok   | err   | warn   | info   | Condition                           |
|-------|------|-------|--------|--------|-------------------------------------|
| Nerd  | [󰄬] | [󰅖]  | [󰈅]   | [󰙎]   | Detected Nerd Font via Env/Registry |
| Std   | [✓]  | [✗]   | [!]    | [i]    | UTF-8 supported, no Nerd Font       |
| ASCII | [OK] | [ERR] | [WARN] | [INFO] | Fallback                            |

> Note: Icons may not render correctly in GitHub preview depending on your browser font.

### Detection Logic

RazTint determines the best available icon and color mode using the following rules:

1. Nerd Font Mode:
   - Enabled if:
     - `RAZTINT_USE_NERD_ICONS` environment variable is set to `1`, `true`, `yes`, or `on`, OR
     - `NERDFONTS` or `NERD_FONTS` environment variable is set, OR
     - `FONT_NAME` or `TERM_FONT` environment variable contains "nerd" or "nf-", OR
     - A Nerd Font is detected via system checks:
       - **Linux**: Uses `fc-list` (fontconfig) to check installed fonts
       - **macOS**: Checks via `system_profiler` and font directories (`~/Library/Fonts`, `/Library/Fonts`)
       - **Windows**: Checks `C:\Windows\Fonts` directory via PowerShell

2. Standard Unicode Mode:
   - Enabled when UTF-8 encoding is available AND
   - `RAZTINT_NO_NERD_ICONS` is set (explicitly disables Nerd Fonts), OR
   - Nerd Fonts are not detected and not forced via `RAZTINT_USE_NERD_ICONS`

3. ASCII Mode:
   - Used when:
     - Output encoding is not UTF-8 (cannot encode Nerd Font or Unicode characters), OR
     - System encoding test fails for Unicode characters

### How to install Nerd Font?

To install Nerd Fonts, visit the official [website](https://www.nerdfonts.com/font-downloads).

---

## Configuration

You can control **RazTint** behavior using environment variables. This is useful for CI/CD pipelines or user overrides.

| Environment Variable             | Value                    | Description                                                                 |
|----------------------------------|--------------------------|-----------------------------------------------------------------------------|
| `NO_COLOR`                       | any                      | Disables all color output (standard specification).                         |
| `RAZTINT_NO_COLOR`               | any                      | Specific override to disable RazTint colors.                                |
| `RAZTINT_FORCE_COLOR`            | `1`, `true`, `yes`, `on` | Forces color output even if not a TTY.                                      |
| `RAZTINT_USE_NERD_ICONS`         | `1`, `true`, `yes`, `on` | Forces the use of Nerd Font icons.                                          |
| `RAZTINT_NO_NERD_ICONS`          | `1`, `true`, `yes`, `on` | Disables Nerd Font detection (falls back to Standard Unicode mode).         |
| `RAZTINT_SKIP_SYSTEM_FONT_SCAN`  | `1`, `true`, `yes`, `on` | Skips OS-level font scanning; only environment-based nerd font hints used.  |
| `RAZTINT_DEBUG`                  | `1`, `true`, `yes`, `on` | Enables debug logging about color/icon/font detection decisions to stderr.  |

---

## API Reference

### Color Functions

The following functions return strings wrapped with ANSI styling when supported:

| Standard Colors | Bright Variants      |
|-----------------|----------------------|
| `black(text)`   | `gray(text)`         |
| `red(text)`     | `bright_red(text)`   |
| `green(text)`   | `bright_green(text)` |
| `yellow(text)`  | `bright_yellow(text)`|
| `blue(text)`    | `bright_blue(text)`  |
| `magenta(text)` | `bright_magenta(text)`|
| `cyan(text)`    | `bright_cyan(text)`  |
| `white(text)`   | `bright_white(text)` |

Internally, these use `tint.color()`.

### Background Color Functions

The following functions return strings wrapped with ANSI background colors when supported:

| Standard Backgrounds | Bright Variants              |
|----------------------|------------------------------|
| `bg_black(text)`     | `bg_gray(text)`              |
| `bg_red(text)`       | `bg_bright_red(text)`        |
| `bg_green(text)`     | `bg_bright_green(text)`      |
| `bg_yellow(text)`    | `bg_bright_yellow(text)`     |
| `bg_blue(text)`      | `bg_bright_blue(text)`       |
| `bg_magenta(text)`   | `bg_bright_magenta(text)`    |
| `bg_cyan(text)`      | `bg_bright_cyan(text)`       |
| `bg_white(text)`     | `bg_bright_white(text)`      |

Internally, these use `tint.background()` and reset with `\033[49m`, so nested
background colors do not clear an outer foreground color.

### Text Style Functions
In addition to colors, RazTint provides functions for applying text styles. 
These styles use their own reset codes, so applying a style won't remove any color you have already applied.

| Function            | Description                |
|---------------------|----------------------------|
| `bold(text)`        | Makes text **bold**        |
| `dim(text)`         | Makes text dimmed          |
| `italic(text)`      | Makes text *italic*        |
| `underline(text)`   | Underlines text            |
| `strikethrough(text)`| Applies strikethrough      |

**Example:**
```python
from raztint import bold, italic, underline, red

# Mixing styles with colors
print(bold(red("This is a very important error message.")))
print(italic("This text is italic."))
print(underline("This text is underlined."))
```
> Known Limitation: bold and dim share the same ANSI reset code. Nesting one inside the other may lead to unexpected behavior.

### `format_text()` – Combine Colors, Backgrounds, and Styles

Instead of deeply nested function calls, use `format_text()` to apply multiple styling options in a single call.

**Signature:**
```python
format_text(text: str, color: str | int | None = None, bg: str | int | None = None,
            styles: str | list[str] | None = None, reset: bool = True) -> str
```

**Parameters:**
- `text`: The text to format
- `color`: Foreground color name (e.g., `"red"`, `"bright_green"`) or ANSI code (31, 91), or `None`
- `bg`: Background color name (e.g., `"red"`, `"bg_red"`) or ANSI code (41, 101), or `None`
- `styles`: A single style string (e.g., `"bold"`), list of style names (e.g., `["bold", "underline"]`), or `None`
- `reset`: If `True` (default), appends a full reset code `\033[0m`. If `False`, only style-specific resets are applied.

**Returns:** Formatted text with ANSI codes if color is enabled, plain text otherwise.

**Examples:**

```python
from raztint import format_text

# Single style and color
print(format_text("Error", color="red", styles="bold"))

# Multiple styles with background
print(format_text("Alert", color="white", bg="red", styles=["bold", "underline"]))

# Using the module-level function
print(format_text("Important message", color="yellow", bg="blue", styles="bold"))
```

**Comparison with nested calls:**

```python
# Old way (deeply nested)
from raztint import red, bold, underline
print(bold(underline(red("Important message"))))

# New way (cleaner and more readable)
from raztint import format_text
print(format_text("Important message", color="red", styles=["bold", "underline"]))
```

**Advanced: Concatenation with `reset=False`**

If you need to concatenate multiple formatted sections without a hard reset between them (useful for building up colored output), use `reset=False`:

```python
from raztint import format_text

part1 = format_text("WARNING:", color="yellow", reset=False)
part2 = format_text(" Disk full", color="red")
print(part1 + part2)
```

**Valid color names:**
Standard: `"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`, `"gray"`
Bright: `"bright_red"`, `"bright_green"`, `"bright_yellow"`, `"bright_blue"`, `"bright_magenta"`, `"bright_cyan"`, `"bright_white"`

For backgrounds, use the same names (e.g., `bg="red"` or `bg="bright_green"`).

**Valid style names:**
- `"bold"`
- `"dim"`
- `"italic"`
- `"underline"`
- `"strikethrough"`

---

## Icon Functions

These return appropriate status symbols based on environment detection:

- `ok()` - Returns a success icon (green checkmark)

- `err()` - Returns an error icon (red cross)

- `warn()` - Returns a warning icon (yellow exclamation)

- `info()` - Returns an info icon (blue 'i')

RazTint selects the best available style in this order:
1. Nerd Font icons (if installed)
2. Unicode icons (if UTF-8 is supported)
3. ASCII fallback

---

## RazTint Class Methods

When using the `RazTint` class directly, you have access to additional methods:

### `color(text: str, fg_code: str) -> str`

Low-level method to apply ANSI color codes to text. Returns the text with ANSI escape sequences when color is enabled, otherwise returns plain text.

**Parameters:**
- `text`: The text to colorize
- `fg_code`: ANSI color code (e.g., "31" for red, "32" for green)

**Example:**
```python
from raztint import RazTint

tint = RazTint()
colored = tint.color("Hello", "31")  # Red text
```

### `set_color(enabled: bool) -> None`

Enable or disable color output programmatically.

**Parameters:**
- `enabled`: `True` to enable colors, `False` to disable

**Example:**
```python
from raztint import RazTint

tint = RazTint()
tint.set_color(False)  # Disable colors
print(tint.red("This will be plain text"))
```

## RazTint Class Attributes

### `use_color: bool`

Boolean indicating whether color output is currently enabled. This is automatically set based on environment detection but can be modified via `set_color()`.

### `icon_mode: str`

Current icon mode being used. Possible values:
- `"nerd"` - Nerd Font icons
- `"std"` - Standard Unicode icons
- `"ascii"` - ASCII fallback icons

---

## Color Detection

Color support is determined by checking (in order):
1. `NO_COLOR` or `RAZTINT_NO_COLOR` environment variables (disables colors)
2. `RAZTINT_FORCE_COLOR` environment variable (forces colors)
3. Whether output is connected to a TTY (`sys.stdout.isatty()`)
4. On Windows: Attempts to enable Virtual Terminal processing
5. `TERM` environment variable (must not be "dumb")

If color is not supported, all color functions return plain text.

---

## Performance & Debugging

In most environments, RazTint's detection overhead is negligible thanks to internal caching. However, in restricted or slow environments you can:

- Disable OS-level font scanning while still allowing env-based nerd font hints:

  ```bash
  RAZTINT_SKIP_SYSTEM_FONT_SCAN=1
  ```

- Inspect why a particular mode was chosen (color on/off, icon mode, font detection) by enabling debug logs:

  ```bash
  RAZTINT_DEBUG=1
  ```

Debug messages are printed to standard error and are disabled by default.

---

## Development

If you want to work on RazTint locally:

1. Clone the repository and install in editable mode with development tools:

   ```bash
   git clone https://github.com/razbuild/raztint.git
   cd raztint
   uv sync --group dev
   ```

2. Run the test suite:

   ```bash
   python -m pytest
   ```

3. Run formatting, linting, and type checking (kept in sync with CI):

   ```bash
   black src tests
   ruff check src tests
   ty check src tests
   ```

---

## Support

- 🐛 **Found a bug?** [Open an issue](https://github.com/razbuild/raztint/issues)
- 💡 **Have a suggestion?** [Open an issue](https://github.com/razbuild/raztint/issues)

---

## License

MIT License

