"""This module allows the user to load the Turbopelican configuration quickly.

Author: Elliot Simpson.
"""

from __future__ import annotations

__all__ = [
    "Configuration",
    "PelicanConfiguration",
    "PublishConfiguration",
    "load_config",
]

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, TypeVar

from turbopelican._utils.errors.errors import TurbopelicanError
from turbopelican._utils.shared import Toml, find_config

if TYPE_CHECKING:
    from pathlib import Path

T = TypeVar("T", bound=Toml)


@dataclass(frozen=True)
class PelicanConfiguration:
    """The configuration for Pelican. Set irrespective of whether or not publishing.

    Deprecated.
    """

    author: str
    sitename: str
    timezone: str
    default_lang: str
    path: str
    links: tuple[tuple[str, str], ...]
    social: tuple[tuple[str, str], ...]
    default_pagination: bool
    theme: str
    article_paths: list[str]
    page_paths: list[str]
    page_save_as: str
    static_paths: list[str]
    extra_path_metadata: dict[str, dict[str, str]]
    index_save_as: str


@dataclass(frozen=True)
class PublishConfiguration:
    """The configuration for Pelican. Set only when publishing.

    Deprecated.
    """

    site_url: str
    relative_urls: bool
    feed_all_atom: str
    category_feed_atom: str
    delete_output_directory: bool


@dataclass(frozen=True)
class Configuration:
    """The configuration for Pelican.

    Deprecated.
    """

    pelican: PelicanConfiguration
    """Used in all deployments."""

    publish: PublishConfiguration
    """Only used for publishing."""


def _access_setting_cluster(
    config: dict[str, Toml], section_name: str
) -> dict[str, Toml]:
    """Extracts a section of the configuration for further introspection.

    Deprecated.

    Args:
        config: The configuration to be introspected.
        section_name: The name of the section in the configuration to be
            specifically introspected.

    Returns:
        The pertinent section in the config.
    """
    if section_name not in config:
        raise TurbopelicanError(f"Could not find key: {section_name}")

    section = config[section_name]
    if not isinstance(section, dict):
        raise TurbopelicanError(f"Could not find key: {section_name}")
    return section


def _access_setting(expect_type: type[T], config: dict[str, Toml], *keys: str) -> T:
    """Extracts the setting from the settings with the expected type checked.

    Deprecated.

    Args:
        expect_type: The type of the value to be returned.
        config: The configuration to be introspected.
        keys: The combination of keys to be used to divide the configuration.

    Returns:
        The value in the configuration matching the provided keys.
    """
    subset = config

    for key in keys[:-1]:
        if key not in subset:
            raise TurbopelicanError(f"Could not find key: {'.'.join(keys)}")
        value = subset[key]
        if not isinstance(value, dict):
            raise TurbopelicanError(f"Could not find key: {'.'.join(keys)}")
        subset = value

    final_key = keys[-1]
    if final_key not in subset:
        raise TurbopelicanError(f"Could not find key: {'.'.join(keys)}")

    section = subset[final_key]
    if not isinstance(section, expect_type):
        raise TurbopelicanError(
            f"Incorrect type {type(section)} for key: {'.'.join(keys)}"
        )
    return section


class SettingGetter(Protocol):
    """A generic function for getting configuration.

    Deprecated.
    """

    def __call__(self, expect_type: type[T], *keys: str) -> T: ...


class SettingGetterWithFallback(Protocol):
    """A generic function for getting configuration, or failing that, None.

    Deprecated.
    """

    def __call__(self, expect_type: type[T], *keys: str) -> T | None: ...


def _setting_getter(
    config: dict[str, Toml], section_key: str
) -> tuple[SettingGetter, SettingGetterWithFallback]:
    """Creates and returns two functions for obtaining settings.

    Deprecated.

    Args:
        config: The configuration to be introspected.
        section_key: The key for the configuration subsection.

    Returns:
        A tuple containing:
        * A function for getting configuration normally.
        * A function for getting confiugration, or failing that, returning
          None.
    """
    section = _access_setting_cluster(config, section_key)

    def _access_setting_as(expect_type: type[T], *keys: str) -> T:
        """Returns the expected setting.

        Args:
            expect_type: The type of the value to be returned.
            keys: The combination of keys to be used to divide the configuration.

        Returns:
            The value from the settings.
        """
        return _access_setting(expect_type, section, *keys)

    def _access_setting_as_with_fallback(expect_type: type[T], *keys: str) -> T | None:
        """Returns the expected setting, or failing that, returns None.

        Args:
            expect_type: The type of the value to be returned.
            keys: The combination of keys to be used to divide the configuration.

        Returns:
            The value from the settings or if the configuration does not
            exist, None.
        """
        try:
            return _access_setting(expect_type, section, *keys)
        except TurbopelicanError:
            return None

    return _access_setting_as, _access_setting_as_with_fallback


def _get_extract_path_metadata(getter: SettingGetter) -> dict[str, dict[str, str]]:
    """Converts the path metadata into a form acceptable for Pelican.

    Deprecated.

    Args:
        getter: The function to obtain settings.

    Returns:
        The EXTRACT_PATH_METADATA setting.
    """
    return {
        metadata["origin"]: {
            key: value for (key, value) in metadata.items() if key != "origin"
        }
        for metadata in getter(list, "extra_path_metadata")
    }


def load_config(start_path: Path | str = ".") -> Configuration:
    """Loads the configuration into reusable structures.

    Deprecated.

    Args:
        start_path: The path at which to start searching for `pyproject.toml`.

    Returns:
        An instance of the configuration in the appropriate structure.
    """
    warnings.warn(
        "Use `turbopelican.config` instead of `turbopelican.load_config`.",
        DeprecationWarning,
        stacklevel=2,
    )
    config = find_config(start_path)
    pelican_conf_get, pelican_conf_get_fallback = _setting_getter(config, "pelican")
    publish_conf_get, _publish_conf_get_fallback = _setting_getter(config, "publish")

    pelican_links = tuple(map(tuple, pelican_conf_get_fallback(list, "links") or []))
    pelican_social = tuple(map(tuple, pelican_conf_get_fallback(list, "social") or []))

    return Configuration(
        pelican=PelicanConfiguration(
            author=pelican_conf_get(str, "author"),
            sitename=pelican_conf_get(str, "sitename"),
            timezone=pelican_conf_get(str, "timezone"),
            default_lang=pelican_conf_get(str, "default_lang"),
            path=pelican_conf_get(str, "path"),
            links=pelican_links,
            social=pelican_social,
            default_pagination=pelican_conf_get(bool, "default_pagination"),
            theme=pelican_conf_get(str, "theme"),
            article_paths=pelican_conf_get(list, "article_paths"),
            page_paths=pelican_conf_get(list, "page_paths"),
            page_save_as=pelican_conf_get(str, "page_save_as"),
            static_paths=pelican_conf_get(list, "static_paths"),
            extra_path_metadata=_get_extract_path_metadata(pelican_conf_get),
            index_save_as=pelican_conf_get(str, "index_save_as"),
        ),
        publish=PublishConfiguration(
            site_url=publish_conf_get(str, "site_url"),
            relative_urls=publish_conf_get(bool, "relative_urls"),
            feed_all_atom=publish_conf_get(str, "feed_all_atom"),
            category_feed_atom=publish_conf_get(str, "category_feed_atom"),
            delete_output_directory=publish_conf_get(bool, "delete_output_directory"),
        ),
    )
