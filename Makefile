clean:
	rm -rf .venv .pytest_cache

init: clean
	pip install poetry
	poetry install

test:
	poetry run python -m pytest

# CI / CD
ci-test:
	poetry run python -m pytest