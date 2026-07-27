<div align="center">
  <img src="https://raw.githubusercontent.com/razbuild/raztint/master/assets/RazTint.svg" alt="RazTint" width="400" />
  <br><br>

  [![Python Versions](https://img.shields.io/pypi/pyversions/raztint)](https://pypi.org/project/raztint/)

  [![PyPI Version](https://img.shields.io/pypi/v/raztint)](https://pypi.org/project/raztint/)
  [![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)](https://github.com/razbuild/raztint)
  [![Codecov](https://img.shields.io/codecov/c/github/razbuild/raztint)](https://codecov.io/gh/razbuild/raztint)

</div>

Every CLI project eventually invents its own way to print "success" or "error." One module uses green text, another adds an emoji, a third does both differently. Output looks inconsistent, breaks in CI, and nobody notices until a log line leaks a password.

```python
# before
print("\033[32mSuccess\033[0m")

# after
print(paint("Success", intent="success"))
```

RazTint defines a fixed mapping from intent (`success`, `error`, `warning`, …) to color and icon once, and every call site reuses that same mapping instead of picking its own.

---

## Installation

Requires Python 3.10+.

```bash
pip install raztint
```

From source:

```bash
git clone https://github.com/razbuild/raztint.git
cd raztint
uv sync
```

## Quick Start

```python
from raztint import ok, paint

print(f"{ok()} File saved.")
print(paint("Connection failed.", color="red", icon="err"))

# intent sets color + icon together from one semantic name
print(paint("Deployment complete.", intent="success"))

# redact masks secrets before the string is printed
print(paint("password=1234", intent="debug", redact=True))  # password=****
```

Redaction on its own, without formatting:

```python
from raztint import redact

print(redact("password=supersecret api_key=ghp_abc123"))
# password=**** api_key=****
```

More examples in [Getting Started](docs/getting-started.md).

---

## Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/razbuild/raztint/master/assets/preview.png" alt="RazTint preview: Nerd Font, Unicode, and ASCII icon modes with colored and styled output examples" width="644"/>
</p>
<p align="center"><em>A simulated production log stream 9 secrets detected, 9 secrets redacted, 0 leaked to the terminal.</em></p>

---

## Features

- **Intents**: presets (`success`, `error`, `warning`, `debug`, …) that separate meaning from styling
- **`paint()`**: one call for color, background, styles, and icons
- **Status icons**: `ok()`, `err()`, `warn()`, `info()`, `pending()`, `debug()`, each with the three-tier fallback
- **Redaction**: pattern-based masking (`key=value` pairs like `password=`, `api_key=`, `token=`) applied as part of the formatting call, not a separate logging step; patterns are configurable, see [Security & Redaction](docs/redaction.md)
- **Environment detection**: Nerd Font → Unicode → ASCII, cached; configurable via `NO_COLOR`, `RAZTINT_FORCE_COLOR`
- **Typed**: `py.typed`, full public API type hints
- **Advanced styling**: raw 16-color, 256-color, and True Color support, plus bold, italic, underline, dim, and strikethrough when semantic intents aren't enough.

## Documentation

| Guide                                             | Description                                              |
| -------------------------------------------------- | --------------------------------------------------------- |
| [Getting Started](docs/getting-started.md)         | Functional usage, `paint()`, and the `tint` instance       |
| [API Reference](docs/api-reference.md)             | Colors, styles, icons, and `RazTint` class methods         |
| [Intents](docs/intents.md)                         | Semantic presets for common CLI messages                   |
| [Security & Redaction](docs/redaction.md)          | Masking tokens, credentials, and custom rules               |
| [Icons & Detection](docs/icons-and-detection.md)   | Icon modes and environment/font/color detection logic       |
| [Configuration](docs/configuration.md)             | Environment variables and runtime toggles                   |
| [Development](docs/development.md)                 | Local setup, tests, and linting                             |
| [Tutorial](docs/tutorial.md)                       | Philosophy, detection walk-through, and best practices      |

### Example Scripts

| Script                                             | Description                                  |
| --------------------------------------------------- | ---------------------------------------------- |
| [`examples/basic_usage.py`](examples/basic_usage.py) | Colors, styles, icons, intents, and redaction in one script |
| [`examples/paint_demo.py`](examples/paint_demo.py)   | Every color, style, and icon mode              |
| [`examples/real_world_cli.py`](examples/real_world_cli.py) | Simulated file-processor CLI            |

---

## Design Philosophy

RazTint is built around a single idea:

> [!NOTE]
> Make terminal output consistent, meaningful, and safe by default.

RazTint is not a terminal UI framework. It focuses on high-quality console messaging with:

- ANSI color support
- Semantic logging helpers
- Automatic icon fallbacks
- Secret masking
- Zero external dependencies

By keeping its scope intentionally small, RazTint stays predictable, dependency-free, and easy to drop into existing CLI projects.

---

## Logging Integration Example

RazTint only returns a formatted string, it doesn't hook into `logging` or replace a handler. Pass that string to `print()`, a logger, or anything else that accepts a string.

```python
import logging
from logging import Logger, getLogger

from raztint import paint

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger: Logger = getLogger(__name__)

logger.info(paint("Database migration completed.", intent="success", icon=None))
logger.warning(paint("Disk usage above 90%.", intent="warning", icon=None, styles="dim"))
logger.error(
    paint("Authentication failed for token=abc123", intent="error", redact=True, icon=None)
)
```

## Known Limitations

- Python 3.10+ only.
- Font detection relies on OS tools (`fc-list` on Linux, `system_profiler` on macOS, PowerShell on Windows). Set `RAZTINT_SKIP_SYSTEM_FONT_SCAN=1` in sandboxed environments.
- When `NO_COLOR` is set, all color output is suppressed regardless of other settings.

## Contributing

PRs and issues are welcome. Open an issue first to discuss before starting work on a feature.
See [CONTRIBUTING.md](https://github.com/razbuild/.github/blob/main/CONTRIBUTING.md) for setup and guidelines.

## License

[![License](https://img.shields.io/pypi/l/raztint)](https://github.com/razbuild/raztint/blob/master/LICENSE)

<div align="center">
  <img src="https://raw.githubusercontent.com/razbuild/.github/main/assets/badge.svg" alt="Made by RazBuild" width="160">
</div>