.PHONY: check type

check:
    uv run ruff check .

type:
    uv run mypy .
