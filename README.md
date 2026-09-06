<div align="center">

<img src="https://raw.githubusercontent.com/razbuild/raztint/main/assets/RazTint.svg" alt="RazTint Logo" width="185" />

# RazTint

**Semantic formatting for Python CLIs with built-in secret redaction.**

<br>

[![Python Versions](https://img.shields.io/pypi/pyversions/raztint)](https://pypi.org/project/raztint/)
[![PyPI Version](https://img.shields.io/pypi/v/raztint)](https://pypi.org/project/raztint/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](https://github.com/razbuild/raztint)
[![Codecov](https://img.shields.io/codecov/c/github/razbuild/raztint/main)
](https://codecov.io/gh/razbuild/raztint)

</div>

Keep your CLI output consistent. Write what a message means, not how it should look. RazTint handles colors, icons, and common secret redaction for you.

---

## Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/razbuild/raztint/main/assets/preview.png" alt="RazTint preview: Nerd Font, Unicode, and ASCII icon modes with colored and styled output examples" width="644"/>
</p>

<p align="center">
<em>A simulated production log stream: 9 secrets detected, 9 secrets redacted, 0 leaked to the terminal.</em>
</p>

---

## Installation

Requires Python `3.10+`.

```bash
pip install raztint
# with uv
uv add raztint
```

From source:

```bash
git clone https://github.com/razbuild/raztint.git
cd raztint
uv sync
```

---

## Quick Start

```python
from raztint import paint, ok

# icon shortcut
print(f"{ok()} Build passed.")

print(paint("Connection failed.", intent="error"))

# secrets are redacted before the string is printed
print(paint("password=1234", intent="debug", redact=True))
# password=****
```

`paint()` returns a plain string. Pass it to `print()`, a `logging` handler, or anywhere else a string works.

See [Getting Started](docs/getting-started.md) for installation and common usage.

---

## Why RazTint

- **Semantic output instead of ANSI escape codes**
- **Automatic secret redaction before rendering**
- **Works anywhere a string is accepted**

---

## The problem

CLI output drifts over time. One module prints green for success, another adds an emoji, a third does both differently. Six months in, nothing agrees.

Debug logging is often where secrets slip through. A stray `print(f"token={token}")` is easy to add while troubleshooting and easy to forget. It ends up in your terminal or your logs.

```python
# before: every call site invents its own formatting, and secrets slip through
print(f"\033[31mAuth failed for token={token}\033[0m")

# after: one call, styled and redacted
print(paint(f"Auth failed for token={token}", intent="error", redact=True))
# Auth failed for token=****
```

---

## Core features

- **Semantic intents** `success`, `error`, `warning`, `debug`, and more. Use semantic names instead of choosing colors manually.

- **State-aware output** `case()` maps application states to semantic intents, while `transient()` provides temporary terminal output for in-progress operations.

- **Redaction** masks `key=value` pairs such as `password=`, `api_key=`, and `token=`. Patterns are configurable, see [Security and Redaction](docs/redaction.md).

- **Icon helpers** `ok()`, `err()`, `warn()`, `info()`, `pending()`, `debug()`. Falls back from Nerd Font to Unicode to ASCII depending on the terminal.

- **Manual control** raw `16/256/True` Color and text styles, for the cases intents don't cover.

- **Type hints throughout** ships with `py.typed`. Respects `NO_COLOR` and `RAZTINT_FORCE_COLOR`.

---

## Design philosophy

> [!NOTE]
> Make terminal output consistent, meaningful, and safe by default.

RazTint is not a terminal UI framework. It doesn't hook into `logging` or replace a handler. It stays a formatting layer, on purpose:

- ANSI color support
- Semantic logging helpers
- Automatic icon fallback
- Secret redaction
- Zero external dependencies

A small scope keeps RazTint focused.

---

## Documentation

| Guide                                                                                             | Description                                             |
| --------------------------------------------------------------------------------------------------| ---------------------------------------------------------|
| [Getting Started](https://github.com/razbuild/raztint/blob/main/docs/getting-started.md)        | Functional usage, `paint()`, and the `tint` instance      |
| [API Reference](https://github.com/razbuild/raztint/blob/main/docs/api-reference.md)            | Colors, styles, icons, and `RazTint` class methods         |
| [Intents](https://github.com/razbuild/raztint/blob/main/docs/intents.md)                        | Semantic presets for common CLI messages                   |
| [Security and Redaction](https://github.com/razbuild/raztint/blob/main/docs/redaction.md)       | Masking tokens, credentials, and custom rules               |
| [Icons and Detection](https://github.com/razbuild/raztint/blob/main/docs/icons-and-detection.md) | Icon modes and environment/font/color detection logic      |
| [Configuration](https://github.com/razbuild/raztint/blob/main/docs/configuration.md)            | Environment variables and runtime toggles                    |
| [Development](https://github.com/razbuild/raztint/blob/main/docs/development.md)                | Local setup, tests, and linting                              |

**Examples:** [`showcase.py`](https://github.com/razbuild/raztint/blob/main/examples/showcase.py) · [`file_processor.py`](https://github.com/razbuild/raztint/blob/main/examples/file_processor.py) · [`redaction_demo.py`](https://github.com/razbuild/raztint/blob/main/examples/redaction_demo.py)

---

## Known limitations

- Python `3.10+` only.
- Font detection relies on OS tools (`fc-list`, `system_profiler`, PowerShell). Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in sandboxed environments.
- Setting `NO_COLOR` suppresses all color output, regardless of other settings.

---

## Contributing

PRs and issues are welcome. Open an issue first to discuss any new feature.

See [Contributing Guide](https://github.com/razbuild/raztint/blob/main/CONTRIBUTING.md) for setup and guidelines.

---

## License

[![License](https://img.shields.io/pypi/l/raztint)](https://github.com/razbuild/raztint/blob/main/LICENSE)

<div align="center">
  <img src="https://raw.githubusercontent.com/razbuild/.github/main/assets/badge.svg" alt="Made by RazBuild" width="160">
</div>
