.PHONY: build lint format test type-check integration-test ci

TEMP_DIR := $(shell mktemp -d -t tmp.turbopelican.XXXXXXXXXX)
TARGET := $(TEMP_DIR)/mywebsite

build:
	uv sync

lint:
	uv run ruff check

format:
	uv run ruff format --check

test:
	uv run pytest

type-check:
	uv run pyright

integration-test:
	uv run turbopelican init --author "GNU make" "$(TARGET)" -nd
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" pelican content
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" pelican -s publishconf.py content
	@rm -rf "$(TEMP_DIR)"

ci: lint format test type-check integration-test
	@echo "CI run passed"
