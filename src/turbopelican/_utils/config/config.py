"""This module allows the user to load the turbopelican cofiguration quickly.

Author: Elliot Simpson.
"""

from __future__ import annotations

__all__ = [
    "PelicanConfig",
    "config",
]

from enum import StrEnum
from typing import TYPE_CHECKING, Literal, NoReturn, TypeVar

import pydantic

from turbopelican._utils.errors.errors import TurbopelicanError
from turbopelican._utils.shared import Toml, find_config

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T", bound=Toml)

Links = pydantic.RootModel[tuple[tuple[str, str], ...]]
Social = pydantic.RootModel[tuple[tuple[str, str], ...]]
ArticlePaths = pydantic.RootModel[list[str]]
PagePaths = pydantic.RootModel[list[str]]
ExtraPathMetadata = pydantic.RootModel[dict[str, dict[str, str]]]
StaticPaths = pydantic.RootModel[list[str]]


class PelicanConfig(pydantic.BaseModel):
    """The configuration passed to Turbopelican."""

    article_paths: list[str] = pydantic.Field(default_factory=[""].copy)
    author: str | None = None
    author_feed_atom: str | None = "feeds/{slug}.atom.xml"
    author_feed_rss: str | None = "feeds/{slug}.rss.xml"
    category_feed_atom: str | None = "feeds/{slug}.atom.xml"
    default_lang: str = "en"
    default_pagination: int | Literal[False] = False
    delete_output_directory: bool = False
    extra_path_metadata: dict[str, dict[str, str]] = pydantic.Field(
        default_factory=dict
    )
    feed_all_atom: str | None = "feeds/all.atom.xml"
    index_save_as: str = "index.html"
    links: tuple[tuple[str, str], ...] = ()
    page_paths: list[str] = pydantic.Field(default_factory=["pages"].copy)
    page_save_as: str = "pages/{slug}.html"
    path: str = "."
    relative_urls: bool = False
    site_url: str = ""
    sitename: str = "A Pelican Blog"
    social: tuple[tuple[str, str], ...] = ()
    static_paths: list[str] = pydantic.Field(default_factory=["images"].copy)
    theme: str = "notmyidea"
    timezone: str = "UTC"
    translation_feed_atom: str | None = "feeds/all-{lang}.atom.xml"

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

    @pydantic.field_validator("links", mode="after")
    @classmethod
    def _validate_links(cls, v: tuple) -> tuple[tuple[str, str], ...]:
        """Validate the `links` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        Links.model_validate(v)
        return v

    @pydantic.field_validator("social", mode="after")
    @classmethod
    def _validate_social(cls, v: tuple) -> tuple[tuple[str, str], ...]:
        """Validate the `social` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        Social.model_validate(v)
        return v

    @pydantic.field_validator("article_paths", mode="after")
    @classmethod
    def _validate_article_paths(cls, v: list) -> list[str]:
        """Validate the `article_paths` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        ArticlePaths.model_validate(v)
        return v

    @pydantic.field_validator("page_paths", mode="after")
    @classmethod
    def _validate_page_paths(cls, v: list) -> list[str]:
        """Validate the `page_paths` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        PagePaths.model_validate(v)
        return v

    @pydantic.field_validator("static_paths", mode="after")
    @classmethod
    def _validate_static_paths(cls, v: list) -> list[str]:
        """Validate the `static_paths` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        StaticPaths.model_validate(v)
        return v

    @pydantic.field_validator("extra_path_metadata", mode="after")
    @classmethod
    def _validate_extra_path_metadata(cls, v: dict) -> dict[str, dict[str, str]]:
        """Validate the `extra_path_metadata` field.

        Args:
            v: The input value.

        Returns:
            The input value unchanged.
        """
        ExtraPathMetadata.model_validate(v)
        return v


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
