# RazTint Documentation

Welcome to the RazTint documentation. The [README](../README.md) covers installation and a minimal quick start; the guides below go into detail.

## Guides

| Guide | What you'll learn |
|---|---|
| [Getting Started](getting-started.md) | Import styles, `paint()`, and class-based usage |
| [API Reference](api-reference.md) | Every public function, parameter, and class attribute |
| [Intents](intents.md) | Semantic message presets (`success`, `danger`, …) |
| [Security & Redaction](redaction.md) | `redact()` and built-in secret masking rules |
| [Icons & Detection](icons-and-detection.md) | Nerd Font / Unicode / ASCII modes and how they are chosen |
| [Configuration](configuration.md) | Environment variables, color detection, debugging |
| [Development](development.md) | Contributing, running tests, and CI checks |

## Package layout

RazTint is organized into focused modules:

| Module | Purpose |
|---|---|
| `raztint.core` | `RazTint` instance, ANSI helpers, and icon method registration |
| `raztint.data` | Color/style registries, intent presets, typed literals |
| `raztint.detect` | TTY, Windows VT, and Nerd Font detection |
| `raztint.formatting` | `paint()` / `format_text()` implementation |
| `raztint.icons` | Icon registry and mode resolution |
| `raztint.security` | Regex-based secret redaction |

Most users only need the top-level imports from `raztint`; the subpackages are available for advanced or internal use.
