import shutil
import subprocess
from collections.abc import Generator
from pathlib import Path
from unittest import mock

import pytest
import tomlkit

from turbopelican._commands.init.config import (
    HandleDefaultsMode,
    InputMode,
    TurboConfiguration,
    Verbosity,
)
from turbopelican._commands.init.create import (
    generate_repository,
    update_pyproject,
    update_website,
    uv_sync,
)


@pytest.fixture
def mock_shutil_which_uv() -> Generator[None, None, None]:
    """Mocks out `shutil.which` to return a path."""
    with mock.patch.object(shutil, "which", mock.Mock(return_value="/usr/bin/uv")):
        yield


@pytest.fixture
def mock_shutil_which_uv_missing() -> Generator[None, None, None]:
    """Mocks out `shutil.which` to return `None`."""
    with mock.patch.object(shutil, "which", mock.Mock(return_value=None)):
        yield


@pytest.fixture
def mock_subprocess_run() -> Generator[mock.Mock, None, None]:
    """Mocks out `subprocess.run`."""
    with mock.patch.object(subprocess, "run") as mock_subprocess_run:
        yield mock_subprocess_run


@pytest.mark.usefixtures("mock_shutil_which_uv")
def test_uv_sync(mock_subprocess_run: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.NORMAL)
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/uv", "sync"],
        check=True,
        cwd=Path(),
    )


@pytest.mark.usefixtures("mock_shutil_which_uv")
def test_uv_sync_quiet(mock_subprocess_run: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.QUIET)
    mock_subprocess_run.assert_called_once_with(
        ["/usr/bin/uv", "sync", "--quiet"],
        check=True,
        cwd=Path(),
    )


@pytest.mark.usefixtures("mock_shutil_which_uv_missing")
def test_uv_sync_missing(mock_subprocess_run: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.NORMAL)
    mock_subprocess_run.assert_not_called()


def test_generate_repository_bad_directory(tmp_path: Path) -> None:
    """Tests that the appropriate error is raised when an invalid directory is given.

    Args:
        tmp_path: A temporary and empty directory.
    """
    with pytest.raises(FileNotFoundError):
        generate_repository(tmp_path / "inextant" / "myrepo", verbosity=Verbosity.QUIET)


@pytest.mark.usefixtures("mock_subprocess_run")
def test_generate_repository_new_folder(tmp_path: Path) -> None:
    """Tests that the repository can be generated successfully, creating a new folder.

    Args:
        tmp_path: A temporary and empty directory.
    """
    path_to_repo = tmp_path / "myrepo"
    generate_repository(path_to_repo, verbosity=Verbosity.NORMAL)
    assert (path_to_repo / "turbopelican.toml").exists()


@pytest.mark.usefixtures("mock_subprocess_run")
def test_generate_repository_empty_folder(tmp_path: Path) -> None:
    """Tests that the repository can be generated successfully in an empty folder.

    Args:
        tmp_path: A temporary and empty directory.
    """
    path_to_repo = tmp_path / "myrepo"
    path_to_repo.mkdir()
    generate_repository(path_to_repo, verbosity=Verbosity.NORMAL)
    assert (path_to_repo / "turbopelican.toml").exists()


def test_update_website(tmp_path: Path) -> None:
    """Checks that `turbopelican.toml` is updated appropraitely.

    Args:
        tmp_path: A temporary and empty directory.
    """
    path_to_repo = tmp_path / "myrepo"
    path_to_repo.mkdir()
    path_to_toml = path_to_repo / "turbopelican.toml"
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

    config = TurboConfiguration(
        directory=path_to_repo,
        author="Bob",
        site_name="Bob's website",
        timezone="Antarctica/Troll",
        default_lang="ru",
        site_url="https://hellothere.github.io",
        verbosity=Verbosity.NORMAL,
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    update_website(config)

    with path_to_toml.open(encoding="utf8") as read_toml:
        toml = tomlkit.load(read_toml)

    assert toml.get("pelican", {}).get("author") == "Bob"
    assert toml.get("pelican", {}).get("sitename") == "Bob's website"
    assert toml.get("pelican", {}).get("timezone") == "Antarctica/Troll"
    assert toml.get("pelican", {}).get("default_lang") == "ru"
    assert toml.get("publish", {}).get("site_url") == "https://hellothere.github.io"


def test_update_pyproject(tmp_path: Path) -> None:
    """Checks that the project can be udpated appropriately.

    Args:
        tmp_path: A temporary and empty directory.
    """
    path_to_repo = tmp_path / "bobs_website"
    path_to_repo.mkdir()
    path_to_toml = path_to_repo / "pyproject.toml"
    with path_to_toml.open("w", encoding="utf8") as write_toml:
        write_toml.write(
            """
            [project]
            name = "somename"
            """,
        )

    update_pyproject(path_to_repo)

    with path_to_toml.open(encoding="utf8") as read_toml:
        toml = tomlkit.load(read_toml)

    assert toml.get("project", {}).get("name") == "bobswebsite"
