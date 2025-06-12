import os
import shutil
import subprocess
from collections.abc import Generator
from pathlib import Path
from unittest import mock

import pytest
import tomlkit

from turbopelican._commands.adorn.config import AdornConfiguration
from turbopelican._commands.adorn.create import (
    NotAFileError,
    _check_python_version,
    _check_repository_exists,
    check_repository,
    copy_files,
    install_packages,
)
from turbopelican._utils.shared.args import (
    HandleDefaultsMode,
    InputMode,
    InstallType,
    Verbosity,
)


@pytest.fixture
def config(tmp_path: Path) -> AdornConfiguration:
    """Provides a valid configuration for the `adorn` subcommand."""
    return AdornConfiguration(
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


@pytest.fixture
def repository(config: AdornConfiguration) -> None:
    """Provides a repository already prepared."""
    (config.directory / "pyproject.toml").write_text(
        """
        [project]
        requires-python = ">= 3.11"
        """.strip()
    )
    (config.directory / ".python-version").write_text("3.11")


@pytest.fixture
def mock_shutil_which_uv() -> Generator[None, None, None]:
    """Mocks out `shutil.which` to return a path."""
    with mock.patch.object(shutil, "which", mock.Mock(return_value="/usr/bin/uv")):
        yield


@pytest.fixture
def mock_subprocess_check_call() -> Generator[mock.Mock, None, None]:
    """Mocks out `subprocess.check_call`."""
    with mock.patch.object(subprocess, "check_call") as mock_subprocess_check_call:
        yield mock_subprocess_check_call


def test_check_repository_exists(tmp_path: Path) -> None:
    """Checks no error is raised if the repository exists."""
    _check_repository_exists(tmp_path)


def test_check_repository_exists_not_found(tmp_path: Path) -> None:
    """Raises an error if the repository does not exist."""
    with pytest.raises(FileNotFoundError):
        _check_repository_exists(tmp_path / "fake")


def test_check_repository_exists_not_directory(tmp_path: Path) -> None:
    """Raises an error if the repository is not a directory."""
    (tmp_path / "fake").touch()
    with pytest.raises(NotADirectoryError):
        _check_repository_exists(tmp_path / "fake")


@pytest.mark.usefixtures("repository")
def test_check_python_version(config: AdornConfiguration) -> None:
    """Checks no error is raised if the Python version is set correctly."""
    _check_python_version(config)


@pytest.mark.usefixtures("repository")
def test_check_python_version_minimum_requires_problem(
    config: AdornConfiguration,
) -> None:
    """Checks error is raised if the `pyproject.toml` specifies a lower version."""
    with (config.directory / "pyproject.toml").open("rb") as read_pyproject:
        pyproject_toml = tomlkit.load(read_pyproject)

    pyproject_toml.get("project", {})["requires-python"] = ">= 3.8"

    with (config.directory / "pyproject.toml").open("w") as write_pyproject:
        tomlkit.dump(pyproject_toml, write_pyproject)

    with pytest.raises(RuntimeError):
        _check_python_version(config)


@pytest.mark.usefixtures("repository")
def test_check_python_version_python_version_does_not_exist(
    config: AdornConfiguration,
) -> None:
    """Checks error is raised if the `.python-version` file does not exist."""
    (config.directory / ".python-version").unlink()
    with pytest.raises(FileNotFoundError):
        _check_python_version(config)


@pytest.mark.usefixtures("repository")
def test_check_python_version_python_version_dir(
    config: AdornConfiguration,
) -> None:
    """Checks error is raised if `.python-version` points to a non-file."""
    python_version = config.directory / ".python-version"
    (python_version).unlink()
    python_version.mkdir()
    with pytest.raises(NotAFileError):
        _check_python_version(config)


@pytest.mark.usefixtures("repository")
def test_check_python_version_python_version_wrong(
    config: AdornConfiguration,
) -> None:
    """Checks error is raised if `.python-version` file contains lower version."""
    (config.directory / ".python-version").write_text("3.8")
    with pytest.raises(RuntimeError):
        _check_python_version(config)


@pytest.mark.usefixtures("repository")
def test_check_repository(config: AdornConfiguration) -> None:
    """Checks no error is raised if repository is configured correctly."""
    check_repository(config)


@pytest.mark.usefixtures("repository")
def test_check_repository_no_pyproject(config: AdornConfiguration) -> None:
    """Checks error is raised if `pyproject.toml` is missing."""
    (config.directory / "pyproject.toml").unlink()
    with pytest.raises(FileNotFoundError):
        check_repository(config)


@pytest.mark.usefixtures("repository")
def test_check_repository_pyproject_dir(config: AdornConfiguration) -> None:
    """Checks error is raised if `pyproject.toml` is not a file."""
    pyproject = config.directory / "pyproject.toml"
    pyproject.unlink()
    pyproject.mkdir()
    with pytest.raises(NotAFileError):
        check_repository(config)


@pytest.mark.usefixtures("repository")
@pytest.mark.parametrize(
    "filename", ["turbopelican.toml", "pelicanconf.py", "content", "output", "themes"]
)
def test_check_repository_turbopelican_unexpected_file(
    config: AdornConfiguration, filename: str
) -> None:
    """Checks error is raised if an unexpected file is found."""
    (config.directory / filename).touch()
    with pytest.raises(FileExistsError):
        check_repository(config)


@pytest.mark.usefixtures("repository")
def test_check_repository_turbopelican_unexpected_workflow(
    config: AdornConfiguration,
) -> None:
    """Checks error is raised if workflows file is unexpectedly present."""
    workflows = config.directory / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "turbopelican.yml").touch()
    with pytest.raises(FileExistsError):
        check_repository(config)


@pytest.mark.usefixtures("repository")
def test_copy_files(config: AdornConfiguration) -> None:
    """Checks files from template can be copied across correctly."""
    copy_files(config)
    for directory in [
        config.directory / ".github" / "workflows" / "turbopelican.yml",
        config.directory / "turbopelican.toml",
        config.directory / "pelicanconf.py",
        config.directory / "content",
        config.directory / "themes",
    ]:
        assert directory.exists()


@pytest.mark.usefixtures("repository", "mock_shutil_which_uv")
def test_install_packages(
    config: AdornConfiguration, mock_subprocess_check_call: mock.Mock
) -> None:
    """Checks that `uv` is given correct instructions for installing packages."""
    install_packages(config)

    environ = os.environ.copy()
    environ.pop("VIRTUAL_ENV")

    mock_subprocess_check_call.assert_called_once_with(
        ["/usr/bin/uv", "add", "pelican[markdown]>=4.11.0", "turbopelican>=0.3.3"],
        cwd=config.directory,
        env=environ,
    )
