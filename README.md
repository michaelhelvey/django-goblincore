<p align="center">
  <img src="./assets/the-goblin-market-hilda-koe.jpg" alt="Goblin painting" width="200" />
</p>

<h1 align="center">Django-Goblincore</h1>

<p align="center">
  <i>A opinionated starting point for modern Django development</i>
</p>

## Features

- Functional testing with Pytest instead of the default Django base classes
- Django best practices (or at least opinions): A custom user model, emails instead of usernames,
  ServeStatic (Whitenoise) for static files, standard base template with messages framework support,
  etc.
- Common packages already installed: django-filter for auto-generating filters for your list views,
  django rest framework for your APIs, django-channels for websockets and other realtime uses,
  `daphne` for ASGI, django-htmx for forms and other dynamic content, etc.
- Deep integration with the modern JS ecosystem: `./manage.py runserver` starts Vite for you, and
  you get all the nice features of Vite that you might be used to from javascript frameworks. If you
  want to add a React app to your Django application, it's as simple as adding the React Vite
  plugin.
- Styling with Tailwindcss and DaisyUI
- Opinionated linting & formatting for both Python and Javascript with Ruff & VitePlus.

## Getting Started

Before getting started, make sure you have the following installed:

- Python 3.14+
- Node.js (latest LTS recommended)
- pnpm 11+ (or it will be installed automatically via packageManager field if you have corepack
  enabled)
- uv package manager ([install instructions](https://docs.astral.sh/uv/))

Then just run `pnpm local-setup` to install dependencies and initalize your environment, then run
`./manage.py runserver` to start your app at `http://localhost:8000`
