"""Configures Pelican.

Author: Elliot Simpson
"""

__all__ = [
    "ANALYTICS",
    "ARCHIVES_SAVE_AS",
    "ARTICLE_EXCLUDES",
    "ARTICLE_LANG_SAVE_AS",
    "ARTICLE_LANG_URL",
    "ARTICLE_ORDER_BY",
    "ARTICLE_PATHS",
    "ARTICLE_SAVE_AS",
    "ARTICLE_URL",
    "AUTHOR",
    "AUTHORS_SAVE_AS",
    "AUTHOR_FEED_ATOM",
    "AUTHOR_FEED_ATOM_URL",
    "AUTHOR_FEED_RSS",
    "AUTHOR_FEED_RSS_URL",
    "AUTHOR_REGEX_SUBSTITUTIONS",
    "AUTHOR_SAVE_AS",
    "AUTHOR_URL",
    "BIND",
    "CACHE_CONTENT",
    "CACHE_PATH",
    "CATEGORIES_SAVE_AS",
    "CATEGORY_FEED_ATOM",
    "CATEGORY_FEED_ATOM_URL",
    "CATEGORY_FEED_RSS",
    "CATEGORY_FEED_RSS_URL",
    "CATEGORY_REGEX_SUBSTITUTIONS",
    "CATEGORY_SAVE_AS",
    "CATEGORY_URL",
    "CHECK_MODIFIED_METHOD",
    "CONTENT_CACHING_LAYER",
    "CSS_FILE",
    "DATE_FORMATS",
    "DAY_ARCHIVE_SAVE_AS",
    "DAY_ARCHIVE_URL",
    "DEFAULT_CATEGORY",
    "DEFAULT_DATE",
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_LANG",
    "DEFAULT_METADATA",
    "DEFAULT_ORPHANS",
    "DEFAULT_PAGINATION",
    "DELETE_OUTPUT_DIRECTORY",
    "DIRECT_TEMPLATES",
    "DISPLAY_CATEGORIES_ON_MENU",
    "DISPLAY_PAGES_ON_MENU",
    "DISQUS_SITENAME",
    "DOCUTILS_SETTINGS",
    "DRAFT_LANG_SAVE_AS",
    "DRAFT_LANG_URL",
    "DRAFT_PAGE_LANG_SAVE_AS",
    "DRAFT_PAGE_LANG_URL",
    "DRAFT_PAGE_SAVE_AS",
    "DRAFT_PAGE_URL",
    "DRAFT_SAVE_AS",
    "DRAFT_URL",
    "EXTRA_PATH_METADATA",
    "FEED_ALL_ATOM",
    "FEED_ALL_ATOM_URL",
    "FEED_ALL_RSS",
    "FEED_ALL_RSS_URL",
    "FEED_APPEND_REF",
    "FEED_ATOM",
    "FEED_ATOM_URL",
    "FEED_DOMAIN",
    "FEED_MAX_ITEMS",
    "FEED_RSS",
    "FEED_RSS_URL",
    "FILENAME_METADATA",
    "FORMATTED_FIELDS",
    "GITHUB_URL",
    "GZIP_CACHE",
    "IGNORE_FILES",
    "INDEX_SAVE_AS",
    "INTRASITE_LINK_REGEX",
    "JINJA_ENVIRONMENT",
    "LINKS",
    "LINKS_WIDGET_NAME",
    "LOAD_CONTENT_CACHE",
    "MARKDOWN",
    "MONTH_ARCHIVE_SAVE_AS",
    "MONTH_ARCHIVE_URL",
    "NEWEST_FIRST_ARCHIVES",
    "OUTPUT_PATH",
    "OUTPUT_RETENTION",
    "OUTPUT_SOURCES",
    "OUTPUT_SOURCES_EXTENSION",
    "PAGE_EXCLUDES",
    "PAGE_LANG_SAVE_AS",
    "PAGE_LANG_URL",
    "PAGE_ORDER_BY",
    "PAGE_PATHS",
    "PAGE_SAVE_AS",
    "PAGE_URL",
    "PATH",
    "PATH_METADATA",
    "PLUGIN_PATHS",
    "PORT",
    "PYGMENTS_RST_OPTIONS",
    "RELATIVE_URLS",
    "REVERSE_CATEGORY_ORDER",
    "RSS_FEED_SUMMARY_ONLY",
    "SITENAME",
    "SITESUBTITLE",
    "SITEURL",
    "SLUGIFY_PRESERVE_CASE",
    "SLUGIFY_SOURCE",
    "SLUGIFY_USE_UNICODE",
    "SLUG_REGEX_SUBSTITUTIONS",
    "SOCIAL",
    "SOCIAL_WIDGET_NAME",
    "STATIC_CHECK_IF_MODIFIED",
    "STATIC_CREATE_LINKS",
    "STATIC_EXCLUDES",
    "STATIC_EXCLUDE_SOURCES",
    "STATIC_PATHS",
    "STYLESHEET_URL",
    "SUMMARY_END_SUFFIX",
    "SUMMARY_MAX_LENGTH",
    "SUMMARY_MAX_PARAGRAPHS",
    "TAGS_SAVE_AS",
    "TAG_FEED_ATOM",
    "TAG_FEED_ATOM_URL",
    "TAG_FEED_RSS",
    "TAG_REGEX_SUBSTITUTIONS",
    "TAG_SAVE_AS",
    "TAG_URL",
    "TEMPLATE_EXTENSIONS",
    "TEMPLATE_PAGES",
    "THEME",
    "THEME_STATIC_DIR",
    "THEME_STATIC_PATHS",
    "THEME_TEMPLATES_OVERRIDES",
    "TIMEZONE",
    "TRANSLATION_FEED_ATOM",
    "TRANSLATION_FEED_ATOM_URL",
    "TRANSLATION_FEED_RSS",
    "TRANSLATION_FEED_RSS_URL",
    "TWITTER_USERNAME",
    "TYPOGRIFY",
    "TYPOGRIFY_DASHES",
    "TYPOGRIFY_IGNORE_TAGS",
    "TYPOGRIFY_OMIT_FILTERS",
    "USE_FOLDER_AS_CATEGORY",
    "WITH_FUTURE_DATES",
    "YEAR_ARCHIVE_SAVE_AS",
    "YEAR_ARCHIVE_URL",
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


_default_regex_substitutions = _get(
    "slug_regex_substitutions",
    [
        [r"[^\\w\\s-]", ""],
        [r"(?u)\\A\\s*", ""],
        [r"(?u)\\s*\\Z", ""],
        [r"[-\\s]+", "-"],
    ],
)


ANALYTICS: str | None = _get("analytics", None)
ARCHIVES_SAVE_AS: str = _get("archives_save_as", "archives.html")
ARTICLE_EXCLUDES: list[str] = _get("article_excludes", [])
ARTICLE_LANG_SAVE_AS: str = _get("article_lang_save_as", "{slug}-{lang}.html")
ARTICLE_LANG_URL: str = _get("article_lang_url", "{slug}-{lang}.html")
ARTICLE_ORDER_BY: str = _get("article_order_by", "reversed-date")
ARTICLE_PATHS: list[str] = _get("article_paths", [""])
ARTICLE_SAVE_AS: str = _get("article_save_as", "{slug}.html")
ARTICLE_URL: str = _get("article_url", "{slug}.html")
AUTHOR: str | None = _get("author", None)
AUTHORS_SAVE_AS: str = _get("authors_save_as", "authors.html")
AUTHOR_FEED_ATOM: str | None = _get("author_feed_atom", "feeds/{slug}.atom.xml")
AUTHOR_FEED_ATOM_URL: str | None = _get("author_feed_atom_url", None)
AUTHOR_FEED_RSS: str | None = _get("author_feed_rss", "feeds/{slug}.rss.xml")
AUTHOR_FEED_RSS_URL: str | None = _get("author_feed_rss_url", None)
AUTHOR_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = list(
    map(tuple, _get("author_regex_substitutions", _default_regex_substitutions))
)
AUTHOR_SAVE_AS: str = _get("author_save_as", "author/{slug}.html")
AUTHOR_URL: str = _get("author_url", "author/{slug}.html")
BIND: str = _get("bind", "127.0.0.1")
CACHE_CONTENT: bool = _get("cache_content", fallback=False)
CACHE_PATH: str = _get("cache_path", "cache")
CATEGORIES_SAVE_AS: str = _get("categories_save_as", "categories.html")
CATEGORY_FEED_ATOM: str | None = _get("category_feed_atom", "feeds/{slug}.atom.xml")
CATEGORY_FEED_ATOM_URL: str | None = _get("category_feed_atom_url", None)
CATEGORY_FEED_RSS: str | None = _get("category_feed_rss", None)
CATEGORY_FEED_RSS_URL: str | None = _get("category_feed_rss_url", None)
CATEGORY_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = list(
    map(tuple, _get("category_regex_substitutions", _default_regex_substitutions))
)
CATEGORY_SAVE_AS: str = _get("category_save_as", "category/{slug}.html")
CATEGORY_URL: str = _get("category_url", "category/{slug}.html")
CHECK_MODIFIED_METHOD: str = _get("check_modified_method", "mtime")
CONTENT_CACHING_LAYER: str = _get("content_caching_layer", "reader")
CSS_FILE: str = _get("css_file", "main.css")
DATE_FORMATS: dict[str, str | tuple[str, str]] = {
    lang: (tuple(date_format) if isinstance(date_format, list) else date_format)
    for (lang, date_format) in _get("date_formats", {}).items()
}
DAY_ARCHIVE_SAVE_AS: str = _get("day_archive_save_as", "")
DAY_ARCHIVE_URL: str = _get("day_archive_url", "")
DEFAULT_CATEGORY: str = _get("default_category", "misc")
DEFAULT_DATE: str | tuple[int, ...] | None = _get("default_date", None)
DEFAULT_DATE_FORMAT: str = _get("default_date_format", "%a %d %B %Y")
DEFAULT_LANG: str = _get("default_lang", "en")
DEFAULT_METADATA: str = _get("default_metadata", {})
DEFAULT_ORPHANS: int = _get("default_orphans", 0)
DEFAULT_PAGINATION: bool = _get("default_pagination", fallback=False)
DELETE_OUTPUT_DIRECTORY: bool = _get("delete_output_directory", fallback=False)
DIRECT_TEMPLATES: list[str] = _get(
    "direct_templates", ["index", "tags", "categories", "authors", "archives"]
)
DISPLAY_CATEGORIES_ON_MENU: bool = _get("display_categories_on_menu", fallback=True)
DISPLAY_PAGES_ON_MENU: bool = _get("display_pages_on_menu", fallback=True)
DISQUS_SITENAME: str | None = _get("disqus_sitename", None)
DOCUTILS_SETTINGS: dict = _get("docutils_settings", {})
DRAFT_LANG_SAVE_AS: str = _get("draft_lang_save_as", "drafts/{slug}-{lang}.html")
DRAFT_LANG_URL: str = _get("draft_lang_url", "drafts/{slug}-{lang}.html")
DRAFT_PAGE_LANG_SAVE_AS: str = _get(
    "draft_page_lang_save_as", "drafts/pages/{slug}-{lang}.html"
)
DRAFT_PAGE_LANG_URL: str = _get(
    "draft_page_lang_url", "drafts/pages/{slug}-{lang}.html"
)
DRAFT_PAGE_SAVE_AS: str = _get("draft_page_save_as", "drafts/pages/{slug}.html")
DRAFT_PAGE_URL: str = _get("draft_page_url", "drafts/pages/{slug}.html")
DRAFT_SAVE_AS: str = _get("draft_save_as", "drafts/{slug}.html")
DRAFT_URL: str = _get("draft_url", "drafts/{slug}.html")
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = {
    metadata["origin"]: {
        key: value for (key, value) in metadata.items() if key != "origin"
    }
    for metadata in _get("extra_path_metadata", {})
}
FEED_ALL_ATOM: str | None = _get("feed_all_atom", "feeds/all.atom.xml")
FEED_ALL_ATOM_URL: str | None = _get("feed_all_atom_url", None)
FEED_ALL_RSS: str | None = _get("feed_all_rss", None)
FEED_ALL_RSS_URL: str | None = _get("feed_all_rss_url", None)
FEED_APPEND_REF: bool = _get("feed_append_ref", fallback=False)
FEED_ATOM: str | None = _get("feed_atom", None)
FEED_ATOM_URL: str | None = _get("feed_atom_url", None)
FEED_DOMAIN: str = _get("feed_domain", "")
FEED_MAX_ITEMS: int | None = _get("feed_max_items", 100)
FEED_RSS: str | None = _get("feed_rss", None)
FEED_RSS_URL: str | None = _get("feed_rss_url", None)
FILENAME_METADATA: str = _get(
    "filename_metadata", r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)"
)
FORMATTED_FIELDS: list[str] = _get("formatted_fields", ["summary"])
GITHUB_URL: str | None = _get("github_url", None)
GZIP_CACHE: bool = _get("gzip_cache", fallback=True)
IGNORE_FILES: list[str] = _get("ignore_files", ["**/.*"])
INDEX_SAVE_AS: str = _get("index_save_as", "index.html")
INTRASITE_LINK_REGEX: str = _get("intrasite_link_regex", "[{|](?P<what>.*?)[|}]")
JINJA_ENVIRONMENT: dict = _get(
    "jinja_environment", {"extensions": [], "trim_blocks": True, "lstrip_blocks": True}
)
LINKS: tuple[tuple[str, str], ...] = tuple(map(tuple, _get("links", [])))
LINKS_WIDGET_NAME: str | None = _get("links_widget_name", None)
LOAD_CONTENT_CACHE: bool = _get("load_content_cache", fallback=False)
MARKDOWN: dict = _get(
    "markdown",
    {
        "extension_configs": {
            "markdown.extensions.codehilite": {"css_class": "highlight"},
            "markdown.extensions.extra": {},
            "markdown.extensions.meta": {},
        },
        "output_format": "html5",
    },
)
MONTH_ARCHIVE_SAVE_AS: str = _get("month_archive_save_as", "")
MONTH_ARCHIVE_URL: str = _get("month_archive_url", "")
NEWEST_FIRST_ARCHIVES: bool = _get("newest_first_archives", fallback=True)
OUTPUT_PATH: str = _get("output_path", "output")
OUTPUT_RETENTION: list[str] = _get("output_retention", [])
OUTPUT_SOURCES: bool = _get("output_sources", fallback=False)
OUTPUT_SOURCES_EXTENSION: str = _get("output_sources_extension", ".text")
PAGE_EXCLUDES: list[str] = _get("page_excludes", [])
PAGE_LANG_SAVE_AS: str = _get("page_lang_save_as", "pages/{slug}-{lang}.html")
PAGE_LANG_URL: str = _get("page_lang_url", "pages/{slug}-{lang}.html")
PAGE_ORDER_BY: str = _get("page_order_by", "basename")
PAGE_PATHS: list[str] = _get("page_paths", ["pages"])
PAGE_SAVE_AS: str = _get("page_save_as", "pages/{slug}.html")
PAGE_URL: str = _get("page_url", "pages/{slug}.html")
PATH: str = _get("path", ".")
PATH_METADATA: str = _get("path_metadata", "")
PLUGIN_PATHS: list[str] = _get("plugin_paths", [])
PORT: int = _get("port", 8000)
PYGMENTS_RST_OPTIONS: dict = _get("pygments_rst_options", {})
RELATIVE_URLS: bool = _get("relative_urls", fallback=False)
REVERSE_CATEGORY_ORDER: bool = _get("reverse_category_order", fallback=False)
RSS_FEED_SUMMARY_ONLY: bool = _get("rss_feed_summary_only", fallback=True)
SITENAME: str = _get("sitename", "A Pelican Blog")
SITESUBTITLE: str | None = _get("sitesubtitle", None)
SITEURL: str = _get("site_url", "")
SLUGIFY_PRESERVE_CASE: bool = _get("slugify_preserve_case", fallback=False)
SLUGIFY_SOURCE: str = _get("slugify_source", "title")
SLUGIFY_USE_UNICODE: bool = _get("slugify_use_unicode", fallback=False)
SLUG_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = list(
    map(tuple, _default_regex_substitutions)
)
SOCIAL: tuple[tuple[str, str], ...] = tuple(map(tuple, _get("social", [])))
SOCIAL_WIDGET_NAME: str | None = _get("social_widget_name", None)
STATIC_CHECK_IF_MODIFIED: bool = _get("static_check_if_modified", fallback=False)
STATIC_CREATE_LINKS: bool = _get("static_create_links", fallback=False)
STATIC_EXCLUDES: list[str] = _get("static_excludes", [])
STATIC_EXCLUDE_SOURCES: bool = _get("static_exclude_sources", fallback=True)
STATIC_PATHS: list[str] = _get("static_paths", ["images"])
STYLESHEET_URL: str | None = _get("stylesheet_url", None)
SUMMARY_END_SUFFIX: str = _get("summary_end_suffix", "…")
SUMMARY_MAX_LENGTH: int | None = _get("summary_end_suffix", 50)
SUMMARY_MAX_PARAGRAPHS: int | None = _get("summary_max_paragraphs", None)
TAGS_SAVE_AS: str = _get("tags_save_as", "tags.html")
TAG_FEED_ATOM: str | None = _get("tag_feed_atom", None)
TAG_FEED_ATOM_URL: str | None = _get("tag_feed_atom_url", None)
TAG_FEED_RSS: str | None = _get("tag_feed_rss", None)
TAG_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = list(
    map(tuple, _get("tag_regex_substitutions", _default_regex_substitutions))
)
TAG_SAVE_AS: str = _get("tag_save_as", "tag/{slug}.html")
TAG_URL: str = _get("tag_url", "tag/{slug}.html")
TEMPLATE_EXTENSIONS: list[str] = _get("template_extensions", [".html"])
TEMPLATE_PAGES: dict[str, str] = _get("template_pages", {})
THEME: str = _get("theme", "notmyidea")
THEME_STATIC_DIR: str = _get("theme_static_dir", "theme")
THEME_STATIC_PATHS: list[str] = _get("theme_static_paths", ["static"])
THEME_TEMPLATES_OVERRIDES: list[str] = _get("theme_templates_overrides", [])
TIMEZONE: str = _get("timezone", "UTC")
TRANSLATION_FEED_ATOM: str | None = _get(
    "translation_feed_atom", "feeds/all-{lang}.atom.xml"
)
TRANSLATION_FEED_ATOM_URL: str | None = _get("translation_feed_atom_url", None)
TRANSLATION_FEED_RSS: str | None = _get("translation_feed_rss", None)
TRANSLATION_FEED_RSS_URL: str | None = _get("translation_feed_rss_url", None)
TWITTER_USERNAME: str | None = _get("twitter_username", None)
TYPOGRIFY: bool = _get("typogrify", fallback=False)
TYPOGRIFY_DASHES: str = _get("typogrify_dashes", "default")
TYPOGRIFY_IGNORE_TAGS: list[str] = _get("typogrify_ignore_tags", [])
TYPOGRIFY_OMIT_FILTERS: list[str] = _get("typogrify_omit_filters", [])
USE_FOLDER_AS_CATEGORY: bool = _get("use_folder_as_category", fallback=True)
WITH_FUTURE_DATES: bool = _get("with_future_dates", fallback=True)
YEAR_ARCHIVE_SAVE_AS: str = _get("year_archive_save_as", "")
YEAR_ARCHIVE_URL: str = _get("year_archive_url", "")
