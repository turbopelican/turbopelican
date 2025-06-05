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
    "ARTICLE_TRANSLATION_ID",
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
    "JINJA_FILTERS",
    "JINJA_GLOBALS",
    "JINJA_TESTS",
    "LINKS",
    "LINKS_WIDGET_NAME",
    "LOAD_CONTENT_CACHE",
    "LOCALE",
    "LOG_FILTER",
    "MARKDOWN",
    "MENUITEMS",
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
    "PAGE_TRANSLATION_ID",
    "PAGE_URL",
    "PAGINATED_TEMPLATES",
    "PAGINATION_PATTERNS",
    "PATH",
    "PATH_METADATA",
    "PLUGINS",
    "PLUGIN_PATHS",
    "PORT",
    "PYGMENTS_RST_OPTIONS",
    "READERS",
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
from collections.abc import Callable
from typing import Literal

from turbopelican import config

if os.environ.get("TURBOPELICAN_CONFIG_TYPE", "DEV") == "PUBLISH":
    _config_type = "PUBLISH"
else:
    _config_type = "DEV"

_config = config(_config_type)

ANALYTICS: str | None = _config.analytics
ARCHIVES_SAVE_AS: str = _config.archives_save_as
ARTICLE_EXCLUDES: list[str] = _config.article_excludes
ARTICLE_LANG_SAVE_AS: str = _config.article_lang_save_as
ARTICLE_LANG_URL: str = _config.article_lang_url
ARTICLE_ORDER_BY: str = _config.article_order_by
ARTICLE_PATHS: list[str] = _config.article_paths
ARTICLE_SAVE_AS: str = _config.article_save_as
ARTICLE_TRANSLATION_ID: str | Literal[False] | None = _config.article_translation_id
ARTICLE_URL: str = _config.article_url
AUTHOR: str | None = _config.author
AUTHORS_SAVE_AS: str = _config.authors_save_as
AUTHOR_FEED_ATOM: str | None = _config.author_feed_atom
AUTHOR_FEED_ATOM_URL: str | None = _config.author_feed_atom_url
AUTHOR_FEED_RSS: str | None = _config.author_feed_rss
AUTHOR_FEED_RSS_URL: str | None = _config.author_feed_rss_url
AUTHOR_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = _config.author_regex_substitutions
AUTHOR_SAVE_AS: str = _config.author_save_as
AUTHOR_URL: str = _config.author_url
BIND: str = _config.bind
CACHE_CONTENT: bool = _config.cache_content
CACHE_PATH: str = _config.cache_path
CATEGORIES_SAVE_AS: str = _config.categories_save_as
CATEGORY_FEED_ATOM: str | None = _config.category_feed_atom
CATEGORY_FEED_ATOM_URL: str | None = _config.category_feed_atom_url
CATEGORY_FEED_RSS: str | None = _config.category_feed_rss
CATEGORY_FEED_RSS_URL: str | None = _config.category_feed_rss_url
CATEGORY_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = (
    _config.category_regex_substitutions
)
CATEGORY_SAVE_AS: str = _config.category_save_as
CATEGORY_URL: str = _config.category_url
CHECK_MODIFIED_METHOD: str = _config.check_modified_method
CONTENT_CACHING_LAYER: str = _config.content_caching_layer
CSS_FILE: str = _config.css_file
DATE_FORMATS: dict[str, str | tuple[str, str]] = _config.date_formats
DAY_ARCHIVE_SAVE_AS: str = _config.day_archive_save_as
DAY_ARCHIVE_URL: str = _config.day_archive_url
DEFAULT_CATEGORY: str = _config.default_category
DEFAULT_DATE: str | tuple[int, ...] | None = _config.default_date
DEFAULT_DATE_FORMAT: str = _config.default_date_format
DEFAULT_LANG: str = _config.default_lang
DEFAULT_METADATA: dict = _config.default_metadata
DEFAULT_ORPHANS: int = _config.default_orphans
DEFAULT_PAGINATION: int | bool = _config.default_pagination
DELETE_OUTPUT_DIRECTORY: bool = _config.delete_output_directory
DIRECT_TEMPLATES: list[str] = _config.direct_templates
DISPLAY_CATEGORIES_ON_MENU: bool = _config.display_categories_on_menu
DISPLAY_PAGES_ON_MENU: bool = _config.display_pages_on_menu
DISQUS_SITENAME: str | None = _config.disqus_sitename
DOCUTILS_SETTINGS: dict = _config.docutils_settings
DRAFT_LANG_SAVE_AS: str = _config.draft_lang_save_as
DRAFT_LANG_URL: str = _config.draft_lang_url
DRAFT_PAGE_LANG_SAVE_AS: str = _config.draft_page_lang_save_as
DRAFT_PAGE_LANG_URL: str = _config.draft_page_lang_url
DRAFT_PAGE_SAVE_AS: str = _config.draft_page_save_as
DRAFT_PAGE_URL: str = _config.draft_page_url
DRAFT_SAVE_AS: str = _config.draft_save_as
DRAFT_URL: str = _config.draft_url
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = _config.extra_path_metadata
FEED_ALL_ATOM: str | None = _config.feed_all_atom
FEED_ALL_ATOM_URL: str | None = _config.feed_all_atom_url
FEED_ALL_RSS: str | None = _config.feed_all_rss
FEED_ALL_RSS_URL: str | None = _config.feed_all_rss_url
FEED_APPEND_REF: bool = _config.feed_append_ref
FEED_ATOM: str | None = _config.feed_atom
FEED_ATOM_URL: str | None = _config.feed_atom_url
FEED_DOMAIN: str = _config.feed_domain
FEED_MAX_ITEMS: int | None = _config.feed_max_items
FEED_RSS: str | None = _config.feed_rss
FEED_RSS_URL: str | None = _config.feed_rss_url
FILENAME_METADATA: str = _config.filename_metadata
FORMATTED_FIELDS: list[str] = _config.formatted_fields
GITHUB_URL: str | None = _config.github_url
GZIP_CACHE: bool = _config.gzip_cache
IGNORE_FILES: list[str] = _config.ignore_files
INDEX_SAVE_AS: str = _config.index_save_as
INTRASITE_LINK_REGEX: str = _config.intrasite_link_regex
JINJA_ENVIRONMENT: dict = _config.jinja_environment
JINJA_FILTERS: dict[str, Callable] = _config.jinja_filters
JINJA_GLOBALS: dict = _config.jinja_globals
JINJA_TESTS: dict[str, Callable] = _config.jinja_tests
LINKS: tuple[tuple[str, str], ...] = _config.links
LINKS_WIDGET_NAME: str | None = _config.links_widget_name
LOAD_CONTENT_CACHE: bool = _config.load_content_cache
LOCALE: str | list[str] = _config.locale
LOG_FILTER: list[tuple[int, str]] = _config.log_filter
MARKDOWN: dict = _config.markdown
MENUITEMS: tuple[tuple[str, str], ...] = _config.menuitems
MONTH_ARCHIVE_SAVE_AS: str = _config.month_archive_save_as
MONTH_ARCHIVE_URL: str = _config.month_archive_url
NEWEST_FIRST_ARCHIVES: bool = _config.newest_first_archives
OUTPUT_PATH: str = _config.output_path
OUTPUT_RETENTION: list[str] = _config.output_retention
OUTPUT_SOURCES: bool = _config.output_sources
OUTPUT_SOURCES_EXTENSION: str = _config.output_sources_extension
PAGE_EXCLUDES: list[str] = _config.page_excludes
PAGE_LANG_SAVE_AS: str = _config.page_lang_save_as
PAGE_LANG_URL: str = _config.page_lang_url
PAGE_ORDER_BY: str = _config.page_order_by
PAGE_PATHS: list[str] = _config.page_paths
PAGE_SAVE_AS: str = _config.page_save_as
PAGE_TRANSLATION_ID: str | Literal[False] | None = _config.page_translation_id
PAGE_URL: str = _config.page_url
PAGINATED_TEMPLATES: dict[str, int | None] = _config.paginated_templates
PAGINATION_PATTERNS: list[tuple[int, str, str]] = _config.pagination_patterns
PATH: str = _config.path
PATH_METADATA: str = _config.path_metadata
PLUGINS: dict[str, Callable | str] = _config.plugins
PLUGIN_PATHS: list[str] = _config.plugin_paths
PORT: int = _config.port
PYGMENTS_RST_OPTIONS: dict = _config.pygments_rst_options
READERS: dict[str, Callable | None] = _config.readers
RELATIVE_URLS: bool = _config.relative_urls
REVERSE_CATEGORY_ORDER: bool = _config.reverse_category_order
RSS_FEED_SUMMARY_ONLY: bool = _config.rss_feed_summary_only
SITENAME: str = _config.sitename
SITESUBTITLE: str | None = _config.sitesubtitle
SITEURL: str = _config.site_url
SLUGIFY_PRESERVE_CASE: bool = _config.slugify_preserve_case
SLUGIFY_SOURCE: str = _config.slugify_source
SLUGIFY_USE_UNICODE: bool = _config.slugify_use_unicode
SLUG_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = _config.slug_regex_substitutions
SOCIAL: tuple[tuple[str, str], ...] = _config.social
SOCIAL_WIDGET_NAME: str | None = _config.social_widget_name
STATIC_CHECK_IF_MODIFIED: bool = _config.static_check_if_modified
STATIC_CREATE_LINKS: bool = _config.static_create_links
STATIC_EXCLUDES: list[str] = _config.static_excludes
STATIC_EXCLUDE_SOURCES: bool = _config.static_exclude_sources
STATIC_PATHS: list[str] = _config.static_paths
STYLESHEET_URL: str | None = _config.stylesheet_url
SUMMARY_END_SUFFIX: str = _config.summary_end_suffix
SUMMARY_MAX_LENGTH: int | None = _config.summary_max_length
SUMMARY_MAX_PARAGRAPHS: int | None = _config.summary_max_paragraphs
TAGS_SAVE_AS: str = _config.tags_save_as
TAG_FEED_ATOM: str | None = _config.tag_feed_atom
TAG_FEED_ATOM_URL: str | None = _config.tag_feed_atom_url
TAG_FEED_RSS: str | None = _config.tag_feed_rss
TAG_REGEX_SUBSTITUTIONS: list[tuple[str, str]] = _config.tag_regex_substitutions
TAG_SAVE_AS: str = _config.tag_save_as
TAG_URL: str = _config.tag_url
TEMPLATE_EXTENSIONS: list[str] = _config.template_extensions
TEMPLATE_PAGES: dict[str, str] = _config.template_pages
THEME: str = _config.theme
THEME_STATIC_DIR: str = _config.theme_static_dir
THEME_STATIC_PATHS: list[str] = _config.theme_static_paths
THEME_TEMPLATES_OVERRIDES: list[str] = _config.theme_templates_overrides
TIMEZONE: str = _config.timezone
TRANSLATION_FEED_ATOM: str | None = _config.translation_feed_atom
TRANSLATION_FEED_ATOM_URL: str | None = _config.translation_feed_atom_url
TRANSLATION_FEED_RSS: str | None = _config.translation_feed_rss
TRANSLATION_FEED_RSS_URL: str | None = _config.translation_feed_rss_url
TWITTER_USERNAME: str | None = _config.twitter_username
TYPOGRIFY: bool = _config.typogrify
TYPOGRIFY_DASHES: str = _config.typogrify_dashes
TYPOGRIFY_IGNORE_TAGS: list[str] = _config.typogrify_ignore_tags
TYPOGRIFY_OMIT_FILTERS: list[str] = _config.typogrify_omit_filters
USE_FOLDER_AS_CATEGORY: bool = _config.use_folder_as_category
WITH_FUTURE_DATES: bool = _config.with_future_dates
YEAR_ARCHIVE_SAVE_AS: str = _config.year_archive_save_as
YEAR_ARCHIVE_URL: str = _config.year_archive_url
