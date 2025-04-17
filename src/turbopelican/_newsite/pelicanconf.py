"""Configures Pelican.

Author: Elliot Simpson
"""

import tomllib
from pathlib import Path

with Path("turbopelican.toml").open("rb") as config:
    turbopelican_config = tomllib.load(config)["pelican"]


AUTHOR: str = turbopelican_config["author"]
SITENAME: str = turbopelican_config["sitename"]
SITEURL = ""

TIMEZONE: str = turbopelican_config["timezone"]

DEFAULT_LANG: str = turbopelican_config["default_lang"]

PATH: str = turbopelican_config["path"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS: tuple[tuple[str, str], ...] = tuple(
    (link["title"], link["url"]) for link in turbopelican_config.get("links", [])
)

# Social widget
SOCIAL: tuple[tuple[str, str], ...] = tuple(
    (link["title"], link["url"]) for link in turbopelican_config.get("social", [])
)

DEFAULT_PAGINATION: bool = turbopelican_config["default_pagination"]

THEME: str = turbopelican_config["theme"]

ARTICLE_PATHS: list[str] = turbopelican_config["article_paths"]
PAGE_PATHS: list[str] = turbopelican_config["page_paths"]
PAGE_SAVE_AS: str = turbopelican_config["page_save_as"]

STATIC_PATHS: list[str] = turbopelican_config["static_paths"]
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = {
    metadata["origin"]: {
        key: value for (key, value) in metadata.items() if key != "origin"
    }
    for metadata in turbopelican_config["extra_path_metadata"]
}

INDEX_SAVE_AS: str = turbopelican_config["index_save_as"]
INDEX_URL: str = turbopelican_config["index_url"]
