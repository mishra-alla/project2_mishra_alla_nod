install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	pip install dist/*.whl

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

test:
	@echo "=== ТЕСТИРОВАНИЕ ==="
	@rm -f db_meta.json
	@echo "1. Создание таблицы..."
	@echo "create_table users name:str age:int" | poetry run python -m src.primitive_db.main
	@echo ""
	@echo "2. Проверка файла..."
	@ls -la db_meta.json 2>/dev/null && echo "Файл создан" || echo "Файл не создан"
	@echo ""
	@echo "3. Список таблиц..."
	@echo "list_tables" | poetry run python -m src.primitive_db.main

clean:
	rm -rf dist/
	rm -rf .ruff_cache/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf src/primitive_db/__pycache__/
	rm -f db_meta.json

.PHONY: install project build publish package-install lint format test clean
