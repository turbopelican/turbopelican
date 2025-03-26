# turbopelican

An uber-quick tool to create a Pelican static-site and deploy it to GitHub Pages.

## Usage

Users are recommended to run turbopelican using `uvx`:

```sh
uvx turbopelican mypersonalsite
```

This will create a new repository `mypersonalsite`, with everything ready to push to GitHub. Make sure that the site-url uses the GitHub repository's name. For example, if you want the website to be `https://turbopelicanwashere.github.io`, your GitHub repository will need to be called `turbopelicanwashere.github.io`. You will then need to open your GitHub repository's settings, and under "Code and automation" click "Pages". The section "Build and deployment" allows you to choose a source. Choose GitHub actions. Then publish your site.

You can learn more about Pelican [here](https://getpelican.com).

### Notes

Pelican still targets Python 3.9, which does not bundle built-in support for reading TOML configuration. Projects using `turbopelican` requires Python 3.11 or higher, and therefore adopts the newer convention of placing configuration in a TOML file rather than Python scripts. Generally, you should only need to modify `turbopelican.toml`, rather than `pelicanconf.py` or `publishconf.py`.

