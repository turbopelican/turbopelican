from pathlib import Path
from unittest import mock

import pydantic
import pytest

from turbopelican import (
    Configuration,
    PelicanConfig,
    PelicanConfiguration,
    PublishConfiguration,
    TurbopelicanError,
    config,
    load_config,
)
from turbopelican._utils.config.config import (
    _access_setting,
    _access_setting_cluster,
    _CombinedConfig,
    _get_extract_path_metadata,
    _handle_validation_error,
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


def test_pelicanconfig() -> None:
    """Tests that providing no fields is the same as using the defaults."""
    assert PelicanConfig.model_validate({}) == PelicanConfig()


def test_pelicanconfig_transform_social() -> None:
    """Tests that social can be transformed for use by Pelican."""
    assert PelicanConfig._transform_social([["a", "b"], ["c", "d"]]) == (
        ("a", "b"),
        ("c", "d"),
    )


def test_pelicanconfig_transform_links() -> None:
    """Tests that links can be transformed for use by Pelican."""
    assert PelicanConfig._transform_links([["a", "b"], ["c", "d"]]) == (
        ("a", "b"),
        ("c", "d"),
    )


def test_pelicanconfig_transform_single_extra_path_metadata() -> None:
    """Tests that an extra path metadata item can be transformed for use by Pelican."""
    assert PelicanConfig._transform_single_extra_path_metadata(
        {"origin": "a", "other": "b"}
    ) == {"other": "b"}


def test_pelicanconfig_transform_extra_path_metadata_success() -> None:
    """Tests that extra path metadata can be transformed for use by Pelican."""
    extra_path_metadata = [{"origin": "a"}, {"origin": "b", "other": "c"}]
    expected = {"a": {}, "b": {"other": "c"}}
    assert PelicanConfig._transform_extra_path_metadata(extra_path_metadata) == expected


def test_pelicanconfig_transform_extra_path_metadata_validation_error() -> None:
    """Tests that invalid extra path metadata is rejected."""
    extra_path_metadata = [{"origin": "a"}, {"other": "c"}]
    with pytest.raises(pydantic.ValidationError, match="origin[\n ]+Field required"):
        PelicanConfig._transform_extra_path_metadata(extra_path_metadata)


def test_pelicanconfig_transform_extra_path_metadata_repeated() -> None:
    """Tests that invalid extra path metadata is rejected."""
    extra_path_metadata = [{"origin": "a"}, {"origin": "a"}]
    with pytest.raises(TurbopelicanError, match="Repeated `origin` field"):
        PelicanConfig._transform_extra_path_metadata(extra_path_metadata)


def test_pelicanconfig_validators() -> None:
    """Tests that the validators are all working."""
    config_dict = {
        "links": [["a", "b"]],
        "social": [["c", "d"]],
        "article_paths": ["e", "f"],
        "static_paths": ["g", "h"],
        "extra_path_metadata": [{"origin": "i", "other": "j"}],
    }
    config = PelicanConfig.model_validate(config_dict)
    expected = PelicanConfig()
    expected.links = (("a", "b"),)
    expected.social = (("c", "d"),)
    expected.article_paths = ["e", "f"]
    expected.static_paths = ["g", "h"]
    expected.extra_path_metadata = {"i": {"other": "j"}}
    assert config == expected


def test_pelicanconfig_validate_links_fail() -> None:
    """Tests that the validator for links blocks bad links."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        PelicanConfig._validate_links(((1, 2),))


def test_pelicanconfig_validate_social_fail() -> None:
    """Tests that the validator for social blocks bad social."""
    with pytest.raises(pydantic.ValidationError, match="Input should be a valid tuple"):
        PelicanConfig._validate_social((1,))


def test_pelicanconfig_validate_article_paths_fail() -> None:
    """Tests that the validator for article paths blocks bad article paths."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        PelicanConfig._validate_article_paths([1, 2])


def test_pelicanconfig_validate_page_paths_fail() -> None:
    """Tests that the validator for page paths blocks bad page paths."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        PelicanConfig._validate_page_paths([{}, {}])


def test_pelicanconfig_validate_static_paths_fail() -> None:
    """Tests that the validator for static paths blocks bad static paths."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        PelicanConfig._validate_static_paths([{}, {}])


def test_pelicanconfig_validate_extra_path_metadata_fail() -> None:
    """Tests that the validator for extra path metadata paths blocks bad metadata."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        PelicanConfig._validate_extra_path_metadata({1.2: {"a": "b"}})


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (-1, None),
        (1, 1),
        ({"a": -1, "b": "c"}, {"a": None, "b": "c"}),
        ([-1, "a"], [None, "a"]),
    ],
)
def test_combinedconfig_nullify_sentinels(value: object, expected: object) -> None:
    """Tests that the sentinels can be nullified."""
    assert _CombinedConfig._nullify_sentinels(value) == expected


def test_combinedconfig_defaults() -> None:
    """Tests that the Pelican settings override missing publication settings."""
    input_config = {
        "pelican": {"author": "Joe", "sitename": "My site"},
        "publish": {"sitename": "Your site", "timezone": "GMT"},
    }
    config = _CombinedConfig.model_validate(input_config)
    assert config.pelican.author == "Joe"
    assert config.pelican.sitename == "My site"
    assert config.pelican.timezone != "GMT"
    assert config.publish.author == "Joe"
    assert config.publish.sitename == "Your site"
    assert config.publish.timezone == "GMT"


def test_handle_validation_error() -> None:
    """Tests that the first configuration error is shown."""
    with pytest.raises(pydantic.ValidationError) as exc:
        PelicanConfig.model_validate({"links": [1], "social": [2]})
    with pytest.raises(TurbopelicanError, match="links.0"):
        _handle_validation_error(exc.value)


def test_config(tmp_path: Path) -> None:
    """Tests that the configuration can be parsed successfully.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "turbopelican.toml").write_text(
        """
        [pelican]
        author = "Fred"
        sitename = "Fred's site"

        [publish]
        sitename = "The site"
        site_url = "https://mysitename.github.io"
        """
    )

    dev_config = config("DEV", start_path=tmp_path)
    assert dev_config.author == "Fred"
    assert dev_config.sitename == "Fred's site"
    assert dev_config.site_url != "https://mysitename.github.io"

    publish_config = config("PUBLISH", start_path=tmp_path)
    assert publish_config.author == "Fred"
    assert publish_config.sitename == "The site"
    assert publish_config.site_url == "https://mysitename.github.io"
