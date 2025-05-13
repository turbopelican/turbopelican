"""Settings for publishing to GitHub Pages.

This file is only used if you use `make publish` or
explicitly specify it as your config file.
"""

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

__all__ = [
    "ARTICLE_PATHS",
    "AUTHOR",
    "AUTHOR_FEED_ATOM",
    "AUTHOR_FEED_RSS",
    "CATEGORY_FEED_ATOM",
    "DEFAULT_LANG",
    "DEFAULT_PAGINATION",
    "DELETE_OUTPUT_DIRECTORY",
    "EXTRA_PATH_METADATA",
    "FEED_ALL_ATOM",
    "INDEX_SAVE_AS",
    "LINKS",
    "PAGE_PATHS",
    "PAGE_SAVE_AS",
    "PATH",
    "RELATIVE_URLS",
    "SITENAME",
    "SITEURL",
    "SOCIAL",
    "STATIC_PATHS",
    "THEME",
    "TIMEZONE",
    "TRANSLATION_FEED_ATOM",
]

import os
import sys
import tomllib
from pathlib import Path

sys.path.append(os.curdir)
from pelicanconf import (
    ARTICLE_PATHS,
    AUTHOR,
    AUTHOR_FEED_ATOM,
    AUTHOR_FEED_RSS,
    DEFAULT_LANG,
    DEFAULT_PAGINATION,
    EXTRA_PATH_METADATA,
    INDEX_SAVE_AS,
    LINKS,
    PAGE_PATHS,
    PAGE_SAVE_AS,
    PATH,
    SITENAME,
    SOCIAL,
    STATIC_PATHS,
    THEME,
    TIMEZONE,
    TRANSLATION_FEED_ATOM,
)

with Path("turbopelican.toml").open("rb") as config:
    pelicanconf = tomllib.load(config)


# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = pelicanconf["publish"]["site_url"]
RELATIVE_URLS = pelicanconf["publish"]["relative_urls"]

FEED_ALL_ATOM = pelicanconf["publish"]["feed_all_atom"]
CATEGORY_FEED_ATOM = pelicanconf["publish"]["category_feed_atom"]

DELETE_OUTPUT_DIRECTORY = pelicanconf["publish"]["delete_output_directory"]
