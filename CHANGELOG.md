# Changelog

## Version 0.3.3

### Bug fixes

- In the version prior, attempting to build a static site using the
  settings for publication would result in an `ImportError` being raised, due
  to `publishconf.py` not containing its parent directory in the `PYTHONPATH`.
  Now `PYTHONPATH` is updated so that it imports `pelicanconf.py`
  successfully.
- In the version prior, attempting to build a static site using the
  settings for publication would (were it not for the bug above), result in
  `publishconf.py` attempting to access non-existent TOML, causing an error.
  Now placing the TOML inside by default.
- In the version prior, attempting to build a static site using the
  settings for publication would (were it not for the bugs above), result in
  missing variables, causing Pelican to raise an error when attempting to
  overwrite an existing `output/index.html` file. Now importing the required
  variables from `pelicanconf.py`.
- In the version prior, GitHub Actions incorrectly built the static site using
  the default configuration, which is not supposed to be used for publication.
  Now uses the appropriate configuration.
- Fixing spelling mistake in documentation.

### Other changes

- Both `pelicanconf.py` and `publishconf.py` should now contain complete
  `__all__` lists.
- Now including a run of `turbopelican` in the continuous integration, to be
  checked by GitHub Actions.
- Now providing a `Makefile` to both set up the repository and to perform the
  same tasks that are used in the continuous integration.

## Version 0.3.2

### Bug fixes

- In the version prior, a `ConfigurationError` was inconsistently raised when
  an incorrect default language is provided. Now making consistent.
- In the version prior, if no suggestion could be made for the site URL, then
  irrespective of the site URL provided via standard input, an error was
  raised. Now the user is able to input a valid site URL successfully.

### Other changes

- Inverting badge colours. Badge should now be higher-contrast.
- Making Python modules private, so less likely to be imported.
- Removing pydantic as a dependency. Should make the tool faster to run.
- Using `pyright` exclusively for static type checking. The Neovim
  configuration was previously incorrect, so now users of Neovim should be
  able to see `pyright` warnings.
- Disabling `missing-trailing-comma` rule, which is not supposed to be used in
  conjunction with the formatter.
- Updating all dependencies. Includes bumping `pyright` to v1.1.397 and `ruff`
  to v0.11.6.
- Using hatch-vcs to determine package versioning.

## Version 0.3.1

### Bug fixes

- In the version prior, the default git branch could be master, depending on
  the version/configuration of `git`. This did not accord with `README.md`.
  Now the default branch is always `main`.

### Other changes

- Improving `README.md` to show an annotated image demonstrating how to
  configure a GitHub repository to deploy to GitHub Pages.
- Using enums `Verbosity`, `InputMode` and `HandleDefaultsMode` rather than
  booleans for configuration.
- Using `ConfigurationError` for errors raised by incorrect CLI input, rather
  than `ValueError`.
- Using `FileNotFoundError` for when the directory for the repository passed
  into `turbopelican` does not have an extant parent.
- Removing unreachable code.
- Functions `get_raw_args_without_subcommand` and `get_raw_args` now can take
  argument overrides, useful for testing.
- Implementing unit tests.
- Ensuring `uv sync` is run after `pyproject.toml` is updated.

## Version 0.3.0

### Deprecated features

- Running `turbopelican` without a subcommand is now deprecated.

### Features

- Introducing `--no-input` flag. This should cause `turbopelican` to raise an
  error if the command the user ran is insufficient without receiving further
  arguments via standard input.
- Introducing `--use-defaults` flag. This causes `turbopelican` to search for
  the provided configuration settings in the following order:
  1. Command-line arguments
  2. Default arguments
  3. Standard input (unless using `--no-input` flag)
- Removing links and social media from deployed configuration files.
- `turbopelican.toml` should now contain all configuration that was previously
  contained in `pelicanconf.py` and `publishconf.py`.
- A subparser for `turbopelican` allows initializing repositories via the
  `turbopelican init` command.
- Putting contents in the `README.md` file in deployed repositories.

### Other changes

- Creating profile picture for organization.
- Shifting repository to `turbopelican` GitHub organization. No longer hosted
  by `clockback`.
- Writing summary of tool's purpose in `README.md`.

## Version 0.2.1

### Bug fixes

- In the version prior, users were given the GitHub workflow
  `run-quality-gates.yml`, despite the file not containing quality gates.
  Renamed to `turbopelican.yml`.

### Other changes

- Correcting logo in `README.md` for universal viewing on media like PyPI.
- Condensing logo SVG size.
- Including turbopelican badge in `README.md`.
- Expanding the `README.md` instructions with more comprehensive instructions.
- Adding "Typing :: Typed" classifier to project metadata.

## Version 0.2.0

### Features

- Including custom theme for more intuitive start to creating website from
  scratch. This includes corresponding changes to the content and settings.
- New `--quiet` flag allows the user to suppress output, save for input
  prompts.

### Other changes

- Adding logo to `README.md`.
- Improving readability of `README.md`.
- Hiding the `.env` file. This contains the token for publishing.
- Fixing typos in `src/turbopelican/args.py`.

## Version 0.1.1

### Bug fixes

- In the version prior, if someone ran the development server, the assets
  (e.g. CSS) would be incorrectly loaded.

### Other changes

- Correcting grammar in `README.md`.
- Adding keywords to project metadata.
- Adding classifiers to project metadata.
- Adding URL to `CHANGELOG.md` in project metadata.

## Version 0.1.0

- Creating CLI tool for creating Pelican static-site pages for GitHub Pages.
