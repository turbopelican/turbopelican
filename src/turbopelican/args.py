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
    no_input: bool
    use_defaults: bool


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
    parser.add_argument(
        "--no-input",
        "-n",
        help="Raises an error if user input required to operate.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--use-defaults",
        "-d",
        help="Uses default arguments where not provided in CLI.",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def _get_author(
    cli_author: str | None,
    git_path: str,
    *,
    no_input: str,
    use_defaults: bool,
) -> str:
    """Obtains the author of the website/package.

    The priority order is: provided by CLI; provided by user input; and if
    possible, the git user.

    Args:
        cli_author: The author provided by the CLI if applicable.
        git_path: The string path to the git instance.
        no_input: Whether or not to raise an error if user input required.
        use_defaults: Use the defaults if no flag has been passed.

    Returns:
        The name of the author.
    """
    if cli_author:
        return cli_author

    if no_input and not use_defaults:
        raise ValueError("Could not obtain author without user input.")

    get_default_author = subprocess.run(
        [git_path, "config", "--get", "user.name"],
        capture_output=True,
        text=True,
        check=False,
    )

    if get_default_author.returncode:
        if no_input:
            raise ValueError("Could not obtain author without user input.")
        author = ""
        while not author:
            author = input("Who is the website author? ")
        return author

    default_author = get_default_author.stdout.strip()
    if use_defaults:
        return default_author
    if no_input:
        raise ValueError("Could not obtain author without user input.")
    return input(f"Who is the website author? [{default_author}] ") or default_author


def _get_site_name(
    cli_site_name: str | None,
    path: Path,
    *,
    no_input: str,
    use_defaults: bool,
) -> str:
    """Returns the name of the website.

    Args:
        cli_site_name: The site-name provided by the CLI if applicable.
        path: The resolved path to the directory where the project is located.
        no_input: Whether or not to raise an error if user input required.
        use_defaults: Use the defaults if no flag has been passed.

    Returns:
        The name of the website.
    """
    if cli_site_name:
        return cli_site_name

    if use_defaults:
        return path.name

    if no_input:
        raise ValueError("Could not obtain site name without user input.")

    return input(f"What is the name of the website? [{path.name}] ") or path.name


def _get_timezone(
    cli_timezone: str | None,
    *,
    no_input: str,
    use_defaults: bool,
) -> str:
    """Returns the timezone for the website.

    Args:
        cli_timezone: The timezone provided by the CLI if applicable.
        no_input: Whether or not to raise an error if user input required.
        use_defaults: Use the defaults if no flag has been passed.

    Returns:
        The timezone of the website.
    """
    if cli_timezone:
        return cli_timezone

    if no_input and not use_defaults:
        raise ValueError("Could not obtain timezone without user input.")

    default_local_zone = get_localzone()
    if not isinstance(default_local_zone, ZoneInfo):
        if no_input:
            raise ValueError("Could not obtain local zone without user input.")
        chosen_local_zone = input("What timezone will your website use? ")
        if not chosen_local_zone:
            raise ValueError("No timezone provided.")
    elif use_defaults:
        return default_local_zone.key
    elif no_input:
        raise ValueError("Could not obtain local zone without user input.")
    else:
        chosen_local_zone = (
            input(f"What timezone will your website use? [{default_local_zone.key}] ")
            or default_local_zone.key
        )

    if chosen_local_zone not in available_timezones():
        raise ValueError(f"Invalid timezone provided: {chosen_local_zone}")

    return chosen_local_zone


def _get_default_lang(
    cli_default_lang: str | None,
    *,
    no_input: str,
    use_defaults: bool,
) -> str:
    """Returns the default language for the website.

    Args:
        cli_default_lang: The default language provided by the CLI if applicable.
        no_input: Whether or not to raise an error if user input required.
        use_defaults: Use the defaults if no flag has been passed.

    Returns:
        The default language of the website.
    """
    if cli_default_lang:
        return cli_default_lang

    if use_defaults:
        return "en"
    if no_input:
        raise ValueError("Could not obtain default language without user input.")

    chosen_lang = input("What language will your website use? [en] ")
    if not chosen_lang:
        return "en"

    if not langcodes.Language.get(chosen_lang).is_valid():
        raise ValueError(f"Invalid language: {chosen_lang}")

    return chosen_lang


def _validate_site_url(site_url: str) -> None:
    """Checks the provided site URL.

    Args:
        site_url: The site URL that the user has proposed.
    """
    if not (site_url.startswith("https://") and site_url.endswith(".github.io")):
        raise ValueError(f"Invalid website URL: {site_url}")

    assess_name = site_url.removesuffix(".github.io").removeprefix("https://")
    if not assess_name:
        raise ValueError(f"Invalid website URL: {site_url}")

    for char in assess_name:
        if not (char.isalpha() or char.isdigit() or char == "-"):
            raise ValueError(f"Invalid website URL: {site_url}")


def _get_site_url(
    cli_site_url: str | None,
    path: Path,
    *,
    no_input: str,
    use_defaults: bool,
) -> str:
    """Returns the website URL.

    Args:
        cli_site_url: The site URL provided by the CLI if applicable.
        path: The resolved path to the directory where the project is located.
        no_input: Whether or not to raise an error if user input required.
        use_defaults: Use the defaults if no flag has been passed.

    Returns:
        The website URL.
    """
    if cli_site_url:
        return cli_site_url

    if no_input and not use_defaults:
        raise ValueError("Could not obtain site URL without user input.")

    website_name = path.name.removesuffix(".github.io").replace("_", "-")
    filtered_name = "".join(
        char for char in website_name if char.isalpha() or char.isdigit() or char == "-"
    )
    if filtered_name:
        default_url = f"https://{filtered_name}.github.io"
        if use_defaults:
            return default_url
        chosen_name = input(f"What is your website URL? [{default_url}] ")
        if not chosen_name:
            return default_url
    elif no_input:
        raise ValueError("Could not obtain site URL without user input.")
    else:
        chosen_name = input("What is your website URL? ").removesuffix(".github.io")
        if not chosen_name:
            raise ValueError("Website URL not provided.")

    _validate_site_url(chosen_name)
    return chosen_name


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
    author = _get_author(
        raw_args.author,
        git_path,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )
    site_name = _get_site_name(
        raw_args.site_name,
        path,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )
    timezone = _get_timezone(
        raw_args.timezone,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )
    default_lang = _get_default_lang(
        raw_args.default_lang,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )
    site_url = _get_site_url(
        raw_args.site_url,
        path,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )

    return TurboConfiguration(
        directory=path,
        author=author,
        site_name=site_name,
        timezone=timezone,
        default_lang=default_lang,
        site_url=site_url,
        quiet=raw_args.quiet,
        no_input=raw_args.no_input,
        use_defaults=raw_args.use_defaults,
    )
