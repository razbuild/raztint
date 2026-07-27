# RazTint Documentation

For installation and quick start, see the [README](../README.md).

## Guides

| Guide | Description |
|---|---|
| [Getting Started](getting-started.md) | `paint()` parameters, color types, `tint` singleton, class-based usage |
| [API Reference](api-reference.md) | All functions, parameters, and type aliases |
| [Intents](intents.md) | Semantic preset registry and override behavior |
| [Security & Redaction](redaction.md) | Built-in mask rules and custom patterns |
| [Icons & Detection](icons-and-detection.md) | Icon modes and environment detection logic |
| [Configuration](configuration.md) | Environment variables and runtime toggles |
| [Development](development.md) | Setup, tests, linting, and contributing |

## Package layout

| Module | Purpose |
|---|---|
| `raztint.core` | `RazTint` instance, ANSI helpers, method registration |
| `raztint.data` | Color/style registries, intent presets, typed literals |
| `raztint.detect` | TTY, Windows VT, and Nerd Font detection |
| `raztint.formatting` | `paint()` / `format_text()` implementation |
| `raztint.icons` | Icon registry and mode resolution |
| `raztint.security` | Regex-based secret redaction |

Most users only need top-level imports from `raztint`; subpackages are for advanced use.