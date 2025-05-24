# Changelog

## Version 0.4.3

### Bug fixes

- In version 0.4.0, Turbopelican would parse `links` and `social` as lists of
  lists, rather than lists of two-element tuples. Now they are parsed as lists
  of two-element tuples.
- In version 0.4.0, a minimal Turbopelican project's `pelicanconf.py` would
  expect to receive arrays of key-value pairs, rather than arrays of arrays
  when parsing `links` and `social`. This differed from a regular Turbopelican
  project. Now expecting arrays of arrays.

### Other changes

- Shifting `TurbopelicanError` into separate folder dedicated to errors.
- Including badges for PyPI project and use of uv in `README.md`.
- Fixing spelling mistake in `CHANGELOG.md`.

## Version 0.4.2

### Bug fixes

- In version 0.4.0, Turbopelican would suppress all output from `uv sync`,
  when the desired behaviour was for Turbopelican to suppress only the virtual
  environment warning. Now the output can be viewed again, minus the warning.

### Other changes

- Providing instructions in `README.md` for editing the Turbopelican
  repository using NeoVim.
- Renaming `TurboConfiguration` to `InitConfiguration`. The variables should
  be clearly distinct so there is not confusion as to which is responsible for
  what.
- Prettified `init.lua`. Future changes can be prettified at
  `https://codebeautify.org/lua-beautifier`.
- Releasing new versions of Turbopelican automatically. When a version tag is
  pushed to GitHub, a workflow starts which builds the package and uploads it
  to PyPI, as well as creating a GitHub release with the appropriate details
  scraped from `CHANGELOG.md`.

## Version 0.4.1

### Bug fixes

- In version 0.2.0, a phantom setting `INDEX_URL` was mistakenly introduced.
  Now it has been removed.

### Other changes

- Enabling developers to start the "**Run CI**" workflow manually, rather than
  the workflow only running after a push. This is so that contributors who
  push to their own fork, without first enabling the use of workflows, can
  still easily run the workflow on their branch.
- Adding a section to the `README.md` titled "**Development**", which outlines
  who developers can contribute to Turbopelican.
- Adding a table of contents to `README.md` for improved navigation.
- Removing unused `pyright` execution environment (directory does not exist
  anymore), which was previously incorrect anyway.
- Shifting `pyright` configuration into `pyproject.toml` to minimize the
  number of files at the root level.

## Version 0.4.0

### Features

- Allowing the user to import `turbopelican`, which simplifies the process
  of loading configuration from `turbopelican.toml` or `pyproject.toml`.
- By default, new projects use the `load_config` function from `turbopelican`
  to load their configuration without the need for parsing TOML manually.
- Introducing `--minimal-install` flag to allow the user to create a project
  without installing `turbopelican` as a dependency thereof.
- New projects now include a Turbopelican badge in their `README.md` file.

### Other changes

- Stopping `pyright` from sending hint diagnostics to NeoVim. This would
  result in any variable prefixed with an underscore causing a hint.
- The template for the new website directory, as well as override templates,
  are now kept together in one parent folder.
- Silencing warnings during run of `make ci` that uv is interacting with the
  `mywebsite` project's virtual environment when a different virtual
  environment is activated. This is intentional behaviour, and needs no
  warning.
- Updating all dependencies. Includes bumping `tzdata` to v2025.2, `pyright`
  to v1.1.400 and `ruff` to v0.11.9.

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
