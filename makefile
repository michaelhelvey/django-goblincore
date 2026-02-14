default:
	./manage.py runserver

build:
	pnpm exec vite build

test:
	pytest -v --cov --cov-report=term-missing
	pnpm test --run

format:
	uv run ruff format .
	uv run ruff check --select I --fix .
	pnpm run format

lint:
	uv run ruff check .
	pnpm run lint

lint-fix:
	uv run ruff check --fix .
	uv run ruff check --select I --fix .
	pnpm run lint --fix

setup:
	uv sync
	pnpm install
	pnpm exec vite build
	cp .env.example .env
	source ./.venv/bin/activate
	./manage.py migrate
