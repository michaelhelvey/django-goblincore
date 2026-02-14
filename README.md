# Goblincore

An opinionated starting point for modern Django development.

## Features

- Functional testing with Pytest instead of the default Django base classes
- Django best practices (or at least opinions): A custom user model, emails instead of usernames,
  ServeStatic (Whitenoise) for static files, standard base template with messages framework support,
  etc.
- Common packages already installed: django-filter for auto-generating filters for your list views,
  django rest framework for your APIs, django-channels for websockets and other realtime uses,
  `daphne` for ASGI, etc.
- Deep integration with the modern JS ecosystem: `./manage.py runserver` starts Vite for you, and
  you get all the nice features of Vite that you might be used to from javascript frameworks. If you
  want to add a React app to your Django application, it's as simple as adding the React Vite
  plugin.
- Styling with Tailwindcss and DaisyUI
- Opinionated linting & formatting for both Python and Javascript with Ruff, Eslint, and Prettier

## Getting Started

Before getting started, make sure you have the following installed:

- Python 3.14+
- Node.js (latest LTS recommended)
- pnpm 10+ (or it will be installed automatically via packageManager field if you have corepack
  enabled)
- uv package manager ([install instructions](https://docs.astral.sh/uv/))

If you use [mise](https://github.com/jdx/mise), you can install all of this by just running
`mise install` and `uv python install 3.14.2` (or your version of choice).

Then just run `make setup` to install dependencies and initalize your environment.

## Common Commands

Start the application by running `./manage.py runserver` and visiting `http://localhost:8000`.

Create yourself a user by running `./manage.py createsuperuser`. It's a standard Django application,
so you'll mostly just be interacting with the standard `./manage.py` stuff.
