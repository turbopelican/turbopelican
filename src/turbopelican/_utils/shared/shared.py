import tomllib
from pathlib import Path

from turbopelican._utils.errors.errors import TurbopelicanError

__all__ = [
    "Toml",
    "find_config",
]

Toml = str | int | float | list["Toml"] | dict[str, "Toml"]


def _get_project_root(start_path: Path | str = ".") -> Path:
    """Iterates through ancestors until the project root is obtained.

    Args:
        start_path: The path at which to start searching for `pyproject.toml`.

    Returns:
        The project root.
    """
    child = Path(start_path).resolve() / "starthere"
    parent = child.parent
    found = None
    while child != parent:
        search = parent / "pyproject.toml"
        if search.exists():
            found = parent
        child = parent
        parent = child.parent

    if found is None:
        raise FileNotFoundError("Could not find project root.")

    return found


def _find_config_file(start_path: Path | str = ".") -> Path:
    """Searches for the file which contains the configuration for turbopelican.

    Args:
        start_path: The path at which to start searching for `pyproject.toml`.

    Returns:
        The path to the file which contains the configuration for turbopelican.
    """
    project_root = _get_project_root(start_path)
    turbopelican_toml = project_root / "turbopelican.toml"
    if turbopelican_toml.exists():
        return turbopelican_toml
    return project_root / "pyproject.toml"


def find_config(start_path: Path | str = ".") -> dict[str, Toml]:
    """Obtains the configuration for turbopelican.

    Args:
        start_path: The path at which to start searching for `pyproject.toml`.

    Returns:
        The configuration contained in the configuration file.
    """
    config_file = _find_config_file(start_path)
    with config_file.open("rb") as config:
        contents = tomllib.load(config)
    if config_file.name == "turbopelican.toml":
        return_dict = contents
    else:
        return_dict = contents["tool"]["turbopelican"]
    if not isinstance(return_dict, dict):
        raise TurbopelicanError("turbopelican has not been configured.")
    return return_dict
