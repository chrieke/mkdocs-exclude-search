install:  # Requires pip >= 25.1 for --group.
	pip install -e . --group dev --group docs

lint:
	ruff format .
	ruff check --fix .
	mypy

test: lint
	python -m pytest
	coverage-badge -f -o coverage.svg

serve:  # Serve the docs/ example site with the plugin (requires `make install`).
	python -m mkdocs serve
