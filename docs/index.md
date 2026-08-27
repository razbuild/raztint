# RazTint Documentation

RazTint is a zero-dependency Python library for clear, semantic command-line output. It formats text with ANSI colors and icons, and can redact common secrets before a string is displayed or logged.

## Start here

1. Install RazTint and print your first message in [Getting Started](getting-started.md).
2. Use [Intents](intents.md) for consistent success, error, warning, and diagnostic messages.
3. Read [Security and Redaction](redaction.md) before displaying potentially sensitive values.

## Guides

| Guide | Use it when you need to... |
|---|---|
| [Getting Started](getting-started.md) | Install RazTint, format common messages, and choose between the shared instance and your own instance. |
| [Intents](intents.md) | Apply the built-in semantic presets or override one part of a preset. |
| [Security and Redaction](redaction.md) | Mask built-in secret patterns or define custom masking rules. |
| [Icons and Detection](icons-and-detection.md) | Understand icon fallbacks, color detection, and terminal capabilities. |
| [Configuration](configuration.md) | Control detection with environment variables or at runtime. |

## Reference

| Reference | Contents |
|---|---|
| [API Reference](api-reference.md) | Public functions, `RazTint`, accepted color values, and public types. |
| [Development](development.md) | Local setup, tests, quality checks, and project layout. |

## Examples

- [`examples/showcase.py`](../examples/showcase.py) demonstrates colors, styles, icons, intents, and redaction.
- [`examples/redaction_demo.py`](../examples/redaction_demo.py) demonstrates built-in and custom redaction rules.
- [`examples/file_processor.py.py`](../examples/file_processor.py.py) is a simulated command-line workflow.

Most applications should import from `raztint`. The package submodules are intended for advanced use.
