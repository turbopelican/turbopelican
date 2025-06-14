import shutil
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path
from unittest import mock

import pytest
import tomlkit

from turbopelican._commands.init.config import InitConfiguration
from turbopelican._commands.init.create import (
    _copy_template,
    commit_changes,
    generate_repository,
    update_pyproject,
    uv_sync,
)
from turbopelican._utils.shared.args import (
    HandleDefaultsMode,
    InputMode,
    InstallType,
    Verbosity,
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
def mock_subprocess_popen() -> Generator[mock.Mock, None, None]:
    """Mocks out `subprocess.Popen`."""
    mock_process = mock.Mock()
    mock_process.stderr = None
    mock_process.returncode = 0
    with mock.patch.object(
        subprocess, "Popen", return_value=mock_process
    ) as mock_subprocess_popen:
        yield mock_subprocess_popen


@pytest.fixture
def mock_subprocess_run() -> Generator[mock.Mock, None, None]:
    """Mocks out `subprocess.run`."""
    with mock.patch.object(subprocess, "run") as mock_subprocess_run:
        yield mock_subprocess_run


@pytest.mark.usefixtures("mock_shutil_which_uv")
def test_uv_sync(mock_subprocess_popen: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.NORMAL)
    mock_subprocess_popen.assert_called_once_with(
        ["/usr/bin/uv", "sync"],
        stdout=sys.stdout,
        stderr=subprocess.PIPE,
        cwd=Path(),
        text=True,
        bufsize=1,
    )


@pytest.mark.usefixtures("mock_shutil_which_uv")
def test_uv_sync_quiet(mock_subprocess_popen: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.QUIET)
    mock_subprocess_popen.assert_called_once_with(
        ["/usr/bin/uv", "sync", "--quiet"],
        stdout=sys.stdout,
        stderr=subprocess.PIPE,
        cwd=Path(),
        text=True,
        bufsize=1,
    )


@pytest.mark.usefixtures("mock_shutil_which_uv_missing")
def test_uv_sync_missing(mock_subprocess_run: mock.Mock) -> None:
    """Tests that repository is synced appropriately."""
    uv_sync(Path(), verbosity=Verbosity.NORMAL)
    mock_subprocess_run.assert_not_called()


@pytest.fixture
def config(tmp_path: Path) -> InitConfiguration:
    return InitConfiguration(
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


def test_copy_template(tmp_path: Path) -> None:
    """Tests that a template can be copied successfully.

    Args:
        tmp_path: A temporary and empty directory.
    """
    copy_to = tmp_path / "copy_here"
    copy_to.mkdir()
    _copy_template(copy_to, "newsite")
    path_to_conf = copy_to / "pelicanconf.py"
    original_text = path_to_conf.read_text()
    _copy_template(copy_to, "minimal")
    assert path_to_conf.read_text() != original_text
    assert (copy_to / "turbopelican.toml").exists()


def test_generate_repository_bad_directory(config: InitConfiguration) -> None:
    """Tests that the appropriate error is raised when an invalid directory is given.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    config.directory = config.directory / "inextant" / "myrepo"
    with pytest.raises(FileNotFoundError):
        generate_repository(config)


def test_generate_repository_not_a_directory(config: InitConfiguration) -> None:
    """Tests that the appropriate error is raised when a non-directory is given.

    Args:
        config: The configuration for Turbopelican. Supplied via fixture.
    """
    config.directory = config.directory / "myfile"
    config.directory.touch()
    with pytest.raises(NotADirectoryError):
        generate_repository(config)


def test_generate_repository_not_empty(config: InitConfiguration) -> None:
    """Tests that the appropriate error is raised when a non-empty directory is given.

    Args:
        config: The configuration for Turbopelican. Supplied via fixture.
    """
    config.directory = config.directory / "myrepo"
    config.directory.mkdir()
    (config.directory / "hello-world.txt").touch()
    with pytest.raises(RuntimeError):
        generate_repository(config)


@pytest.mark.usefixtures("mock_subprocess_run")
def test_generate_repository_new_folder(config: InitConfiguration) -> None:
    """Tests that the repository can be generated successfully, creating a new folder.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    config.directory = config.directory / "myrepo"
    generate_repository(config)
    assert (config.directory / "turbopelican.toml").exists()


@pytest.mark.usefixtures("mock_subprocess_run")
def test_generate_repository_empty_folder(config: InitConfiguration) -> None:
    """Tests that the repository can be generated successfully in an empty folder.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    config.directory = config.directory / "myrepo"
    config.directory.mkdir()
    generate_repository(config)
    assert (config.directory / "turbopelican.toml").exists()


def test_update_pyproject(tmp_path: Path) -> None:
    """Checks that the project can be updated appropriately.

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


def test_commit_changes(config: InitConfiguration) -> None:
    """Checks that changes can be committed successfully.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    git_path = shutil.which("git")
    assert git_path
    subprocess.run([git_path, "init"], check=True, cwd=config.directory)
    (config.directory / "commit-me.txt").touch()
    commit_changes(config)
    subprocess.run(
        [git_path, "rev-parse", "--is-empty-tree", "HEAD"],
        check=True,
        cwd=config.directory,
    )


def test_commit_changes_no_commit(config: InitConfiguration) -> None:
    """Checks that changes are not configured if Turbopelican instructed not to commit.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
    """
    config.commit_changes = False
    git_path = shutil.which("git")
    assert git_path
    subprocess.run([git_path, "init"], check=True, cwd=config.directory)
    (config.directory / "commit-me.txt").touch()
    commit_changes(config)
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [git_path, "rev-parse", "--is-empty-tree", "HEAD"],
            check=True,
            cwd=config.directory,
        )


@pytest.mark.parametrize("setting", ["user.name", "user.email"])
def test_commit_changes_bad_git_config(config: InitConfiguration, setting: str) -> None:
    """Checks that appropriate error is raised if git is not configured correctly.

    Args:
        config: The configuration for Turbopelican. Suppied via fixture.
        setting: The name of the setting to mangle. Supplied via parameterization.
    """
    git_path = shutil.which("git")
    assert git_path
    subprocess.run([git_path, "init"], check=True, cwd=config.directory)
    subprocess.run([git_path, "config", setting, " "], check=True, cwd=config.directory)
    (config.directory / "commit-me.txt").touch()
    with pytest.raises(RuntimeError):
        commit_changes(config)
