
.PHONY: fmt
fmt:
	uv run toml-sort -i pyproject.toml
	uv run ruff check --fix
	uv run ruff format

.PHONY: typecheck
typecheck:
	uv run mypy
