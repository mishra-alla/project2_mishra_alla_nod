install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	@echo "Installing package with Python 3.12..."
	python3.12 -m pip install --user dist/project2_mishra_nod-0.1.0-py3-none-any.whl

lint:
	poetry run ruff check .

test-run:
	@echo "Testing project..."
	poetry run project
