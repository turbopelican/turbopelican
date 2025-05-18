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

start_section := $(shell awk "/^\#\# Version / {print NR; exit }" CHANGELOG.md)
next_section = $(shell awk "/^\#\# Version /{count++} count == 2 {print NR; exit}" CHANGELOG.md)
end_section = $(shell expr $(next_section) - 2)

found_version_line = $(shell sed -n '$(start_section)p' CHANGELOG.md)
current_version = $(shell git describe --tags --abbrev=0)
expected_version_line = \#\# Version $(patsubst v%,%,$(current_version))

ifeq ($(found_version_line),$(expected_version_line))
	run_release_notes_command = sed -n '$(start_section),$(end_section)p' CHANGELOG.md > release-notes.md
else
	run_release_notes_command = @echo "CHANGELOG.md and tag mismatch."; exit 1
endif

release-notes.md: CHANGELOG.md
	@echo "Generating release notes."
	$(run_release_notes_command)
