"""This module allows the user to load the turbopelican cofiguration quickly.

Author: Elliot Simpson.
"""

from __future__ import annotations

__all__ = [
    "PelicanConfig",
    "config",
]

import importlib
import logging
from collections.abc import Callable
from enum import StrEnum
from typing import TYPE_CHECKING, Annotated, Any, Literal, NoReturn, TypeVar

import pydantic

from turbopelican._utils.errors.errors import TurbopelicanError
from turbopelican._utils.shared import Toml, find_config

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T", bound=Toml)

GlobalAny = Any


class DeploymentType(StrEnum):
    """The deployment settings to be used."""

    DEV = "DEV"
    PUBLISH = "PUBLISH"


def _default_markdown() -> dict:
    return {
        "extension_configs": {
            "markdown.extensions.codehilite": {"css_class": "highlight"},
            "markdown.extensions.extra": {},
            "markdown.extensions.meta": {},
        },
        "output_format": "html5",
    }


def _default_paginated_templates() -> dict[str, int | None]:
    return {"index": None, "tag": None, "category": None, "author": None}


def _validate_tuple_of_title_url_pairs(value: tuple) -> tuple[tuple[str, str]]:
    """Raises an error if field is not a tuple with any number of title/URL pairs.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[tuple[tuple[str, str], ...]].model_validate(value)
    return value


def _validate_list_of_strings(value: list) -> list[str]:
    """Raises an error if field is not a list of strings.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[list[str]].model_validate(value)
    return value


def _validate_twice_nested_dict(value: dict) -> dict[str, dict[str, str]]:
    """Raises an error if field is not a twice-nested dict with string keys/values.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, dict[str, str]]].model_validate(value)
    return value


def _validate_list_of_regex_substitutions(value: list) -> list[tuple[str, str]]:
    """Raises an error if field is not a list of tuples, each containing two strings.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[list[tuple[str, str]]].model_validate(value)
    return value


def _validate_datetime(value: str | tuple | None) -> str | tuple[int, ...] | None:
    """Raises an error if field is not a string, tuple of integers, or None.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[str | tuple[int, ...] | None].model_validate(value)
    return value


def _validate_date_formats(value: dict) -> dict[str, str | tuple[str, str]]:
    """Raises an error if the field is not a date format dictionary.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, str | tuple[str, str]]].model_validate(value)
    return value


def _validate_string_dict(value: dict) -> dict[str, str]:
    """Raises an error if the field is not a dictionary with string values.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, str]].model_validate(value)
    return value


def _validate_locale(value: str | list) -> str | list[str]:
    """Raises an error if the field is not a valid locale field.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[str | list[str]].model_validate(value)
    return value


def _validate_paginated_templates(value: dict) -> dict[str, int | None]:
    """Raises an error if the field is not a valid paginated templates field.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """

    class _PaginatedTemplates(pydantic.BaseModel, extra="forbid"):
        """Allows validation of `PAGINATED_TEMPLATES`."""

        index: int | None = None
        tag: int | None = None
        category: int | None = None
        author: int | None = None

    _PaginatedTemplates.model_validate(value, strict=True)
    return value


def _validate_pagination_patterns(value: list) -> list[tuple[int, str, str]]:
    """Raises an error if the field is not a valid pagination patterns field.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[list[tuple[int, str, str]]].model_validate(value)
    return value


def _validate_log_filter(value: list) -> list[tuple[int, str]]:
    """Raises an error if the field is not a valid log filter field.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[list[tuple[int, str]]].model_validate(value)
    return value


def _validate_dict_of_functions(value: dict) -> dict[str, Callable]:
    """Raises an error if the field is not a dictionary with function values.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, Callable]].model_validate(value)
    return value


def _validate_dict_of_nullable_functions(value: dict) -> dict[str, Callable | None]:
    """Raises an error if the field is not a dictionary with nullable function values.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, Callable | None]].model_validate(value)
    return value


def _validate_dict_of_functions_and_names(value: dict) -> dict[str, Callable | str]:
    """Raises an error if the field is not a dictionary with function/string values.

    Args:
        value: The provided field to be validated.

    Returns:
        The value unchanged.
    """
    pydantic.RootModel[dict[str, Callable | str]].model_validate(value)
    return value


_TupleOfTitleURLPairs = Annotated[
    tuple[tuple[str, str], ...],
    pydantic.AfterValidator(_validate_tuple_of_title_url_pairs),
]
_ListOfStrings = Annotated[
    list[str], pydantic.AfterValidator(_validate_list_of_strings)
]
_TwiceNestedDict = Annotated[
    dict[str, dict[str, str]], pydantic.AfterValidator(_validate_twice_nested_dict)
]
_ListOfRegexSubstitutions = Annotated[
    list[tuple[str, str]],
    pydantic.AfterValidator(_validate_list_of_regex_substitutions),
]
_Datetime = Annotated[
    str | tuple[int, ...] | None, pydantic.AfterValidator(_validate_datetime)
]
_DateFormats = Annotated[
    dict[str, str | tuple[str, str]], pydantic.AfterValidator(_validate_date_formats)
]
_StringDict = Annotated[dict[str, str], pydantic.AfterValidator(_validate_string_dict)]
_Locale = Annotated[str | list[str], pydantic.AfterValidator(_validate_locale)]
_PaginatedTemplates = Annotated[
    dict[str, int | None], pydantic.AfterValidator(_validate_paginated_templates)
]
_PaginationPatterns = Annotated[
    list[tuple[int, str, str]], pydantic.AfterValidator(_validate_pagination_patterns)
]
_LogFilter = Annotated[
    list[tuple[int, str]], pydantic.AfterValidator(_validate_log_filter)
]
_DictOfFunctions = Annotated[
    dict[str, Callable], pydantic.AfterValidator(_validate_dict_of_functions)
]
_DictOfNullableFunctions = Annotated[
    dict[str, Callable | None],
    pydantic.AfterValidator(_validate_dict_of_nullable_functions),
]
_DictOfFunctionsAndNames = Annotated[
    dict[str, Callable | str],
    pydantic.AfterValidator(_validate_dict_of_functions_and_names),
]


class PelicanConfig(pydantic.BaseModel):
    """The configuration passed to Turbopelican."""

    analytics: str | None = None
    archives_save_as: str = "archives.html"
    article_excludes: _ListOfStrings = pydantic.Field(default_factory=list)
    article_lang_save_as: str = "{slug}-{lang}.html"
    article_lang_url: str = "{slug}-{lang}.html"
    article_order_by: str = "reversed-date"
    article_paths: _ListOfStrings = pydantic.Field(default_factory=[""].copy)
    article_save_as: str = "{slug}.html"
    article_translation_id: str | Literal[False] | None = "slug"
    article_url: str = "{slug}.html"
    author: str | None = None
    authors_save_as: str = "authors.html"
    author_feed_atom: str | None = "feeds/{slug}.atom.xml"
    author_feed_atom_url: str | None = None
    author_feed_rss: str | None = "feeds/{slug}.rss.xml"
    author_feed_rss_url: str | None = None
    author_regex_substitutions: _ListOfRegexSubstitutions = pydantic.Field(
        default_factory=[
            (r"[^\\w\\s-]", ""),
            (r"(?u)\\A\\s*", ""),
            (r"(?u)\\s*\\Z", ""),
            (r"[-\\s]+", "-"),
        ].copy
    )
    author_save_as: str = "author/{slug}.html"
    author_url: str = "author/{slug}.html"
    bind: str = "127.0.0.1"
    cache_content: bool = False
    cache_path: str = "cache"
    categories_save_as: str = "categories.html"
    category_feed_atom: str | None = "feeds/{slug}.atom.xml"
    category_feed_atom_url: str | None = None
    category_feed_rss: str | None = None
    category_feed_rss_url: str | None = None
    category_regex_substitutions: _ListOfRegexSubstitutions = pydantic.Field(
        default_factory=[
            (r"[^\\w\\s-]", ""),
            (r"(?u)\\A\\s*", ""),
            (r"(?u)\\s*\\Z", ""),
            (r"[-\\s]+", "-"),
        ].copy
    )
    category_save_as: str = "category/{slug}.html"
    category_url: str = "category/{slug}.html"
    check_modified_method: str = "mtime"
    content_caching_layer: str = "reader"
    css_file: str = "main.css"
    date_formats: _DateFormats = pydantic.Field(default_factory=dict)
    day_archive_save_as: str = ""
    day_archive_url: str = ""
    default_category: str = "misc"
    default_date: _Datetime = None
    default_date_format: str = "%a %d %B %Y"
    default_lang: str = "en"
    default_metadata: dict = pydantic.Field(default_factory=dict)
    default_orphans: int = 0
    default_pagination: int | Literal[False] = False
    delete_output_directory: bool = False
    direct_templates: _ListOfStrings = pydantic.Field(
        default_factory=["index", "tags", "categories", "authors", "archives"].copy
    )
    display_categories_on_menu: bool = True
    display_pages_on_menu: bool = True
    disqus_sitename: str | None = None
    docutils_settings: dict = pydantic.Field(default_factory=dict)
    draft_lang_save_as: str = "drafts/{slug}-{lang}.html"
    draft_lang_url: str = "drafts/{slug}-{lang}.html"
    draft_page_lang_save_as: str = "drafts/pages/{slug}-{lang}.html"
    draft_page_lang_url: str = "drafts/pages/{slug}-{lang}.html"
    draft_page_save_as: str = "drafts/pages/{slug}.html"
    draft_page_url: str = "drafts/pages/{slug}.html"
    draft_save_as: str = "drafts/{slug}.html"
    draft_url: str = "drafts/{slug}.html"
    extra_path_metadata: _TwiceNestedDict = pydantic.Field(default_factory=dict)
    feed_all_atom: str | None = "feeds/all.atom.xml"
    feed_all_atom_url: str | None = None
    feed_all_rss: str | None = None
    feed_all_rss_url: str | None = None
    feed_append_ref: bool = False
    feed_atom: str | None = None
    feed_atom_url: str | None = None
    feed_domain: str = ""
    feed_max_items: int | None = 100
    feed_rss: str | None = None
    feed_rss_url: str | None = None
    filename_metadata: str = r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)"
    formatted_fields: _ListOfStrings = pydantic.Field(default_factory=["summary"].copy)
    github_url: str | None = None
    gzip_cache: bool = True
    ignore_files: _ListOfStrings = pydantic.Field(default_factory=["**/.*"].copy)
    index_save_as: str = "index.html"
    intrasite_link_regex: str = "[{|](?P<what>.*?)[|}]"
    jinja_environment: dict = pydantic.Field(
        default_factory={
            "extensions": [],
            "trim_blocks": True,
            "lstrip_blocks": True,
        }.copy
    )
    jinja_filters: _DictOfFunctions = pydantic.Field(default_factory=dict)
    jinja_globals: dict = pydantic.Field(default_factory=dict)
    jinja_tests: _DictOfFunctions = pydantic.Field(default_factory=dict)
    links: _TupleOfTitleURLPairs = ()
    links_widget_name: str | None = None
    load_content_cache: bool = False
    locale: _Locale = pydantic.Field(default_factory=[""].copy)
    log_filter: _LogFilter = pydantic.Field(default_factory=list)
    markdown: dict = pydantic.Field(default_factory=_default_markdown)
    menuitems: _TupleOfTitleURLPairs = ()
    month_archive_save_as: str = ""
    month_archive_url: str = ""
    newest_first_archives: bool = True
    output_path: str = "output"
    output_retention: _ListOfStrings = pydantic.Field(default_factory=list)
    output_sources: bool = False
    output_sources_extension: str = ".text"
    page_excludes: _ListOfStrings = pydantic.Field(default_factory=list)
    page_lang_save_as: str = "pages/{slug}-{lang}.html"
    page_lang_url: str = "pages/{slug}-{lang}.html"
    page_order_by: str = "basename"
    page_paths: _ListOfStrings = pydantic.Field(default_factory=["pages"].copy)
    page_save_as: str = "pages/{slug}.html"
    page_translation_id: str | Literal[False] | None = "slug"
    page_url: str = "pages/{slug}.html"
    paginated_templates: _PaginatedTemplates = pydantic.Field(
        default_factory=_default_paginated_templates
    )
    pagination_patterns: _PaginationPatterns = pydantic.Field(
        default_factory=[
            (1, "{name}{extension}", "{name}{extension}"),
            (2, "{name}{number}{extension}", "{name}{number}{extension}"),
        ].copy
    )
    path: str = "."
    path_metadata: str = ""
    plugins: _DictOfFunctionsAndNames = pydantic.Field(default_factory=dict)
    plugin_paths: _ListOfStrings = pydantic.Field(default_factory=list)
    port: int = 8000
    pygments_rst_options: dict = pydantic.Field(default_factory=dict)
    readers: _DictOfNullableFunctions = pydantic.Field(default_factory=dict)
    relative_urls: bool = False
    reverse_category_order: bool = False
    rss_feed_summary_only: bool = True
    site_url: str = ""
    sitename: str = "A Pelican Blog"
    sitesubtitle: str | None = None
    slugify_preserve_case: bool = False
    slugify_source: str = "title"
    slugify_use_unicode: bool = False
    slug_regex_substitutions: _ListOfRegexSubstitutions = pydantic.Field(
        default_factory=[
            (r"[^\\w\\s-]", ""),
            (r"(?u)\\A\\s*", ""),
            (r"(?u)\\s*\\Z", ""),
            (r"[-\\s]+", "-"),
        ].copy
    )
    social: _TupleOfTitleURLPairs = ()
    social_widget_name: str | None = None
    static_check_if_modified: bool = False
    static_create_links: bool = False
    static_excludes: _ListOfStrings = pydantic.Field(default_factory=list)
    static_exclude_sources: bool = True
    static_paths: _ListOfStrings = pydantic.Field(default_factory=["images"].copy)
    stylesheet_url: str | None = None
    summary_end_suffix: str = "…"
    summary_max_length: int | None = 50
    summary_max_paragraphs: int | None = None
    tags_save_as: str = "tags.html"
    tag_feed_atom: str | None = None
    tag_feed_atom_url: str | None = None
    tag_feed_rss: str | None = None
    tag_regex_substitutions: _ListOfRegexSubstitutions = pydantic.Field(
        default_factory=[
            (r"[^\\w\\s-]", ""),
            (r"(?u)\\A\\s*", ""),
            (r"(?u)\\s*\\Z", ""),
            (r"[-\\s]+", "-"),
        ].copy
    )
    tag_save_as: str = "tag/{slug}.html"
    tag_url: str = "tag/{slug}.html"
    template_extensions: _ListOfStrings = pydantic.Field(default_factory=[".html"].copy)
    template_pages: _StringDict = pydantic.Field(default_factory=dict)
    theme: str = "notmyidea"
    theme_static_dir: str = "theme"
    theme_static_paths: _ListOfStrings = pydantic.Field(default_factory=["static"].copy)
    theme_templates_overrides: _ListOfStrings = pydantic.Field(default_factory=list)
    timezone: str = "UTC"
    translation_feed_atom: str | None = "feeds/all-{lang}.atom.xml"
    translation_feed_atom_url: str | None = None
    translation_feed_rss: str | None = None
    translation_feed_rss_url: str | None = None
    twitter_username: str | None = None
    typogrify: bool = False
    typogrify_dashes: str = "default"
    typogrify_ignore_tags: _ListOfStrings = pydantic.Field(default_factory=list)
    typogrify_omit_filters: _ListOfStrings = pydantic.Field(default_factory=list)
    use_folder_as_category: bool = True
    with_future_dates: bool = True
    year_archive_save_as: str = ""
    year_archive_url: str = ""

    @pydantic.field_validator("links", mode="before")
    @classmethod
    def _transform_links(cls, value: list[list[str]]) -> tuple[tuple[str, str], ...]:
        """Transforms the links for use by Pelican.

        Args:
            value: The links in TOML form.

        Returns:
            The links, in a form acceptable to Pelican.
        """
        _links = pydantic.RootModel[list[list[str]]]
        _links.model_validate(value)
        return tuple((title, url) for title, url in value)

    @pydantic.field_validator("social", mode="before")
    @classmethod
    def _transform_social(cls, value: list[list[str]]) -> tuple[tuple[str, str], ...]:
        """Transforms the social for use by Pelican.

        Args:
            value: The social in TOML form.

        Returns:
            The social, in a form acceptable to Pelican.
        """
        _social = pydantic.RootModel[list[list[str]]]
        _social.model_validate(value)
        return tuple((title, url) for title, url in value)

    @pydantic.field_validator("log_filter", mode="before")
    @classmethod
    def _transform_log_filter(cls, value: list) -> list[tuple[int, str]]:
        """Transforms the log filter for use by Pelican.

        Args:
            value: The log filter in TOML form.

        Returns:
            The log filter, in a form acceptable to Pelican.
        """
        log_mapping = {
            "WARNING": logging.WARNING,
            "WARN": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "NOTSET": logging.NOTSET,
        }
        _log_filter = pydantic.RootModel[list[tuple[str | int, str]]]
        _log_filter.model_validate(value)
        final_value = []
        for level, msg in value:
            final_value.append((log_mapping.get(level, level), msg))
        return final_value

    @classmethod
    def _transform_single_extra_path_metadata(
        cls, metadata: dict[str, str]
    ) -> dict[str, str]:
        """Transforms a single extra path metadata item for use by Pelican.

        Args:
            metadata: The metadata to be transformed.

        Returns:
            The metadata without the `origin`.
        """
        return {key: value for key, value in metadata.items() if key != "origin"}

    @pydantic.field_validator("extra_path_metadata", mode="before")
    @classmethod
    def _transform_extra_path_metadata(
        cls, value: list[dict[str, str]]
    ) -> dict[str, dict[str, str]]:
        """Transforms the extra path metadata for use by Pelican.

        Args:
            value: The extra path metadata in TOML form.

        Returns:
            The metadata, extracting `origin` for use as dictionary keys.
        """

        class _ExtraPathMetadata(pydantic.BaseModel):
            """Use to validate the input for `extra_path_metadata`."""

            origin: str

        pydantic.RootModel[list[_ExtraPathMetadata]].model_validate(value)

        transformed = {
            metadata["origin"]: cls._transform_single_extra_path_metadata(metadata)
            for metadata in value
        }

        if len(transformed) != len(value):
            raise TurbopelicanError("Repeated `origin` field in `extra_path_metadata`.")

        return transformed

    @classmethod
    def _default_regex_substitutions(cls, data: object) -> object:
        """Enforces correct defaults for regular expression substitutions.

        Args:
            data: The complete unvalidated data.

        Returns:
            The data, such that if `SLUG_REGEX_SUBSTITUTIONS` was provided, defaults
            `AUTHOR_REGEX_SUBSTITUTIONS`, `CATEGORY_REGEX_SUBSTITIONS` and
            `TAG_REGEX_SUBSTITUTIONS` to `SLUG_REGEX_SUBSTITUTIONS`.
        """
        if not isinstance(data, dict):
            return data

        if "SLUG_REGEX_SUBSTITUTIONS" not in data:
            return data

        for field in [
            "AUTHOR_REGEX_SUBSTITUTIONS",
            "CATEGORY_REGEX_SUBSTITUTIONS",
            "TAG_REGEX_SUBSTITUTIONS",
        ]:
            data.setdefault(field, data["SLUG_REGEX_SUBSTITUTIONS"])

        return data

    @pydantic.model_validator(mode="before")
    @classmethod
    def _regex_substitutions(cls, data: object) -> object:
        """Enforces correct defaults for regular expression substitutions.

        Args:
            data: The complete unvalidated data.

        Returns:
            The data with any modifications necessary. If `SLUG_REGEX_SUBSTITUTIONS` was
            provided, defaults `AUTHOR_REGEX_SUBSTITUTIONS`,
            `CATEGORY_REGEX_SUBSTITIONS` and `TAG_REGEX_SUBSTITUTIONS` to
            `SLUG_REGEX_SUBSTITUTIONS`.
        """
        return cls._default_regex_substitutions(data)


class _ModulePrefixConfig(pydantic.BaseModel):
    """The configuration for identifying a prefix with a module."""

    prefix: str
    module_name: str


_ModulePrefixConfigList = pydantic.RootModel[list[_ModulePrefixConfig]]


class _MetaConfig(pydantic.BaseModel):
    """The configuration for interpreting Pelican configuration."""

    module_prefix: _ModulePrefixConfigList = pydantic.Field(
        default_factory=lambda: _ModulePrefixConfigList([]),
    )


def _parse_sentinel_as_function(data: str, meta_config: _MetaConfig) -> str | Callable:
    """Replaces a string with a function, if appropriate.

    Args:
        data: A string which may or may not need conversion.
        meta_config: The configuration used to interpret Pelican configuration.

    Returns:
        Either the same string that was inputted, or a function.
    """
    for module_prefix in meta_config.module_prefix.root:
        if data.startswith(module_prefix.prefix):
            module = importlib.import_module(module_prefix.module_name)
            return getattr(module, data.removeprefix(module_prefix.prefix))

    return data


def _parse_sentinels(data: object, meta_config: _MetaConfig) -> object:
    """Recursively replaces sentinel values as required.

    Args:
        data: Whatever data still contains any sentinel values.
        meta_config: The configuration used to interpret Pelican configuration.

    Returns:
        The data with sentinel values replaced.
    """
    if isinstance(data, dict):
        return {
            key: _parse_sentinels(value, meta_config) for key, value in data.items()
        }
    if isinstance(data, list):
        return [_parse_sentinels(datum, meta_config) for datum in data]
    if data == -1:
        return None
    if isinstance(data, str):
        return _parse_sentinel_as_function(data, meta_config)
    return data


class _CombinedConfig(pydantic.BaseModel):
    """The complete configuration for both development and publication."""

    pelican: PelicanConfig = pydantic.Field(default_factory=PelicanConfig)
    publish: PelicanConfig

    @pydantic.model_validator(mode="before")
    @classmethod
    def _transform(cls, data: object) -> object:
        """Applies `pelican` settings override missing `publish` settings.

        Args:
            data: The complete unvalidated data.

        Returns:
            The data with any modifications necessary. If a user configures a
            setting in the `pelican` section without specifying it in the
            `publish` section, it should be inferred to be the same.
        """
        if not isinstance(data, dict):
            return data

        meta_config = _MetaConfig.model_validate(data.get("meta", {}))
        data = _parse_sentinels(data, meta_config)

        # Allow Pydantic validation to operate if anything is invalid.
        if not isinstance(data, dict):
            return data
        if "pelican" in data and not isinstance(data["pelican"], dict):
            return data
        if "publish" in data and not isinstance(data["publish"], dict):
            return data

        # Settings missing from the publish configuration fallback to the
        # Pelican configuration settings if provided.
        data["publish"] = {**data.get("pelican", {}), **data.get("publish", {})}
        return data


def _handle_validation_error(exc: pydantic.ValidationError) -> NoReturn:
    """Ensures that only the first configuration error is shown.

    The error is also made more user-friendly for those unfamiliar with
    Pydantic.

    Args:
        exc: The validation exception thrown by Pydantic.

    Raises:
        TurbopelicanError: The configuration is incorrectly formed.
    """
    first_error = exc.errors()[0]
    address = ".".join(map(str, first_error["loc"]))
    message = first_error["msg"]
    raise TurbopelicanError(
        f"Unexpected configuration at: {address}: {message!r}."
    ) from None


def config(
    config_type: DeploymentType | Literal["DEV", "PUBLISH"] = DeploymentType.DEV,
    /,
    *,
    start_path: Path | str = ".",
) -> PelicanConfig:
    """Loads the configuration into a single reusable structure.

    Args:
        config_type: Either DEV or PUBLISH.
        start_path: The path at which to start searching for `pyproject.toml`.

    Returns:
        An instance of the configuration in the appropriate structure.
    """
    raw_config = find_config(start_path)
    try:
        config = _CombinedConfig.model_validate(raw_config)
    except pydantic.ValidationError as exc:
        _handle_validation_error(exc)

    if config_type in {DeploymentType.DEV, "DEV"}:
        return config.pelican

    if config_type in {DeploymentType.PUBLISH, "PUBLISH"}:
        return config.publish

    raise TurbopelicanError(
        f"Incorrect config_type: {config_type}. Must be DEV or PUBLISH."
    )
