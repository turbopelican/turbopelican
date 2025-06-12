from pathlib import Path

import pytest
import tomlkit
from freezegun import freeze_time

from turbopelican._utils.shared.args import (
    CreateConfiguration,
    HandleDefaultsMode,
    InputMode,
    InstallType,
    Verbosity,
)
from turbopelican._utils.shared.create import update_contents, update_website


@pytest.fixture
def config(tmp_path: Path) -> CreateConfiguration:
    return CreateConfiguration(
        directory=tmp_path,
        author="Bob",
        site_name="Bob's website",
        timezone="Antarctica/Troll",
        default_lang="ru",
        site_url="https://hellothere.github.io",
        verbosity=Verbosity.NORMAL,
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        install_type=InstallType.FULL_INSTALL,
    )


def test_update_website(config: CreateConfiguration) -> None:
    """Checks that `turbopelican.toml` is updated appropraitely."""
    config.directory = config.directory / "myrepo"
    config.directory.mkdir()
    path_to_toml = config.directory / "turbopelican.toml"
    with path_to_toml.open("w", encoding="utf8") as write_toml:
        write_toml.write(
            """
            [pelican]
            author = "Fred"
            sitename = "Fred's website"
            timezone = "Asia/Tbilisi"
            default_lang = "en"

            [publish]
            site_url = "https://spaghetti.github.io"
            """,
        )

    update_website(config)

    with path_to_toml.open(encoding="utf8") as read_toml:
        toml = tomlkit.load(read_toml)

    assert toml.get("pelican", {}).get("author") == "Bob"
    assert toml.get("pelican", {}).get("sitename") == "Bob's website"
    assert toml.get("pelican", {}).get("timezone") == "Antarctica/Troll"
    assert toml.get("pelican", {}).get("default_lang") == "ru"
    assert toml.get("publish", {}).get("site_url") == "https://hellothere.github.io"


@freeze_time("2011-11-11")
def test_update_contents(config: CreateConfiguration) -> None:
    """Checks that the website contents can be updated appropriately.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    contents_dir = config.directory / "content"
    contents_dir.mkdir()
    first_file = contents_dir / "first-article.md"
    first_file.write_text("Date: {date}")
    second_file = contents_dir / "second-article.md"
    second_file.write_text(
        """
        Other: 1
        Date: {date}
        Something: 2
        """
    )

    update_contents(config)

    assert first_file.read_text() == "Date: 2011-11-11"
    assert second_file.read_text().splitlines()[2].lstrip() == "Date: 2011-11-11"
