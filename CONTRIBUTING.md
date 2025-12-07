# Contributing to RazTint

Thank you for your interest in contributing to RazTint! We welcome all contributions, big or small.

## How to Report Issues

If you find a bug or have a feature request, please use the provided templates in the [Issues tab](https://github.com/razbuild/raztint/issues):
- Use the **Bug Report** form for errors and unexpected behavior.
- Use the **Feature Request** template for new ideas and enhancements.

When reporting bugs, please include:
- RazTint version
- Python version
- Operating system
- Terminal application
- Nerd Font status (if relevant)
- Steps to reproduce
- Expected vs actual behavior

## Development Setup

To set up your local environment for development:

1. **Fork** the repository and clone it locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/raztint.git
   cd raztint
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the project in editable mode with development dependencies:
   ```bash
   pip install -e .[dev]
   ```
   
   This installs:
   - `pytest` - Testing framework
   - `ruff` - Linter
   - `black` - Code formatter
   - `mypy` - Type checker
   - `coverage` - Test coverage tool

## Running Tests and Quality Checks

Before submitting a Pull Request, please ensure all quality checks pass:

### Run Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=src/raztint --cov-report=html --cov-report=term
```

This will:
- Run all tests
- Generate coverage report in terminal
- Create an HTML report in `htmlcov/` directory (open `htmlcov/index.html` in browser)

### Run Linting
```bash
ruff check .
```

### Format Code
```bash
black .
```

### Run Type Checking
```bash
mypy .
```

### Run All Checks
You can run all checks in sequence:
```bash
ruff check . && black --check . && mypy . && pytest --cov=src/raztint --cov-report=term
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Keep functions focused and small
- Add docstrings for public APIs
- Write tests for new features and bug fixes

## Submitting a Pull Request

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b fix/my-issue
   # or
   git checkout -b feat/new-feature
   ```

2. **Make your changes** and commit them with descriptive messages:
   ```bash
   git add .
   git commit -m "fix: description of what was fixed"
   ```

3. **Push your branch** to your fork:
   ```bash
   git push origin fix/my-issue
   ```

4. **Open a Pull Request** against the `master` branch of the original RazTint repository. 
   - Fill out the Pull Request Template completely
   - Link to any related issues
   - Ensure all CI checks pass

## Commit Message Guidelines

Use clear, descriptive commit messages:
- `fix:` for bug fixes
- `feat:` for new features
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for test additions/changes
- `chore:` for maintenance tasks

Example: `fix: correct Nerd Font detection on Windows`

## Testing Guidelines

- Write tests for all new features
- Ensure existing tests continue to pass
- Test on multiple platforms if possible (Linux, macOS, Windows)
- Test with and without Nerd Fonts
- Test color detection in various scenarios

## Questions?

If you have questions about contributing, feel free to open an issue with the `question` label.
