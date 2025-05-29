"""This module allows the user to load the turbopelican cofiguration quickly.

Author: Elliot Simpson.
"""

from __future__ import annotations

__all__ = [
    "PelicanConfig",
    "config",
]

from enum import StrEnum
from typing import TYPE_CHECKING, Annotated, Literal, NoReturn, TypeVar

import pydantic

from turbopelican._utils.errors.errors import TurbopelicanError
from turbopelican._utils.shared import Toml, find_config

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T", bound=Toml)


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


class PelicanConfig(pydantic.BaseModel):
    """The configuration passed to Turbopelican."""

    archives_save_as: str = "archives.html"
    article_lang_save_as: str = "{slug}-{lang}.html"
    article_lang_url: str = "{slug}-{lang}.html"
    article_order_by: str = "reversed-date"
    article_paths: _ListOfStrings = pydantic.Field(default_factory=[""].copy)
    article_save_as: str = "{slug}.html"
    article_url: str = "{slug}.html"
    author: str | None = None
    authors_save_as: str = "authors.html"
    author_feed_atom: str | None = "feeds/{slug}.atom.xml"
    author_feed_rss: str | None = "feeds/{slug}.rss.xml"
    author_save_as: str = "author/{slug}.html"
    author_url: str = "author/{slug}.html"
    bind: str = "127.0.0.1"
    cache_content: bool = False
    cache_path: str = "cache"
    categories_save_as: str = "categories.html"
    category_feed_atom: str | None = "feeds/{slug}.atom.xml"
    category_save_as: str = "category/{slug}.html"
    category_url: str = "category/{slug}.html"
    check_modified_method: str = "mtime"
    content_caching_layer: str = "reader"
    css_file: str = "main.css"
    day_archive_save_as: str = ""
    day_archive_url: str = ""
    default_category: str = "misc"
    default_date_format: str = "%a %d %B %Y"
    default_lang: str = "en"
    default_pagination: int | Literal[False] = False
    delete_output_directory: bool = False
    display_categories_on_menu: bool = True
    display_pages_on_menu: bool = True
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
    feed_append_ref: bool = False
    filename_metadata: str = r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)"
    gzip_cache: bool = True
    index_save_as: str = "index.html"
    intrasite_link_regex: str = "[{|](?P<what>.*?)[|}]"
    links: _TupleOfTitleURLPairs = ()
    load_content_cache: bool = False
    month_archive_save_as: str = ""
    month_archive_url: str = ""
    newest_first_archives: bool = True
    output_path: str = "output"
    output_sources: bool = False
    output_sources_extension: str = ".text"
    page_lang_save_as: str = "pages/{slug}-{lang}.html"
    page_lang_url: str = "pages/{slug}-{lang}.html"
    page_order_by: str = "basename"
    page_paths: _ListOfStrings = pydantic.Field(default_factory=["pages"].copy)
    page_save_as: str = "pages/{slug}.html"
    page_url: str = "pages/{slug}.html"
    path: str = "."
    path_metadata: str = ""
    relative_urls: bool = False
    reverse_category_order: bool = False
    rss_feed_summary_only: bool = True
    site_url: str = ""
    sitename: str = "A Pelican Blog"
    slugify_preserve_case: bool = False
    slugify_source: str = "title"
    slugify_use_unicode: bool = False
    social: _TupleOfTitleURLPairs = ()
    static_check_if_modified: bool = False
    static_create_links: bool = False
    static_exclude_sources: bool = True
    static_paths: _ListOfStrings = pydantic.Field(default_factory=["images"].copy)
    summary_end_suffix: str = "…"
    tags_save_as: str = "tags.html"
    tag_save_as: str = "tag/{slug}.html"
    tag_url: str = "tag/{slug}.html"
    theme: str = "notmyidea"
    theme_static_dir: str = "theme"
    timezone: str = "UTC"
    translation_feed_atom: str | None = "feeds/all-{lang}.atom.xml"
    typogrify: bool = False
    typogrify_dashes: str = "default"
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


class _CombinedConfig(pydantic.BaseModel):
    """The complete configuration for both development and publication."""

    pelican: PelicanConfig = pydantic.Field(default_factory=PelicanConfig)
    publish: PelicanConfig

    @classmethod
    def _nullify_sentinels(cls, data: object) -> object:
        """Recursively replaces sentinel values with None in dictionaries.

        Args:
            data: Whatever data still contains any sentinel values.

        Returns:
            The data with sentinel values replaced with None.
        """
        if isinstance(data, dict):
            return {key: cls._nullify_sentinels(value) for key, value in data.items()}
        if isinstance(data, list):
            return list(map(cls._nullify_sentinels, data))
        if data == -1:
            return None
        return data

    @pydantic.model_validator(mode="before")
    @classmethod
    def _accept_defaults(cls, data: object) -> object:
        """Applies `pelican` settings override missing `publish` settings.

        Args:
            data: The complete unvalidated data.

        Returns:
            The data with any modifications necessary. If a user configures a
            setting in the `pelican` section without specifying it in the
            `publish` section, it should be inferred to be the same.
        """
        data = cls._nullify_sentinels(data)

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


class DeploymentType(StrEnum):
    """The deployment settings to be used."""

    DEV = "DEV"
    PUBLISH = "PUBLISH"


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
