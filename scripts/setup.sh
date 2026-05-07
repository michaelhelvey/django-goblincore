#!/usr/bin/env bash

set -eou pipefail

uv sync
pnpm install --prefer-offline
pnpm exec vite build
cp .env.example .env
source ./.venv/bin/activate
./manage.py migrate
python ./scripts/create-super-user.py