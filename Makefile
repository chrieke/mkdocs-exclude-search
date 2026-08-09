install:
	pip install -e .
	pip install -r requirements_dev.txt

test:
	rm -r .pytest_cache || true
	black .
	python -m pytest --pylint --pylint-rcfile=./pylintrc --mypy --mypy-ignore-missing-imports --cov=mkdocs_exclude_search/ --durations=3 --ignore=./test-repos/
	coverage-badge -f -o coverage.svg

serve:  # Serve the docs/ example site with the plugin (requires `make install`).
	python -m mkdocs serve
