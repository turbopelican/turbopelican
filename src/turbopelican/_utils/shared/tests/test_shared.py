from pathlib import Path

import pytest

from turbopelican._utils.errors import TurbopelicanError
from turbopelican._utils.shared import find_config
from turbopelican._utils.shared.shared import _find_config_file, _get_project_root


def test_get_project_root_succeed(tmp_path: Path) -> None:
    """Checks that the root of a project can be found.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    child_path = tmp_path / "first" / "second"
    child_path.mkdir(parents=True)
    (tmp_path / "pyproject.toml").touch()
    assert _get_project_root(child_path) == tmp_path


def test_get_project_root_fail(tmp_path: Path) -> None:
    """Checks that when the root of a project cannot be found, an error is raised.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    child_path = tmp_path / "first" / "second"
    child_path.mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        _get_project_root(child_path)


def test_find_config_file_turbopelican_config(tmp_path: Path) -> None:
    """Checks that the `turbopelican.toml` file can be found.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    child_path = tmp_path / "first" / "second"
    child_path.mkdir(parents=True)
    (tmp_path / "pyproject.toml").touch()
    turbopelican_config = tmp_path / "turbopelican.toml"
    turbopelican_config.touch()
    assert _find_config_file(child_path) == turbopelican_config


def test_find_config_file_pyproject_config(tmp_path: Path) -> None:
    """Checks that the `pyproject.toml` file can be found.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    child_path = tmp_path / "first" / "second"
    child_path.mkdir(parents=True)
    pyproject_config = tmp_path / "pyproject.toml"
    pyproject_config.touch()
    assert _find_config_file(child_path) == pyproject_config


def test_find_config_file_pyproject_fail(tmp_path: Path) -> None:
    """Checks that the file containing Turbopelican configuration can be found.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    child_path = tmp_path / "first" / "second"
    child_path.mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        _find_config_file(child_path)


def test_find_config_turbopelican(tmp_path: Path) -> None:
    """Checks that the configuration can be extracted from `turbopelican.toml`.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    (tmp_path / "pyproject.toml").touch()
    turbopelican_toml = tmp_path / "turbopelican.toml"
    turbopelican_toml.write_text("hello = 1")
    assert find_config(tmp_path) == {"hello": 1}


def test_find_config_pyproject(tmp_path: Path) -> None:
    """Checks that the configuration can be extracted from `pyproject.toml`.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    (tmp_path / "pyproject.toml").write_text(
        """
        [tool.turbopelican]
        hello = 1
        """
    )
    assert find_config(tmp_path) == {"hello": 1}


def test_find_config_non_project(tmp_path: Path) -> None:
    """Checks an error is raised when no project configuration is found.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    with pytest.raises(FileNotFoundError):
        assert find_config(tmp_path)


def test_find_config_invalid(tmp_path: Path) -> None:
    """Checks an error is raised when configuration is not parsed as a dictionary.

    Args:
        tmp_path: A temporary directory in which to store the project.
    """
    (tmp_path / "pyproject.toml").write_text(
        """
        [tool]
        turbopelican = 1
        """
    )
    with pytest.raises(TurbopelicanError):
        find_config(tmp_path)
