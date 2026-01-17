# Agent Guidelines for Goblincore

This file contains instructions for AI coding agents working in this repository.

## Project Overview

- **Type:** Modern Django 6.0+ fullstack web application
- **Language:** Python 3.14+
- **Framework:** Django with async/ASGI support
- **Package Manager:** `uv` (modern Python package manager)
- **Database:** SQLite (development), configurable for production
- **Server:** Uvicorn (dev), Gunicorn + Uvicorn Worker (prod)

## Build, Test, and Development Commands

### Running the Application

```bash
# Development server with hot reload (default)
make
# or explicitly:
make default
# or directly:
python -m uvicorn goblincore.asgi:application --reload

# Production server
make prod
# or directly:
python -m gunicorn goblincore.asgi:application -k uvicorn_worker.UvicornWorker
```

### Django Management Commands

```bash
# Run Django management commands
python manage.py <command>

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser
```

### Testing

This project uses pytest with pytest-django for testing.

```bash
# Run all tests with coverage
make test

# Run tests without coverage
pytest

# Run specific test file
pytest app/tests/test_example.py

# Run specific test function
pytest app/tests/test_example.py::test_example

# Run tests matching a pattern
pytest -k "test_async"

# Run with verbose output
pytest -vv

# Run and show coverage in terminal
pytest --cov --cov-report=term-missing

# Keep test database between runs (faster)
pytest --reuse-db

# Create fresh test database
pytest --create-db

# Run async tests
pytest -k "async"
```

### Package Management

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Update dependencies
uv lock --upgrade
```

## Code Style Guidelines

### General Principles

- **Async-First:** Prefer async views and functions for I/O operations
- **Django 6.0+ Standards:** Follow modern Django conventions
- **Simplicity:** Keep code minimal and readable
- **Type Hints:** Do not use static type hints
