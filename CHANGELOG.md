# Changelog

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
