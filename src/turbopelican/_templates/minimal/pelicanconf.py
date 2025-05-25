"""Configures Pelican.

Author: Elliot Simpson
"""

__all__ = [
    "ARTICLE_PATHS",
    "AUTHOR",
    "AUTHOR_FEED_ATOM",
    "AUTHOR_FEED_RSS",
    "CACHE_CONTENT",
    "CATEGORY_FEED_ATOM",
    "DEFAULT_LANG",
    "DEFAULT_PAGINATION",
    "DELETE_OUTPUT_DIRECTORY",
    "DISPLAY_CATEGORIES_ON_MENU",
    "DISPLAY_PAGES_ON_MENU",
    "EXTRA_PATH_METADATA",
    "FEED_ALL_ATOM",
    "FEED_APPEND_REF",
    "GZIP_CACHE",
    "INDEX_SAVE_AS",
    "LINKS",
    "LOAD_CONTENT_CACHE",
    "NEWEST_FIRST_ARCHIVES",
    "OUTPUT_SOURCES",
    "PAGE_PATHS",
    "PAGE_SAVE_AS",
    "PATH",
    "RELATIVE_URLS",
    "REVERSE_CATEGORY_ORDER",
    "RSS_FEED_SUMMARY_ONLY",
    "SITENAME",
    "SITEURL",
    "SLUGIFY_PRESERVE_CASE",
    "SLUGIFY_USE_UNICODE",
    "SOCIAL",
    "STATIC_CHECK_IF_MODIFIED",
    "STATIC_CREATE_LINKS",
    "STATIC_EXCLUDE_SOURCES",
    "STATIC_PATHS",
    "THEME",
    "TIMEZONE",
    "TRANSLATION_FEED_ATOM",
    "TYPOGRIFY",
    "USE_FOLDER_AS_CATEGORY",
    "WITH_FUTURE_DATES",
]

import os
import tomllib
from pathlib import Path
from typing import Any

_AnyJson = Any


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


_turbopelican_config_type = os.environ.get("TURBOPELICAN_CONFIG_TYPE", "DEV")

with Path("turbopelican.toml").open("rb") as config:
    _complete_config = tomllib.load(config)
    _complete_config["pelican"] = _nullify_sentinels(_complete_config["pelican"])
    if _turbopelican_config_type == "PUBLISH":
        _complete_config["publish"] = _nullify_sentinels(_complete_config["publish"])


def _get(setting_name: str, fallback: object) -> _AnyJson:
    """Obtains the setting with the provided name.

    Args:
        setting_name: The key identifying the setting.
        fallback: The default variable to return if key not found.

    Returns:
        The TOML object contained in the input configuration.
    """
    if (
        _turbopelican_config_type == "PUBLISH"
        and setting_name in _complete_config["publish"]
    ):
        return _complete_config["publish"][setting_name]
    return _complete_config["pelican"].get(setting_name, fallback)


ARTICLE_PATHS: list[str] = _get("article_paths", [""])
AUTHOR: str | None = _get("author", None)
AUTHOR_FEED_ATOM: str | None = _get("author_feed_atom", "feeds/{slug}.atom.xml")
AUTHOR_FEED_RSS: str | None = _get("author_feed_rss", "feeds/{slug}.rss.xml")
CACHE_CONTENT: bool = _get("cache_content", fallback=False)
CATEGORY_FEED_ATOM: str | None = _get("category_feed_atom", "feeds/{slug}.atom.xml")
DEFAULT_LANG: str = _get("default_lang", "en")
DEFAULT_PAGINATION: bool = _get("default_pagination", fallback=False)
DELETE_OUTPUT_DIRECTORY: bool = _get("delete_output_directory", fallback=False)
DISPLAY_CATEGORIES_ON_MENU: bool = _get("display_categories_on_menu", fallback=True)
DISPLAY_PAGES_ON_MENU: bool = _get("display_pages_on_menu", fallback=True)
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = {
    metadata["origin"]: {
        key: value for (key, value) in metadata.items() if key != "origin"
    }
    for metadata in _get("extra_path_metadata", {})
}
FEED_ALL_ATOM: str | None = _get("feed_all_atom", "feeds/all.atom.xml")
FEED_APPEND_REF: bool = _get("feed_append_ref", fallback=False)
GZIP_CACHE: bool = _get("gzip_cache", fallback=True)
INDEX_SAVE_AS: str = _get("index_save_as", "index.html")
LINKS: tuple[tuple[str, str], ...] = tuple(map(tuple, _get("links", [])))
LOAD_CONTENT_CACHE: bool = _get("load_content_cache", fallback=False)
NEWEST_FIRST_ARCHIVES: bool = _get("newest_first_archives", fallback=True)
OUTPUT_SOURCES: bool = _get("output_sources", fallback=False)
PAGE_PATHS: list[str] = _get("page_paths", ["pages"])
PAGE_SAVE_AS: str = _get("page_save_as", "pages/{slug}.html")
PATH: str = _get("path", ".")
RELATIVE_URLS: bool = _get("relative_urls", fallback=False)
REVERSE_CATEGORY_ORDER: bool = _get("reverse_category_order", fallback=False)
RSS_FEED_SUMMARY_ONLY: bool = _get("rss_feed_summary_only", fallback=True)
SITENAME: str = _get("sitename", "A Pelican Blog")
SITEURL: str = _get("site_url", "")
SLUGIFY_PRESERVE_CASE: bool = _get("slugify_preserve_case", fallback=False)
SLUGIFY_USE_UNICODE: bool = _get("slugify_use_unicode", fallback=False)
SOCIAL: tuple[tuple[str, str], ...] = tuple(map(tuple, _get("social", [])))
STATIC_CHECK_IF_MODIFIED: bool = _get("static_check_if_modified", fallback=False)
STATIC_CREATE_LINKS: bool = _get("static_create_links", fallback=False)
STATIC_EXCLUDE_SOURCES: bool = _get("static_exclude_sources", fallback=True)
STATIC_PATHS: list[str] = _get("static_paths", ["images"])
THEME: str = _get("theme", "notmyidea")
TIMEZONE: str = _get("timezone", "UTC")
TRANSLATION_FEED_ATOM: str | None = _get(
    "translation_feed_atom", "feeds/all-{lang}.atom.xml"
)
TYPOGRIFY: bool = _get("typogrify", fallback=False)
USE_FOLDER_AS_CATEGORY: bool = _get("use_folder_as_category", fallback=True)
WITH_FUTURE_DATES: bool = _get("with_future_dates", fallback=True)
