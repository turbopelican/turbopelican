"""Parses the CLI arguments to turbopelican.

Author: Elliot Simpson.
"""

import argparse
import shutil
import subprocess
from pathlib import Path
from zoneinfo import ZoneInfo, available_timezones

import langcodes
from pydantic import BaseModel
from tzlocal import get_localzone


class TurboConfiguration(BaseModel):
    """The command line arguments to configure the turbopelican website/project."""

    directory: Path
    author: str
    site_name: str
    timezone: str
    default_lang: str
    site_url: str
    quiet: bool


def _get_raw_args() -> argparse.Namespace:
    """Defines the turbopelican API and returns the provided CLI arguments.

    Returns:
        The argparse namespace for the project.
    """
    parser = argparse.ArgumentParser(
        prog="turbopelican",
        description="Generates a GitHub Page website with Pelican.",
    )
    parser.add_argument(
        "directory",
        help="Path to the repository to be created.",
        default=".",
        nargs="?",
    )
    parser.add_argument(
        "--author",
        help="Name of the author of the website.",
        nargs="?",
    )
    parser.add_argument(
        "--site-name",
        help="The name of the website.",
        nargs="?",
    )
    parser.add_argument(
        "--timezone",
        help="Time zone by which to show dates on the website.",
        nargs="?",
    )
    parser.add_argument(
        "--default-lang",
        help="The language of the website e.g. en.",
        nargs="?",
    )
    parser.add_argument(
        "--site-url",
        help="The url of the website.",
        nargs="?",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        help="Suppresses all output.",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def _get_author(cli_author: str | None, git_path: str) -> str:
    """Obtains the author of the website/package.

    The priority order is: provided by CLI; provided by user input; and if
    possible, the git user.

    Args:
        cli_author: The author provided by the CLI if applicable.
        git_path: The string path to the git instance.

    Returns:
        The name of the author.
    """
    if cli_author:
        return cli_author

    get_default_author = subprocess.run(
        [git_path, "config", "--get", "user.name"],
        capture_output=True,
        text=True,
        check=False,
    )

    if get_default_author.returncode:
        author = ""
        while not author:
            author = input("Who is the website author? ")
        return author

    default_author = get_default_author.stdout.strip()
    return input(f"Who is the website author? [{default_author}] ") or default_author


def _get_site_name(cli_site_name: str | None, path: Path) -> str:
    """Returns the name of the website.

    Args:
        cli_site_name: The site-name provided by the CLI if applicable.
        path: The resolved path to the directory where the project is located.

    Returns:
        The name of the website.
    """
    if cli_site_name:
        return cli_site_name

    return input(f"What is the name of the website? [{path.name}] ") or path.name


def _get_timezone(cli_timezone: str | None) -> str:
    """Returns the timezone for the website.

    Args:
        cli_timezone: The timezone provided by the CLI if applicable.

    Returns:
        The timezone of the website.
    """
    if cli_timezone:
        return cli_timezone

    default_local_zone = get_localzone()
    if not isinstance(default_local_zone, ZoneInfo):
        chosen_local_zone = input("What timezone will your website use? ")
        if not chosen_local_zone:
            raise ValueError("No timezone provided.")
    else:
        chosen_local_zone = (
            input(f"What timezone will your website use? [{default_local_zone.key}] ")
            or default_local_zone.key
        )

    if chosen_local_zone not in available_timezones():
        raise ValueError(f"Invalid timezone provided: {chosen_local_zone}")

    return chosen_local_zone


def _get_default_lang(cli_default_lang: str | None) -> str:
    """Returns the default language for the website.

    Args:
        cli_default_lang: The default language provided by the CLI if applicable.

    Returns:
        The default language of the website.
    """
    if cli_default_lang:
        return cli_default_lang

    chosen_lang = input("What language will your website use? [en] ")
    if not chosen_lang:
        return "en"

    if not langcodes.Language.get(chosen_lang).is_valid():
        raise ValueError(f"Invalid language: {chosen_lang}")

    return chosen_lang


def _get_site_url(cli_site_url: str | None, path: Path) -> str:
    """Returns the website URL.

    Args:
        cli_site_url: The site URL provided by the CLI if applicable.
        path: The resolved path to the directory where the project is located.

    Returns:
        The website URL.
    """
    if cli_site_url:
        return cli_site_url

    website_name = path.name.removesuffix(".github.io").replace("_", "-")
    filtered_name = "".join(
        char for char in website_name if char.isalpha() or char.isdigit() or char == "-"
    )
    if filtered_name:
        default_url = f"https://{filtered_name}.github.io"
        chosen_name = input(f"What is your website URL? [{default_url}] ")
        if not chosen_name:
            return default_url
    else:
        chosen_name = input("What is your website URL? ").removesuffix(".github.io")
        if not chosen_name:
            raise ValueError("Website URL not provided.")

    if not (chosen_name.startswith("https://") and chosen_name.endswith(".github.io")):
        raise ValueError(f"Invalid website URL: {chosen_name}")

    assess_name = chosen_name.removesuffix(".github.io").removeprefix("https://")
    for char in assess_name:
        if not (char.isalpha() or char.isdigit() or char == "-"):
            raise ValueError(f"Invalid website URL: {chosen_name}")

    return f"https://{assess_name}.github.io"


def get_args() -> TurboConfiguration:
    """Returns the command-line arguments in a Pydantic object.

    Returns:
        The command-line arguments.
    """
    git_path = shutil.which("git")
    if git_path is None:
        raise OSError("git not installed")

    raw_args = _get_raw_args()
    path = Path(raw_args.directory).resolve()
    author = _get_author(raw_args.author, git_path)
    site_name = _get_site_name(raw_args.site_name, path)
    timezone = _get_timezone(raw_args.timezone)
    default_lang = _get_default_lang(raw_args.default_lang)
    site_url = _get_site_url(raw_args.site_url, path)

    return TurboConfiguration(
        directory=path,
        author=author,
        site_name=site_name,
        timezone=timezone,
        default_lang=default_lang,
        site_url=site_url,
        quiet=raw_args.quiet,
    )
