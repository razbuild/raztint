# Development

[← Documentation index](index.md)

---

## Local setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/razbuild/raztint.git
cd raztint
uv sync --group dev
```

---

## Running tests

```bash
uv run pytest
```

Skip slow tests:

```bash
uv run pytest -m "not slow"
```

With coverage:

```bash
uv run coverage run -m pytest
uv run coverage report -m
```

---

## Linting and type checking

Kept in sync with CI:

```bash
uv run ruff check src tests
uv run ty check src
```

Format code:

```bash
uv run ruff format src tests
```

---

## Project structure

```
src/raztint/
├── core/          # RazTint instance, ANSI application, builder
├── data/          # Colors, styles, intents, typed literals
├── detect/        # TTY, Windows VT, font detection, debug logging
├── formatting/    # paint() / format_text(), code resolution
├── icons/         # Icon registry and mode resolution
└── security/      # Secret redaction
tests/
├── unit/          # Module-level tests mirroring package layout
└── conftest.py
```

---

## Typing

The package ships with `py.typed` and a top-level stub file `src/raztint/__init__.pyi`. Public `Literal` types live in `raztint.data.types` and are re-exported from `raztint`.

```bash
uv run ty check src
```

---

## Contributing

1. Fork the repository and create a feature branch.
2. Add or update tests for behavior changes.
3. Run `uv run ruff check src tests`, `uv run ty check src`, and `uv run pytest`.
4. Open a pull request with a clear description of the change.

Report bugs and feature requests via [GitHub Issues](https://github.com/razbuild/raztint/issues).

---

## See also

- [Configuration](configuration.md) — environment variables used in CI
- [API Reference](api-reference.md) — public API surface
