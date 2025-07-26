.PHONY: build lint format test type-check integration-test ci

TEMP_DIR := $(shell mktemp -d -t tmp.turbopelican.XXXXXXXXXX)
TARGET := $(TEMP_DIR)/mywebsite
VENV := VIRTUAL_ENV="$(TARGET)/.venv"
CONFIG_TYPE := TURBOPELICAN_CONFIG_TYPE=PUBLISH

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
	# Run `turbopelican init` normally.
	uv run turbopelican init --author "GNU make" "$(TARGET)" -nd
	$(VENV) uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	$(VENV) uv run --directory "$(TARGET)" --no-sync pelican content
	$(VENV) $(CONFIG_TYPE) uv run --directory "$(TARGET)" --no-sync pelican content

	# Run `turbopelican init` with a minimal install.
	@rm -rf "$(TARGET)"
	uv run turbopelican init --author "GNU make" "$(TARGET)" -nd --minimal-install
	$(VENV) uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	$(VENV) uv run --directory "$(TARGET)" --no-sync pelican content
	$(VENV) $(CONFIG_TYPE) uv run --directory "$(TARGET)" --no-sync pelican content

	# Run `turbopelican adorn` normally.
	@rm -rf "$(TARGET)"
	uv init "$(TARGET)"
	git -C "$(TARGET)" remote add origin "git@github.com:myuser/myrepo"
	uv run turbopelican adorn --author "GNU make" "$(TARGET)" -nd
	$(VENV) uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	$(VENV) uv run --directory "$(TARGET)" --no-sync pelican content
	$(VENV) $(CONFIG_TYPE) uv run --directory "$(TARGET)" --no-sync pelican content

	# Run `turbopelican adorn` with a minimal install.
	@rm -rf "$(TARGET)"
	uv init "$(TARGET)"
	git -C "$(TARGET)" remote add origin "git@github.com:myuser/myrepo"
	uv run turbopelican adorn --author "GNU make" "$(TARGET)" -nd --minimal-install
	$(VENV) uv pip --directory "$(TARGET)" install -qe "$(shell pwd)"
	$(VENV) uv run --directory "$(TARGET)" --no-sync pelican content
	$(VENV) $(CONFIG_TYPE) uv run --directory "$(TARGET)" --no-sync pelican content

	# Clean up.
	@rm -rf "$(TEMP_DIR)"

ci: lint format test type-check integration-test
	@echo "CI run passed"

release-notes.md: CHANGELOG.md
	@echo "Generating release notes."
	sed -n '/^## Version /{h;:a;n;/^## Version /!{H;ba};x;s/\n[^\n]*$$//p;q}' CHANGELOG.md > release-notes.md
