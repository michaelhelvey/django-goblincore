default:
	./manage.py runserver

test:
	pytest --cov --cov-report=term-missing

format:
	uv run ruff format .
	pnpm run format

lint:
	uv run ruff check .
	pnpm run lint

lint-fix:
	uv run ruff check --fix .
	pnpm run lint --fix
