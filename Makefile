install:
	pip install -e .

test:
	rm -r .pytest_cache || true
	black .
	python -m pytest --pylint --pylint-rcfile=./pylintrc --mypy --mypy-ignore-missing-imports --cov=mkdocs_exclude_search/ --durations=3
	coverage-badge -f -o coverage.svg

serve-python:
	python /Users/christoph.rieke/.virtualenvs/mkdocs-exclude-search/lib/python3.8/site-packages/mkdocs/__main__.py serve

debug: #breakpoint, In python Console, attach debugger. The magiccomand requires ipython & -e installation of plugin.
	%run /Users/christoph.rieke/.virtualenvs/mkdocs-exclude-search/lib/python3.8/site-packages/mkdocs/__main__.py serve
