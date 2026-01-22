# Goblincore

An opinionated starting point for modern Django development.

## Project Overview

- Language: Python 3.14:
- Framework: Django 6.0+
- Package Manager (python): `uv`
- Package Manager (javascript): `pnpm`
- JS ecosystem: `vite` (bundler / transpiler), `vitest` (js testing)

## Commands

- Start application: `./manage.py runserver` or `make`
- Test: `pytest` or `make test`
- Test (specific file): `pytest app/tests/test_user.py`
- Test (specific test function): `pytest app/tests/test_user.py::test_create_user_with_valid_data`
- Add a package: `uv add <package>`
- Format code: `make format` (runs ruff formatter)
- Lint code: `make lint` (runs ruff linter)
- Lint and fix: `make lint-fix` (runs ruff linter with auto-fix)

You can potentially discover other commands by examining the `Makefile` or by running
`./manage.py --help`.

## Guidelines

- Write functional-style pytest tests. Do not write class based tests.
- Aim for 100% test coverage, but do not overtest a feature. Aim to achieve coverage with a few
  simple tests that validate core functionality.
- Do not use Python type hints. Ignore type hinting errors from the LSP. This project does not use
  static typing.
