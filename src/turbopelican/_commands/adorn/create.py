"""Provides the utilities to generate the website.

Author: Elliot Simpson
"""

import importlib.resources as pkg_resources
import os
import shutil
import subprocess
import tomllib
from pathlib import Path

from turbopelican._commands.adorn.config import AdornConfiguration
from turbopelican._utils.shared.args import InstallType, Verbosity


class NotAFileError(OSError):
    """Operation only works on files."""


def _check_repository_exists(directory: Path) -> None:
    """Raises an error if the repository does not exist.

    Args:
        directory: The path to the repository.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Repository at {directory} does not exist.")
    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a directory.")


def _check_python_version(config: AdornConfiguration) -> None:
    """Checks that the Python version of the repository is high enough.

    Args:
        config: The arguments to configure the website.
    """
    pyproject = config.directory / "pyproject.toml"
    with pyproject.open("rb") as read_pyproject:
        pyproject_toml = tomllib.load(read_pyproject)

    version = pyproject_toml.get("project", {}).get("requires-python")
    if (
        not version
        or not version.startswith(">=")
        or tuple(map(int, version.removeprefix(">=").split("."))) < (3, 11)
    ):
        raise RuntimeError("Repository must use Python version 3.11 or later.")

    python_version = config.directory / ".python-version"

    if not python_version.exists():
        raise FileNotFoundError(
            f"{python_version} not found. File is required to adorn."
        )

    if not python_version.is_file():
        raise NotAFileError(f"{python_version} is not a file.")

    if tuple(map(int, python_version.read_text().split("."))) < (3, 11):
        raise RuntimeError("Repository must use Python version 3.11 or later.")


def check_repository(config: AdornConfiguration) -> None:
    """Checks that a repository is fit to host a new website.

    Args:
        config: The arguments to configure the website.
    """
    _check_repository_exists(config.directory)

    pyproject = config.directory / "pyproject.toml"
    if not pyproject.exists():
        raise FileNotFoundError(f"{pyproject} not found. File is required to adorn.")
    if not pyproject.is_file():
        raise NotAFileError(f"{pyproject} is not a file.")

    _check_python_version(config)

    turbopelican = config.directory / "turbopelican.toml"
    if turbopelican.exists():
        raise FileExistsError(f"{turbopelican} should not exist.")

    pelicanconf = config.directory / "pelicanconf.py"
    if pelicanconf.exists():
        raise FileExistsError(f"{pelicanconf} should not exist.")

    workflow = config.directory / ".github" / "workflows" / "turbopelican.yml"
    if workflow.exists():
        raise FileExistsError(f"{workflow} should not exist.")

    for subdirectory_name in ["content", "output", "themes"]:
        subdirectory = config.directory / subdirectory_name
        if subdirectory.exists():
            raise FileExistsError(f"{subdirectory} should not exist.")


def copy_files(config: AdornConfiguration) -> None:
    """Copy files into repository.

    Args:
        config: The arguments to configure the website.
    """
    (config.directory / ".github" / "workflows").mkdir(parents=True, exist_ok=True)

    src_root = pkg_resources.files(__name__.split(".", 1)[0])

    with pkg_resources.as_file(src_root.joinpath("_templates", "newsite")) as p:
        shutil.copy(p / "turbopelican.toml", config.directory)
        if config.install_type == InstallType.FULL_INSTALL:
            shutil.copy(p / "pelicanconf.py", config.directory)
        shutil.copy(
            p / ".github" / "workflows" / "turbopelican.yml",
            config.directory / ".github" / "workflows",
        )
        shutil.copytree(
            p / "content", config.directory / "content", dirs_exist_ok=False
        )
        shutil.copytree(p / "themes", config.directory / "themes", dirs_exist_ok=False)

    if config.install_type == InstallType.MINIMAL_INSTALL:
        with pkg_resources.as_file(src_root.joinpath("_templates", "minimal")) as p:
            shutil.copy(p / "pelicanconf.py", config.directory)


def install_packages(config: AdornConfiguration) -> None:
    """Installs necessary packages into repository.

    Args:
        config: The arguments to configure the website.
    """
    uv_path = shutil.which("uv")
    if not uv_path:
        raise RuntimeError("uv not installed")

    uv_add_args = [uv_path, "add", "pelican[markdown]>=4.11.0"]
    if config.install_type == InstallType.FULL_INSTALL:
        uv_add_args.append("turbopelican>=0.3.3")
    if config.verbosity == Verbosity.QUIET:
        uv_add_args.append("--quiet")

    environ = os.environ.copy()
    environ.pop("VIRTUAL_ENV")

    subprocess.check_call(uv_add_args, cwd=config.directory, env=environ)


def report_completion(args: AdornConfiguration) -> None:
    """Reports that Turbopelican has finished adorning the repository.

    Args:
        args: The arguments to configure the website.
    """
    if args.verbosity == Verbosity.NORMAL:
        print("⚡ Turbopelican adorned! ⚡")
