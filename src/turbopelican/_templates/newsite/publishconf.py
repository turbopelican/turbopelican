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

from turbopelican import load_config

_base_config = load_config()
_config = _base_config.pelican
_publish_config = _base_config.publish


ARTICLE_PATHS: list[str] = _config.article_paths
AUTHOR: str = _config.author
AUTHOR_FEED_ATOM: None = None
AUTHOR_FEED_RSS: None = None
CATEGORY_FEED_ATOM: str = _publish_config.category_feed_atom
DEFAULT_LANG: str = _config.default_lang
DEFAULT_PAGINATION: bool = _config.default_pagination
DELETE_OUTPUT_DIRECTORY: bool = _publish_config.delete_output_directory
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = _config.extra_path_metadata
FEED_ALL_ATOM: str = _publish_config.feed_all_atom
INDEX_SAVE_AS: str = _config.index_save_as
LINKS: tuple[tuple[str, str], ...] = _config.links
PAGE_PATHS: list[str] = _config.page_paths
PAGE_SAVE_AS: str = _config.page_save_as
PATH: str = _config.path
RELATIVE_URLS: bool = _publish_config.relative_urls
SITENAME: str = _config.sitename
SITEURL: str = _publish_config.site_url
SOCIAL: tuple[tuple[str, str], ...] = _config.social
STATIC_PATHS: list[str] = _config.static_paths
THEME: str = _config.theme
TIMEZONE: str = _config.timezone
TRANSLATION_FEED_ATOM: None = None
