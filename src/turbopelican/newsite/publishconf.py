"""Settings for publishing to GitHub Pages.

This file is only used if you use `make publish` or
explicitly specify it as your config file.
"""

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

__all__ = [
    "AUTHOR",
    "AUTHOR_FEED_ATOM",
    "AUTHOR_FEED_RSS",
    "CATEGORY_FEED_ATOM",
    "DEFAULT_LANG",
    "DEFAULT_PAGINATION",
    "FEED_ALL_ATOM",
    "LINKS",
    "PATH",
    "SITENAME",
    "SOCIAL",
    "TIMEZONE",
    "TRANSLATION_FEED_ATOM",
]

import tomllib
from pathlib import Path

from .pelicanconf import (
    AUTHOR,
    AUTHOR_FEED_ATOM,
    AUTHOR_FEED_RSS,
    DEFAULT_LANG,
    DEFAULT_PAGINATION,
    LINKS,
    PATH,
    SITENAME,
    SOCIAL,
    TIMEZONE,
    TRANSLATION_FEED_ATOM,
)

with Path("turbopelican.toml").open("rb") as config:
    pelicanconf = tomllib.load(config)


# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = pelicanconf["publish"]["site_url"]
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
