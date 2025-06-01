from pathlib import Path

import pydantic
import pytest

from turbopelican import PelicanConfig, TurbopelicanError, config
from turbopelican._utils.config.config import (
    _CombinedConfig,
    _handle_validation_error,
    _validate_datetime,
    _validate_list_of_regex_substitutions,
    _validate_list_of_strings,
    _validate_tuple_of_title_url_pairs,
    _validate_twice_nested_dict,
)


def test_validate_tuple_of_title_url_pairs() -> None:
    """Tests the validator for tuples of title/URL pairs."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        _validate_tuple_of_title_url_pairs(((1, 2),))
    _validate_tuple_of_title_url_pairs((("a", "b"),))


def test_pelicanconfig_validate_list_of_strings() -> None:
    """Tests the validator for lists of strings."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        _validate_list_of_strings([1, 2])
    _validate_list_of_strings(["1", "2"])


def test_pelicanconfig_validate_twice_nested_dict() -> None:
    """Tests the validator for twice-nested dictionaires."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid string"
    ):
        _validate_twice_nested_dict({1.2: {"a": "b"}})
    _validate_twice_nested_dict({"1": {"a": "b"}})


def test_pelicanconfig_validate_list_of_regex_substitutions() -> None:
    """Tests the validator for lists of regular expression substitutions."""
    with pytest.raises(pydantic.ValidationError, match="Input should be a valid tuple"):
        _validate_list_of_regex_substitutions([("a", "b"), "c"])
    _validate_list_of_regex_substitutions([("a", "b"), ("c", "d")])


def test_pelicanconfig_validate_datetime() -> None:
    """Tests the validator for datetimes."""
    with pytest.raises(
        pydantic.ValidationError, match="Input should be a valid integer"
    ):
        _validate_datetime((1, 2, 3.1))
    _validate_datetime((1, 2, 3))


def test_pelicanconfig_default_regex_substitutions() -> None:
    """Tests that regular expression substitutions are defaulted correctly."""
    assert PelicanConfig._default_regex_substitutions({}) == {}
    assert PelicanConfig._default_regex_substitutions(
        {"SLUG_REGEX_SUBSTITUTIONS": [("a", "b")], "TAG_REGEX_SUBSTITUTIONS": []}
    ) == {
        "AUTHOR_REGEX_SUBSTITUTIONS": [("a", "b")],
        "CATEGORY_REGEX_SUBSTITUTIONS": [("a", "b")],
        "SLUG_REGEX_SUBSTITUTIONS": [("a", "b")],
        "TAG_REGEX_SUBSTITUTIONS": [],
    }


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
