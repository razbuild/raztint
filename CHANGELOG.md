# Changelog

**## [0.10.0] - 2026-09-06**
**### Added**
- ****Intent inspection****: Added `intents()` for inspecting available intents and their color, icon, and style configuration.
- ****Terminal preview****: Added `tint.preview()` for inspecting the current terminal environment and `RazTint` configuration.
- ****Transient output****: Added `tint.transient()` for temporary terminal output with support for updating, erasing, and context-manager cleanup.
- ****State-based rendering****: Added `case()` for mapping application states directly to text and semantic intents.
**### Changed**
- Improved type hints for named colors and intent names to provide better IDE autocompletion.
- Tightened validation for color and style-related values.
- Improved consistency between runtime APIs and type stubs.
**### Tests**
- Added test coverage for intent inspection, terminal preview, transient output, and state-based rendering.
**### Docs**
- Added usage examples for the new intent, preview, transient, and case APIs.
**---**


## [0.9.1] - 2026-08-12

### Fixed

- Fixed `ty` type-checking errors caused by registering dynamic color, background, style, and icon methods through the narrower `IconHost` protocol.
- Updated dynamic method registration to use the more specific `FormatTarget` protocol.

---

## [0.9.0] - 2026-07-28

### Changed

- **Breaking**: The semantic intent name `danger` has been renamed to `error`. Replace all `intent="danger"` usages with `intent="error"`.
- **Breaking**: Removed the standalone `rgb()`, `bg_rgb()`, `hex_color()`, `bg_hex_color()`, `color256()`, and `bg_color256()` helper functions. All color formatting is now done exclusively through `paint()` (or `tint.format_text()`).
- **Unified color API**: `paint()` is now the canonical styling function. The `color` and `bg` parameters accept any color value type — named string, hex string (e.g. `"#ff7800"`), RGB tuple (e.g. `(255,120,0)`), or ANSI-256 integer (0-255) — inferred by type. No separate helper functions are needed.
- `BackgroundColorName` type now accepts plain color names (e.g. `"red"`) without the `bg_` prefix, matching the `paint()` `bg` parameter behavior.

### Removed

- Removed public helper functions: `rgb()`, `bg_rgb()`, `hex_color()`, `bg_hex_color()`, `color256()`, `bg_color256()`

### Migration

| Before | After |
|---|---|
| `paint(text, intent="danger")` | `paint(text, intent="error")` |
| `rgb(text, 255, 120, 0)` | `paint(text, color=(255, 120, 0))` |
| `bg_rgb(text, 30, 30, 30)` | `paint(text, bg=(30, 30, 30))` |
| `hex_color(text, "#ff7800")` | `paint(text, color="#ff7800")` |
| `bg_hex_color(text, "#1e1e1e")` | `paint(text, bg="#1e1e1e")` |
| `color256(text, 208)` | `paint(text, color=208)` |
| `bg_color256(text, 236)` | `paint(text, bg=236)` |

---

## [0.8.5] - 2026-07-13

### Fixed
- Fixed `NO_COLOR` and `RAZTINT_NO_COLOR` handling so the presence of either environment variable disables colors even when its value is empty
- Fixed Nerd Font detection to recognize fonts using the `NF` suffix in addition to `Nerd`-based names

### Changed
- Improved Windows Nerd Font detection by also searching for font files with the `NF` suffix

---

## [0.8.4] - 2026-07-07

### Fixed
- Fixed `generic_secret` mask rule not detecting `token` as a sensitive keyword, causing values like `token=abc123` to remain unredacted
- Fixed `generic_secret` rule re-matching and overwriting values already masked by more specific rules (e.g. `github_token`), which previously turned `ghp_****` into `****`, losing the token-type prefix

### Changed
- Updated `generic_secret` pattern's negative lookahead from `(?!\*{4})` to `(?!\S*\*{4})` so it correctly skips values that are partially or fully redacted anywhere in the matched value, not just at the start

---

## [0.8.3] - 2026-07-07

### Added

- Added `benchmarks/` directory for performance benchmarking

### Performance

- Improved environment detection performance
- Optimized font rendering performance

### Tests

- Added new test coverage
- Added `test_env.py`

### Docs

- Improved project documentation
- Enhanced README with clearer explanations
- Updated and expanded usage examples

---

## [0.8.2] - 2026-06-28

### Fixed

- Normalized type hint imports in public API module (`__init__.pyi`)
- Improved type hint consistency by simplifying and deduplicating `data.types` imports
- Fixed minor static type-checking inconsistencies affecting IDEs and type checkers

### Internal

- Refactored type annotation style without changing runtime behavior

---

## [0.8.1] - 2026-06-25

### Fixed

- Fixed missing exports in `__all__` by adding `debug` and `pending` to public API surface

### Changed

- Decoupled type checking configuration by moving `ty` configuration to standalone `ty.toml`
- Decoupled linting configuration by externalizing `ruff` configuration
- Simplified and cleaned up `pyproject.toml` for better maintainability
- Updated dependency lockfile (`uv.lock`) to reflect latest environment state

### Internal

- Improved project tooling structure without affecting runtime behavior

---

## [0.8.0] - 2026-06-13

### Added

- Added True Color and 256-color support via `rgb`, `hex_color`, and `color256` APIs
- Introduced new icons for `Pending` and `debug` states

### Tests

- Added test coverage for True Color and 256-color functionality

### Docs

- Added `examples/` directory with usage samples
- Added tutorial documentation to improve onboarding
- Enhanced README with clearer structure
- Added `preview.png` and updated README preview section

---

## [0.7.1] - 2026-06-09

### Fixed

- Refined `RazTint` icon mode initialization to resolve environment detection through an injected Nerd Font detector, reducing import coupling and making the detection path easier to test.
- Stabilized the module-level icon helper test by restoring the global `tint` state after mutating icon and color settings.

### Docs

- Clarified icon mode behavior across Nerd Font, standard Unicode, and ASCII fallbacks in the README and detection docs.
- Documented `paint(..., reset=False)` behavior more precisely and clarified that icons are still emitted when color is disabled.
- Updated documentation links and wording around redaction, configuration, and typing/stub locations.

---

## [0.7.0] - 2026-06-07

### Added

- **Modular package layout** — split monolithic modules into focused packages: `core`, `data`, `detect`, `formatting`, `icons`, and `security`.
- **Semantic intents** — `paint(..., intent="success")` and presets for `danger`, `warning`, `info`, `pending`, and `debug` via `INTENTS` / `IntentConfig`.
- **Secret redaction** — `redact()` and `paint(..., redact=True)` with built-in `DEFAULT_RULES` for tokens, JWTs, credentials, and common secrets; custom `MaskRule` support.
- **Typed public API** — `ColorName`, `StyleName`, `IconName`, `IconMode`, `IntentName` literals, `py.typed` marker, and `.pyi` stubs for IDE autocompletion.
- **`paint()` enhancements** — intent defaults, redaction, and `UnsetType` sentinel for optional icon inheritance.
- **`core/protocols.py`** — shared Protocol types for formatting, icons, and dynamic method registration.
- **Documentation site** — new `docs/` directory with guides (getting started, API, intents, security, icons, configuration, development); README trimmed to a landing page.
- **128 unit tests** organized under `tests/unit/` mirroring the package structure.

### Changed

- **`paint()`** remains the module-level alias for `tint.format_text()`; implementation moved to `formatting/paint.py`.
- **README** simplified; detailed tutorials and API reference moved to `docs/`.
- **Development workflow** standardized on **uv** only (`uv sync --group dev`, `uv run …`).
- **CI** aligned with uv: single `dev` dependency group, ruff + ty + pytest/coverage across Python 3.10–3.14 and Linux/macOS/Windows.
- **Removed Black** from dev dependencies and CI; formatting handled by `ruff format`.
- **`pyproject.toml`** — fixed classifier placement, added `[tool.uv.build-backend]` with `module-root = "src"`, synced `dependency-groups` with CI.

### Removed

- Legacy flat modules: `colors.py`, `core.py`, `styles.py`, `icons.py`, `env_detect.py`, `font_detect.py`.
- Black formatter configuration and CI step.

---

## [0.6.0] - 2026-05-13

### Added
- `format_text()` method for applying foreground color, background color, and multiple text styles in a single call.
- New tests for `format_text()` covering edge cases, validation, and environment toggles.

### Changed
- Migrated project tooling from pip to uv, including CI configuration.
- Updated README with usage examples for the new `format_text()` helper.

---

## [0.5.0] - 2026-05-12

### Added
- feat: support for ANSI background colors
- test: add unit tests for background color parsing

### Docs
- docs: update README with new color examples

---

## [0.4.1] - 2026-05-12

### Fixed
- `__version__` now correctly reflects the installed version using `importlib.metadata`.  
  Previously, it was hardcoded to `0.3.0`, causing confusion with the actual package version.

---

## [0.4.0] - 2026-05-11

### Added
- **Text style support**: New functions `bold`, `dim`, `italic`, `underline`, and `strikethrough` allow applying text styles without breaking existing ANSI colors. Each style uses its own reset code to preserve color when removed.
- Comprehensive test coverage for all new style functions.

### Docs
- Full documentation for text styles in README and API reference.

---

## [0.3.0] - 2026-05-04

### Added
- Full ANSI 16-color support: added 7 bright color variants (bright_red, bright_green, bright_yellow, bright_blue, bright_magenta, bright_cyan, bright_white).
- New singleton import (`tint`) now documented explicitly in README.

### Changed / Refactored
- Unified color method naming to snake_case for bright variants (e.g., bright_red) in line with existing naming convention.
- Updated Python support to include 3.14 and adjusted classifiers.

### Docs
- Comprehensive README overhaul: bright colors table, singleton clarification, PyPI badge fix, removed incorrect pipx instructions, improved structure.

---

## [0.2.0] - 2026-02-23

### Added
- Expanded test suite for environment and nerd font detection across platforms.
- Optional debug logging and configuration flags for font scanning behavior.

### Changed / Refactored
- Broadened supported Python versions to 3.9–3.13 and updated classifiers.
- Improved robustness and performance of color, icon, and nerd font detection.

### Docs
- Updated README with new configuration flags, performance/debugging notes, and development workflow.
- Documented release changes for 0.2.0 in the changelog.

### CI
- Updated GitHub Actions to install extras-based dependencies and test against multiple Python versions.

---

## [0.1.1] - 2025-12-20

### Added
- Modular structure for colors and icons to improve maintainability.
- New icons and improved visual representation.

### Changed / Refactored
- Refactored code for better readability and organization.
- Updated icon rendering and layout.

### Removed
- Redundant code from the main module after modularization.

### Docs
- Documentation updated to match the new structure and visuals.

### CI
- Continuous integration updated and synchronized with the latest code changes.
