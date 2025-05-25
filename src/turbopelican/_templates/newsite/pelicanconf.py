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

from turbopelican import config

if os.environ.get("TURBOPELICAN_CONFIG_TYPE", "DEV") == "PUBLISH":
    _config_type = "PUBLISH"
else:
    _config_type = "DEV"

_config = config(_config_type)

ARTICLE_PATHS: list[str] = _config.article_paths
AUTHOR: str | None = _config.author
AUTHOR_FEED_ATOM: str | None = _config.author_feed_atom
AUTHOR_FEED_RSS: str | None = _config.author_feed_rss
CACHE_CONTENT: bool = _config.cache_content
CATEGORY_FEED_ATOM: str | None = _config.category_feed_atom
DEFAULT_LANG: str = _config.default_lang
DEFAULT_PAGINATION: int | bool = _config.default_pagination
DELETE_OUTPUT_DIRECTORY: bool = _config.delete_output_directory
DISPLAY_CATEGORIES_ON_MENU: bool = _config.display_categories_on_menu
DISPLAY_PAGES_ON_MENU: bool = _config.display_pages_on_menu
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = _config.extra_path_metadata
FEED_ALL_ATOM: str | None = _config.feed_all_atom
FEED_APPEND_REF: bool = _config.feed_append_ref
GZIP_CACHE: bool = _config.gzip_cache
INDEX_SAVE_AS: str = _config.index_save_as
LINKS: tuple[tuple[str, str], ...] = _config.links
LOAD_CONTENT_CACHE: bool = _config.load_content_cache
NEWEST_FIRST_ARCHIVES: bool = _config.newest_first_archives
OUTPUT_SOURCES: bool = _config.output_sources
PAGE_PATHS: list[str] = _config.page_paths
PAGE_SAVE_AS: str = _config.page_save_as
PATH: str = _config.path
RELATIVE_URLS: bool = _config.relative_urls
REVERSE_CATEGORY_ORDER: bool = _config.reverse_category_order
RSS_FEED_SUMMARY_ONLY: bool = _config.rss_feed_summary_only
SITENAME: str = _config.sitename
SITEURL: str = _config.site_url
SLUGIFY_PRESERVE_CASE: bool = _config.slugify_preserve_case
SLUGIFY_USE_UNICODE: bool = _config.slugify_use_unicode
SOCIAL: tuple[tuple[str, str], ...] = _config.social
STATIC_CHECK_IF_MODIFIED: bool = _config.static_check_if_modified
STATIC_CREATE_LINKS: bool = _config.static_create_links
STATIC_EXCLUDE_SOURCES: bool = _config.static_exclude_sources
STATIC_PATHS: list[str] = _config.static_paths
THEME: str = _config.theme
TIMEZONE: str = _config.timezone
TRANSLATION_FEED_ATOM: str | None = _config.translation_feed_atom
TYPOGRIFY: bool = _config.typogrify
USE_FOLDER_AS_CATEGORY: bool = _config.use_folder_as_category
WITH_FUTURE_DATES: bool = _config.with_future_dates
