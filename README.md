<div align="center"><img width="400" alt="turbopelican logo" src="https://raw.githubusercontent.com/clockback/turbopelican/refs/heads/main/assets/logo.svg"/></div>

# turbopelican

[![turbopelican](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/clockback/turbopelican/refs/heads/adding-badge/assets/badge/v1.json)](https://github.com/clockback/turbopelican)

An uber-quick tool to create a Pelican static-site and deploy it to GitHub
Pages.

## Usage

Users are recommended to run turbopelican using `uvx`:

```sh
uvx turbopelican mypersonalsite
```

This will create a new repository `mypersonalsite`, with everything ready to
push to GitHub.

> ℹ️  **_NOTE:_**  Make sure that the site-url uses the GitHub repository's name.
For example, if you want the website to be `https://johndoe.github.io`, your
GitHub repository will need to be called `johndoe.github.io`.

You will then need to open your GitHub repository's settings, and under
"**Code and automation**" click "**Pages**". The section "**Build and
deployment**" allows you to choose a source. Choose GitHub actions, and your
site should be published.

You can learn more about Pelican [here](https://getpelican.com).

### Configuration

Pelican still targets Python 3.9, which does not bundle built-in support for
reading TOML configuration. Projects using `turbopelican` require Python 3.11
or higher, and therefore adopt the newer convention of placing configuration
in a TOML file rather than Python scripts. Generally, you should only need to
modify `turbopelican.toml`, rather than `pelicanconf.py` or `publishconf.py`.
