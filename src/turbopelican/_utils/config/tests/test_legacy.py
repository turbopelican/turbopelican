from pathlib import Path
from unittest import mock

import pytest

from turbopelican import (
    Configuration,
    PelicanConfiguration,
    PublishConfiguration,
    TurbopelicanError,
    load_config,
)
from turbopelican._utils.config.legacy import (
    _access_setting,
    _access_setting_cluster,
    _get_extract_path_metadata,
    _setting_getter,
)


def test_access_setting_cluster() -> None:
    """Checks that a section of the config can be extracted successfully."""
    assert _access_setting_cluster({"x": {"y": 1}}, "x") == {"y": 1}


def test_access_setting_cluster_missing() -> None:
    """Checks that an appropriate error is raised when a cluster is missing."""
    with pytest.raises(TurbopelicanError):
        _access_setting_cluster({}, "x")


def test_access_setting_cluster_non_dict() -> None:
    """Checks error is raised when a section of the config isn't parsed as a `dict`."""
    with pytest.raises(TurbopelicanError):
        _access_setting_cluster({"x": [1, 2, 3]}, "x")


def test_access_setting() -> None:
    """Checks that settings can be accessed."""
    assert _access_setting(dict, {"x": {"y": {}}}, "x", "y") == {}


def test_access_setting_missing() -> None:
    """Checks error is raised when settings' parents are missing."""
    with pytest.raises(TurbopelicanError):
        _access_setting(dict, {"x": {}}, "x", "y")


def test_access_setting_non_dict() -> None:
    """Checks error is raised when configuration parents are not instances of `dict`."""
    with pytest.raises(TurbopelicanError):
        _access_setting(dict, {"x": 1}, "x", "y")


def test_access_setting_missing_final() -> None:
    """Checks error is raised when settings are missing."""
    with pytest.raises(TurbopelicanError):
        _access_setting(dict, {"x": {"y": 1}}, "x", "z")


def test_access_setting_final_mismatch() -> None:
    """Checks error is raised when settings are unexpected type."""
    with pytest.raises(TurbopelicanError):
        _access_setting(int, {"x": {"y": "a"}}, "x", "y")


def test_setting_getter() -> None:
    """Checks a function which retrieves settings can be generated."""
    setting_getter, setting_getter_fallback = _setting_getter({"x": {"y": 1}}, "x")
    assert setting_getter(int, "y") == 1
    assert setting_getter_fallback(int, "y") == 1
    with pytest.raises(TurbopelicanError):
        setting_getter(int, "z")
    assert setting_getter_fallback(int, "z") is None


def test_get_extract_path_metadata() -> None:
    """Checks extract path metadata can be transformed for use by Pelican."""
    getter = mock.Mock(return_value=[{"origin": "a", "path": "b"}])
    assert _get_extract_path_metadata(getter) == {"a": {"path": "b"}}


def test_load_config(tmp_path: Path) -> None:
    """Checks that the configuration can be loaded successfully.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "turbopelican.toml").write_text(
        """
        [pelican]
        author = "Fred"
        sitename = "Fred's site"
        timezone = "Antarctica/Troll"
        default_lang = "en"
        path = "content"
        default_pagination = false
        theme = "themes/my-theme"
        article_paths = []
        page_paths = [""]
        page_save_as = "{slug}.html"
        static_paths = ["static"]
        index_save_as = ""

        [[pelican.extra_path_metadata]]
        origin = "static/myasset.png"
        path = "myasset.png"

        [publish]
        site_url = "https://mysitename.github.io"
        relative_urls = false
        feed_all_atom = "feeds/all.atom.xml"
        category_feed_atom = "feeds/{slug}.atom.xml"
        delete_output_directory = true
        """
    )
    with pytest.warns(DeprecationWarning, match="Use `turbopelican.config`"):
        config = load_config(tmp_path)
    assert config == Configuration(
        pelican=PelicanConfiguration(
            author="Fred",
            sitename="Fred's site",
            timezone="Antarctica/Troll",
            default_lang="en",
            path="content",
            links=(),
            social=(),
            default_pagination=False,
            theme="themes/my-theme",
            article_paths=[],
            page_paths=[""],
            page_save_as="{slug}.html",
            static_paths=["static"],
            extra_path_metadata={"static/myasset.png": {"path": "myasset.png"}},
            index_save_as="",
        ),
        publish=PublishConfiguration(
            site_url="https://mysitename.github.io",
            relative_urls=False,
            feed_all_atom="feeds/all.atom.xml",
            category_feed_atom="feeds/{slug}.atom.xml",
            delete_output_directory=True,
        ),
    )
