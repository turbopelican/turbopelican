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
    "EXTRA_PATH_METADATA",
    "FEED_ALL_ATOM",
    "INDEX_SAVE_AS",
    "LINKS",
    "PAGE_PATHS",
    "PAGE_SAVE_AS",
    "PATH",
    "SITENAME",
    "SITEURL",
    "SOCIAL",
    "STATIC_PATHS",
    "THEME",
    "TIMEZONE",
    "TRANSLATION_FEED_ATOM",
]

from turbopelican import load_config

_config = load_config().pelican

ARTICLE_PATHS: list[str] = _config.article_paths
AUTHOR: str = _config.author
AUTHOR_FEED_ATOM: None = None
AUTHOR_FEED_RSS: None = None
CATEGORY_FEED_ATOM: None = None
DEFAULT_LANG: str = _config.default_lang
DEFAULT_PAGINATION: bool = _config.default_pagination
EXTRA_PATH_METADATA: dict[str, dict[str, str]] = _config.extra_path_metadata
FEED_ALL_ATOM: None = None
INDEX_SAVE_AS: str = _config.index_save_as
LINKS: tuple[tuple[str, str], ...] = _config.links
PAGE_PATHS: list[str] = _config.page_paths
PAGE_SAVE_AS: str = _config.page_save_as
PATH: str = _config.path
SITENAME: str = _config.sitename
SITEURL: str = ""
SOCIAL: tuple[tuple[str, str], ...] = _config.social
STATIC_PATHS: list[str] = _config.static_paths
THEME: str = _config.theme
TIMEZONE: str = _config.timezone
TRANSLATION_FEED_ATOM: None = None
