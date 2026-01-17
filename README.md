# goblincore

An opinionated template for building modern fullstack applications with Django.

## Features

- ASGI support by default, realtime enabled with Django Channels. (Note: _not_
  async views by default, as the Django ORM integration for these are still
  limited with use with Django generic class-based views).
- Simple static file support with ServeStatic (an async fork of Whitenoise)
- Custom user model and user model manager included by default
- REST framework included by default

## TODO

- do this (https://vite.dev/guide/backend-integration#backend-integration) as
  part of our middleware or something somehow
