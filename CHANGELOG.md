# Changelog

## Version 0.6.1

### Bug fixes

- In the version prior, adorning a version prior without having sourced a
  virtual environment would raise an error, given that the environment
  variable `VIRTUAL_ENV` would not exist. Now the environment variable being
  absent not cause any such issue.
- In version 0.1.0, when a branch on a Turbopelican website repository other
  than `main` was pushed, it would still publish the website due to a typo in
  the GitHub workflow. Now the typo is corrected.
- In version 0.1.0, a Turbopelican website not hosted at the root domain would
  have linking issues. Now the links are appropriately relative to the
  project's root.
- In the version prior, a user adorning a website would be suggested an
  incorrect default site URL. Now the default should be correct.
- In version 0.1.0, a Turbopelican website not hosted at the root domain would
  incorrectly link its CSS styling. Now the styling is correctly linked.
- In version 0.1.0, a Turbopelican website not hosted at the root domain would
  have a hyperlink to the website's root, rather than to the project's root.
  Now correctly directing the hyperlink to the project's root.

### Other changes

- Renaming directory `assets/docs` to `assets/readme`. Documentation is now
  kept at the [project's website](https://turbopelican.github.io).
- Creating a new top-level directory called `docs` which contains the
  contents for the new website, without including styling and boilerplate.
- Using more intuitive example `run-turbopelican-init.gif` for `README.md`.
- Adding project's website to the project's URLs.
- Simplifying process of generating release notes to simple sed script.

## Version 0.6.0

### Features

- Adding `turbopelican adorn` subcommand, which can be used to add Pelican
  static-site websites to existing Git repositories.
- Adding `--no-commit` flag, in the absence of which, `Turbopelican` will
  automatically attempt to create an initial commit in the repository once the
  repository has been fully populated.
- Adding `--use-gh-cli` flag (for use only with a working installation of
  [GitHub CLI](https://cli.github.com/)) which causes Turbopelican to
  automatically attempt to create the GitHub repository and push the local
  tree to GitHub.
- When a user attempts to perform `turbopelican init` on a directory that
  already contains some files, Turbopelican suggests for the user to run
  `turbopelican adorn` instead.

### Other changes

- Cutting redundant NeoVim configuration, while also configuring NeoVim to run
  Ruff's import sorting fix on save.
- Updating dependencies, including `pydantic` to `v2.11.6`, `pyright` to
  `v1.1.402`, and `ruff` to `v0.11.13`.

## Version 0.5.1

### Bug fixes

- In the version prior, the `SLUG_REGEX_SUBSTITUTIONS` values were incorrect.
  This drastically affected site generation by creating a file `.html` instead
  of `my-article.html`, which in turn would make the site practically
  unusable. Now the correct substitutions are being made.
- In version 0.2.0, the `base.html` file contained a typo in `initial-scale`.
  Now the typo has been corrected.
- In version 0.2.0, the `index.md` file contained an `<img>` tag with an
  erroneous closing tag. Now the tag is correctly used.
- In version 0.2.0, any file generated using `base.html` would contain
  `<html lang="">` instead of a tag containing the default language. Now the
  language appears correctly in the HTML.

### Other changes

- Generating an example usage of Turbopelican with Terminalizer for use in
  `README.md`.
- Using more generic examples in `README.md`.
- Adding missing changes (including features) to `CHANGELOG.md` for version
  0.5.0.
- Correcting formatting issue in `CHANGELOG.md`.

## Version 0.5.0

### Features

- Using Pydantic to validate configuration.
- Allowing Pelican configuration settings in their entirety to be configured
  via `turbopelican.toml`.
- Introducing configuration `meta.module_prefix` setting for Turbopelican to
  parse certain strings as functions.
- Introducing configuration `meta.null_sentinel` setting for Turbopelican to
  replace certain values with `null`.
- Using configuration overrides, such that when a configuration setting should
  be the same for development and publication, it only needs to be set in the
  development settings.
- Printing message when Turbopelican finishes project initialization.
- `publishconf.py` is no longer distributed, and Turbopelican can infer both
  development configuration and production configuration only using
  `pelicanconf.py`.
- Introduction of configurable nullable sentinel values. By using the
  configuration setting `meta.null_sentinel`, one can determine which values
  under `pelican` or `publish` are to be swapped for `None` when parsed into
  Python.
- Introduction of configurable module prefixes. The configuration setting
  `meta.module_prefx` should be an array of tables, each with a `prefix` value
  and a `module_name` value. Any string with the specified prefixes are
  swapped out for functions imported from the associated module. E.g. if a
  `prefix` value is set to `"@mymodule:"`, and the associated `module_name`
  value is set to `mypackage.mymodule`, then the string value
  `"@mymodule:func"` will be replaced with the function `func` from
  `mypackage.mymodule`.

### Other changes

- Updating dependencies, including `tomlkit` to `v0.13.3`, `freezegun` to
  `v1.5.2`, `pyright` to `v1.1.401`, `pytest` to `v8.4.0`, and `ruff` to
  `v0.11.12`.
- Aliasing virtual environment in `Makefile`.
- Extracting contents of `_utils/config.py` into multiple files for greater
  extensibility.

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
