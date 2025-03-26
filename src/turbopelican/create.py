"""Provides the utilities to generate the website.

Author: Elliot Simpson
"""

import shutil
from pathlib import Path
from typing import cast

import tomlkit

from turbopelican.args import TurboConfiguration


def generate(directory: Path) -> None:
    """Generates the files in place for turbopelican to use.

    Args:
        directory: The path where the repository is to be initialized.
    """
    if not directory.parent.exists():
        raise ValueError(
            f"Cannot create repository. {directory.parent} does not exist.",
        )
    if directory.exists():
        directory.rmdir()
    to_copy = Path(__file__).parent / "newsite"
    shutil.copytree(to_copy, directory)


def update_website(args: TurboConfiguration) -> None:
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
