default:
	./manage.py runserver

test:
	pytest --cov --cov-report=term-missing
