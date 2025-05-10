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
	# Run normally.
	uv run turbopelican init --author "GNU make" "$(TARGET)" -nd
	VIRTUAL_ENV="$(TARGET)/.venv" uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" --no-sync pelican content
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" --no-sync pelican -s publishconf.py content

	# Run with a minimal install.
	@rm -rf "$(TARGET)"
	uv run turbopelican init --author "GNU make" "$(TARGET)" -nd --minimal-install
	VIRTUAL_ENV="$(TARGET)/.venv" uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" --no-sync pelican content
	VIRTUAL_ENV="$(TARGET)/.venv" uv run --directory "$(TARGET)" --no-sync pelican -s publishconf.py content

	# Clean up.
	@rm -rf "$(TEMP_DIR)"

ci: lint format test type-check integration-test
	@echo "CI run passed"
