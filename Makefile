clean:
	rm -rf .venv .pytest_cache

init: clean
	pip install poetry
	poetry install
	pre-commit install

test:
	poetry run python -m pytest

# CI / CD
ci-setup:
	pip install poetry
	poetry install

ci-tests:
	poetry run python -m pytest