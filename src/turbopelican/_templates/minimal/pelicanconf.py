"""Configures Pelican.

Author: Elliot Simpson
"""

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

import tomllib
from pathlib import Path


def _nullify_sentinels(data: dict) -> dict:
    """Recursively replaces sentinel values with None in dictionaries.

    Args:
        data: Whatever data still contains any sentinel values.

    Returns:
        The data with sentinel values replaced with None.
    """
    if isinstance(data, dict):
        return {key: _nullify_sentinels(value) for key, value in data.items()}
    if isinstance(data, list):
        return list(map(_nullify_sentinels, data))
    if data == -1:
        return None
    return data


with Path("turbopelican.toml").open("rb") as config:
    turbopelican_config = _nullify_sentinels(tomllib.load(config)["pelican"])

ARTICLE_PATHS: list[str] = turbopelican_config.get("article_paths", [""])
AUTHOR: str | None = turbopelican_config.get("author", None)
AUTHOR_FEED_ATOM: str | None = turbopelican_config.get(
    "author_feed_atom", "feeds/{slug}.atom.xml"
)
AUTHOR_FEED_RSS: str | None = turbopelican_config.get(
    "author_feed_rss", "feeds/{slug}.rss.xml"
)
CATEGORY_FEED_ATOM: str | None = turbopelican_config.get(
    "category_feed_atom", "feeds/{slug}.atom.xml"
)
DEFAULT_LANG: str = turbopelican_config.get("default_lang", "en")
DEFAULT_PAGINATION: bool = turbopelican_config.get("default_pagination", False)
DELETE_OUTPUT_DIRECTORY: bool = turbopelican_config.get(
    "delete_output_directory", False
)
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = {
    metadata["origin"]: {
        key: value for (key, value) in metadata.items() if key != "origin"
    }
    for metadata in turbopelican_config.get("extra_path_metadata", {})
}
FEED_ALL_ATOM: str | None = turbopelican_config.get(
    "feeds/all.atom.xml", "feeds/all.atom.xml"
)
INDEX_SAVE_AS: str = turbopelican_config.get("index_save_as", "index.html")
LINKS: tuple[tuple[str, str], ...] = tuple(
    map(tuple, turbopelican_config.get("links", []))
)
PAGE_PATHS: list[str] = turbopelican_config.get("page_paths", ["pages"])
PAGE_SAVE_AS: str = turbopelican_config.get("page_save_as", "pages/{slug}.html")
PATH: str = turbopelican_config.get("path", ".")
RELATIVE_URLS: bool = turbopelican_config.get("relative_urls", False)
SITENAME: str = turbopelican_config.get("sitename", "A Pelican Blog")
SITEURL: str = turbopelican_config.get("site_url", "")
SOCIAL: tuple[tuple[str, str], ...] = tuple(
    map(tuple, turbopelican_config.get("social", []))
)
STATIC_PATHS: list[str] = turbopelican_config.get("static_paths", ["images"])
THEME: str = turbopelican_config.get("theme", "notmyidea")
TIMEZONE: str = turbopelican_config.get("timezone", "UTC")
TRANSLATION_FEED_ATOM: str | None = turbopelican_config.get(
    "translation_feed_atom", "feeds/all-{lang}.atom.xml"
)
