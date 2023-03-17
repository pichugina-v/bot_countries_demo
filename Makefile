install:
	poetry install

test:
	poetry run pytest -vv

hooks:
	poetry run pre-commit run --all-files

run-bot:
	poetry run python aiogram_layer/main.py
