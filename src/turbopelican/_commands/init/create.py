"""Provides the utilities to generate the website.

Author: Elliot Simpson
"""

import importlib.resources as pkg_resources
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal, cast
from zoneinfo import ZoneInfo

import tomlkit
import tomlkit.items

from turbopelican._commands.init.config import (
    InitConfiguration,
    InstallType,
    Verbosity,
)


def uv_sync(directory: Path, *, verbosity: Verbosity) -> None:
    """Sets up the repository with uv.

    Args:
        directory: The path where the repository is to be initialized.
        verbosity: Whether or not to suppress output.
    """
    uv_path = shutil.which("uv")
    if not uv_path:
        return

    uv_sync_args = [uv_path, "sync"]
    if verbosity == Verbosity.QUIET:
        uv_sync_args.append("--quiet")

    # Ensure warnings concerning virtual environments are filtered out.
    process = subprocess.Popen(
        uv_sync_args,
        stdout=sys.stdout,
        stderr=subprocess.PIPE,
        cwd=directory,
        text=True,
        bufsize=1,
    )
    while process.stderr:
        stderr_line = process.stderr.readline()
        if not stderr_line:
            break
        if "does not match the project environment path" not in stderr_line:
            print(stderr_line, file=sys.stderr, end="")

    process.wait()
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, process.args)


def _copy_template(directory: Path, name: Literal["newsite", "minimal"]) -> None:
    """Copies all the files from a template over.

    Args:
        directory: The path where the repository is to be initialized.
        name: The name of the template to copy.
    """
    with pkg_resources.as_file(
        pkg_resources.files(__name__.split(".", 1)[0]).joinpath("_templates", name)
    ) as p:
        shutil.copytree(p, directory, dirs_exist_ok=True)


def generate_repository(args: InitConfiguration) -> None:
    """Generates the files in place for turbopelican to use.

    Args:
        args: The arguments to configure the website.
    """
    if not args.directory.parent.exists():
        raise FileNotFoundError(
            f"Cannot create repository. {args.directory.parent} does not exist.",
        )
    if args.directory.exists():
        args.directory.rmdir()
    _copy_template(args.directory, "newsite")
    if args.install_type == InstallType.MINIMAL_INSTALL:
        _copy_template(args.directory, "minimal")

    git_path = shutil.which("git")
    if git_path is None:
        raise OSError("git not installed")
    git_init_args = [git_path, "init"]
    if args.verbosity == Verbosity.QUIET:
        git_init_args.append("--quiet")
    subprocess.run(git_init_args, check=True, cwd=args.directory)

    git_use_main_branch = [git_path, "branch", "-m", "main"]
    subprocess.run(git_use_main_branch, check=True, cwd=args.directory)


def update_website(args: InitConfiguration) -> None:
    """Updates the Pelican website to use the provided information.

    Args:
        args: The arguments to configure the website.
    """
    turbopelican_conf = Path(args.directory) / "turbopelican.toml"

    with turbopelican_conf.open(encoding="utf8") as configuration:
        toml = tomlkit.load(configuration)

    pelican = cast("tomlkit.items.Table", toml["pelican"])
    publish = cast("tomlkit.items.Table", toml["publish"])

    pelican["author"] = args.author
    pelican["sitename"] = args.site_name
    pelican["timezone"] = args.timezone
    pelican["default_lang"] = args.default_lang
    publish["site_url"] = args.site_url

    with turbopelican_conf.open("w", encoding="utf8") as configuration:
        tomlkit.dump(toml, configuration)


def update_pyproject(directory: Path) -> None:
    """Updates pyproject.toml to use the provided information.

    Args:
        directory: The path to the directory to be modified.
    """
    pyproject_conf = Path(directory) / "pyproject.toml"

    with pyproject_conf.open(encoding="utf8") as configuration:
        toml = tomlkit.load(configuration)

    rawname = "".join(
        char for char in directory.name if char.isalpha() or char.isdigit()
    )
    project = cast("tomlkit.items.Table", toml["project"])
    project["name"] = rawname

    with pyproject_conf.open("w", encoding="utf8") as configuration:
        tomlkit.dump(toml, configuration)


def update_contents(args: InitConfiguration) -> None:
    """Updates the Markdown contents to be ready for publication.

    Args:
        args: The arguments to configure the website.
    """
    today = datetime.now(tz=ZoneInfo(args.timezone)).date()
    for file in (args.directory / "content").glob("*.md"):
        text = file.read_text()
        file.write_text(text.format(date=today))
