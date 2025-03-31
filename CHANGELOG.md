# Changelog

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
