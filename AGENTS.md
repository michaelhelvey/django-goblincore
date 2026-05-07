# Goblincore

An opinionated starting point for modern Django development.

## Project Overview

- Language: Python 3.14:
- Framework: Django 6.0+
- Package Manager (python): `uv`
- Package Manager (javascript): `pnpm`
- JS ecosystem: `vite` (bundler / transpiler), `vitest` (js testing). Both use the `vite-plus`
  unified toolchain.
- CSS styling: tailwindcss with daisyui (docs: https://daisyui.com/llms.txt)

## Commands

_Note: all python commands assume you have the virtual env activated_

- Start application: `./manage.py runserver` or `make`
- Test: `pytest` or `pnpm test`
- Test (specific file): `pytest app/tests/test_user.py`
- Test (specific test function): `pytest app/tests/test_user.py::test_create_user_with_valid_data`
- Add a package: `uv add <package>`
- Format code: `pnpm format` (runs ruff and vp formatter)
- Lint code: `pnpm lint` (runs ruff and vp linter)

## Guidelines

- Write functional-style pytest tests. Do not write class based tests.
- Aim for 100% test coverage, but do not overtest a feature. Aim to achieve coverage with a few
  simple tests that validate core functionality.
- Do not use Python type hints. Ignore type hinting errors from the LSP. This project does not use
  static typing.
