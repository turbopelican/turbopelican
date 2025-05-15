"""Stores configuration specific to creating fresh Pelican websites."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo, available_timezones

import langcodes
import langcodes.tag_parser
from tzlocal import get_localzone

if TYPE_CHECKING:
    from argparse import Namespace


class Verbosity(StrEnum):
    """How verbose `turbopelican init` should be."""

    NORMAL = "NORMAL"
    QUIET = "QUIET"


class InputMode(StrEnum):
    """Either allows or disallows standard input."""

    ACCEPT_INPUT = "ACCEPT_INPUT"
    REJECT_INPUT = "REJECT_INPUT"


class HandleDefaultsMode(StrEnum):
    """Can default inputs not provided by CLI."""

    REQUIRE_STANDARD_INPUT = "REQUIRE_STANDARD_INPUT"
    USE_DEFAULTS = "USE_DEFAULTS"


class InstallType(StrEnum):
    """Whether Turbopelican should be installed in the virtual environment or not."""

    MINIMAL_INSTALL = "MINIMAL_INSTALL"
    FULL_INSTALL = "FULL_INSTALL"


class ConfigurationError(ValueError):
    """The configuration cannot be correctly evaluated, due to missing inputs."""


@dataclass
class InitConfiguration:
    """The command line arguments to configure the turbopelican website/project."""

    directory: Path
    author: str
    site_name: str
    timezone: str
    default_lang: str
    site_url: str
    verbosity: Verbosity
    input_mode: InputMode
    handle_defaults_mode: HandleDefaultsMode
    install_type: InstallType

    @classmethod
    def from_args(cls, raw_args: Namespace) -> InitConfiguration:
        """Returns the command-line arguments in a Pydantic object.

        Returns:
            The command-line arguments.
        """
        git_path = shutil.which("git")
        if git_path is None:
            raise OSError("git not installed")

        path = Path(raw_args.directory).resolve()

        verbosity = Verbosity.QUIET if raw_args.quiet else Verbosity.NORMAL
        input_mode = (
            InputMode.REJECT_INPUT if raw_args.no_input else InputMode.ACCEPT_INPUT
        )
        handle_defaults_mode = (
            HandleDefaultsMode.USE_DEFAULTS
            if raw_args.use_defaults
            else HandleDefaultsMode.REQUIRE_STANDARD_INPUT
        )
        install_type = (
            InstallType.MINIMAL_INSTALL
            if raw_args.minimal_install
            else InstallType.FULL_INSTALL
        )

        author = cls._get_author(
            raw_args.author,
            git_path,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
        )
        site_name = cls._get_site_name(
            raw_args.site_name,
            path,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
        )
        timezone = cls._get_timezone(
            raw_args.timezone,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
        )
        default_lang = cls._get_default_lang(
            raw_args.default_lang,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
        )
        site_url = cls._get_site_url(
            raw_args.site_url,
            path,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
        )

        return InitConfiguration(
            directory=path,
            author=author,
            site_name=site_name,
            timezone=timezone,
            default_lang=default_lang,
            site_url=site_url,
            verbosity=verbosity,
            input_mode=input_mode,
            handle_defaults_mode=handle_defaults_mode,
            install_type=install_type,
        )

    @staticmethod
    def _get_author(
        cli_author: str | None,
        git_path: str,
        *,
        input_mode: InputMode,
        handle_defaults_mode: HandleDefaultsMode,
    ) -> str:
        """Obtains the author of the website/package.

        The priority order is: provided by CLI; provided by user input; and if
        possible, the git user.

        Args:
            cli_author: The author provided by the CLI if applicable.
            git_path: The string path to the git instance.
            input_mode: Whether or not to raise an error if user input required.
            handle_defaults_mode: Use the defaults if no flag has been passed.

        Returns:
            The name of the author.
        """
        if cli_author:
            return cli_author

        if (
            input_mode == InputMode.REJECT_INPUT
            and handle_defaults_mode == HandleDefaultsMode.REQUIRE_STANDARD_INPUT
        ):
            message = "Could not obtain author without user input."
            raise ConfigurationError(message)

        get_default_author = subprocess.run(
            [git_path, "config", "--get", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )

        if get_default_author.returncode:
            if input_mode == InputMode.REJECT_INPUT:
                raise ConfigurationError("Could not obtain author without user input.")
            author = ""
            while not author:
                author = input("Who is the website author? ")
            return author

        default_author = get_default_author.stdout.strip()
        if handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS:
            return default_author
        return (
            input(f"Who is the website author? [{default_author}] ") or default_author
        )

    @staticmethod
    def _get_site_name(
        cli_site_name: str | None,
        path: Path,
        *,
        input_mode: InputMode,
        handle_defaults_mode: HandleDefaultsMode,
    ) -> str:
        """Returns the name of the website.

        Args:
            cli_site_name: The site-name provided by the CLI if applicable.
            path: The resolved path to the directory where the project is located.
            input_mode: Whether or not to raise an error if user input required.
            handle_defaults_mode: Use the defaults if no flag has been passed.

        Returns:
            The name of the website.
        """
        if cli_site_name:
            return cli_site_name

        if handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS:
            return path.name

        if input_mode == InputMode.REJECT_INPUT:
            raise ConfigurationError("Could not obtain site name without user input.")

        return input(f"What is the name of the website? [{path.name}] ") or path.name

    @staticmethod
    def _get_timezone(
        cli_timezone: str | None,
        *,
        input_mode: InputMode,
        handle_defaults_mode: HandleDefaultsMode,
    ) -> str:
        """Returns the timezone for the website.

        Args:
            cli_timezone: The timezone provided by the CLI if applicable.
            input_mode: Whether or not to raise an error if user input required.
            handle_defaults_mode: Use the defaults if no flag has been passed.

        Returns:
            The timezone of the website.
        """
        if cli_timezone:
            return cli_timezone

        if (
            input_mode == InputMode.REJECT_INPUT
            and handle_defaults_mode == HandleDefaultsMode.REQUIRE_STANDARD_INPUT
        ):
            raise ConfigurationError("Could not obtain timezone without user input.")

        default_local_zone = get_localzone()
        if not isinstance(default_local_zone, ZoneInfo):
            if input_mode == InputMode.REJECT_INPUT:
                message = "Could not obtain local zone without user input."
                raise ConfigurationError(message)
            chosen_local_zone = input("What timezone will your website use? ")
            if not chosen_local_zone:
                raise ConfigurationError("No timezone provided.")
        elif handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS:
            return default_local_zone.key
        else:
            prompt = f"What timezone will your website use? [{default_local_zone.key}] "
            chosen_local_zone = input(prompt) or default_local_zone.key

        if chosen_local_zone not in available_timezones():
            raise ConfigurationError(f"Invalid timezone provided: {chosen_local_zone}")

        return chosen_local_zone

    @staticmethod
    def _get_default_lang(
        cli_default_lang: str | None,
        *,
        input_mode: InputMode,
        handle_defaults_mode: HandleDefaultsMode,
    ) -> str:
        """Returns the default language for the website.

        Args:
            cli_default_lang: The default language provided by the CLI if applicable.
            input_mode: Whether or not to raise an error if user input required.
            handle_defaults_mode: Use the defaults if no flag has been passed.

        Returns:
            The default language of the website.
        """
        if cli_default_lang:
            return cli_default_lang

        if handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS:
            return "en"
        if input_mode == InputMode.REJECT_INPUT:
            message = "Could not obtain default language without user input."
            raise ConfigurationError(message)

        chosen_lang = input("What language will your website use? [en] ")
        if not chosen_lang:
            return "en"

        # Raise exception if the language doesn't appear to be valid.
        try:
            language = langcodes.Language.get(chosen_lang)
        except langcodes.tag_parser.LanguageTagError:
            raise ConfigurationError(f"Invalid language: {chosen_lang}") from None
        if not language.is_valid():
            raise ConfigurationError(f"Invalid language: {chosen_lang}")

        return chosen_lang

    @staticmethod
    def _validate_site_url(site_url: str) -> None:
        """Checks the provided site URL.

        Args:
            site_url: The site URL that the user has proposed.
        """
        if not (site_url.startswith("https://") and site_url.endswith(".github.io")):
            raise ConfigurationError(f"Invalid website URL: {site_url}")

        assess_name = site_url.removesuffix(".github.io").removeprefix("https://")
        if not assess_name:
            raise ConfigurationError(f"Invalid website URL: {site_url}")

        for char in assess_name:
            if not (char.isalpha() or char.isdigit() or char == "-"):
                raise ConfigurationError(f"Invalid website URL: {site_url}")

    @classmethod
    def _get_site_url(
        cls,
        cli_site_url: str | None,
        path: Path,
        *,
        input_mode: InputMode,
        handle_defaults_mode: HandleDefaultsMode,
    ) -> str:
        """Returns the website URL.

        Args:
            cli_site_url: The site URL provided by the CLI if applicable.
            path: The resolved path to the directory where the project is located.
            input_mode: Whether or not to raise an error if user input required.
            handle_defaults_mode: Use the defaults if no flag has been passed.

        Returns:
            The website URL.
        """
        if cli_site_url:
            return cli_site_url

        if (
            input_mode == InputMode.REJECT_INPUT
            and handle_defaults_mode == HandleDefaultsMode.REQUIRE_STANDARD_INPUT
        ):
            raise ConfigurationError("Could not obtain site URL without user input.")

        website_name = path.name.removesuffix(".github.io").replace("_", "-")
        filtered_name = "".join(
            char
            for char in website_name
            if char.isalpha() or char.isdigit() or char == "-"
        )
        if filtered_name:
            default_url = f"https://{filtered_name}.github.io"
            if handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS:
                return default_url
            chosen_name = input(f"What is your website URL? [{default_url}] ")
            if not chosen_name:
                return default_url
        elif input_mode == InputMode.REJECT_INPUT:
            raise ConfigurationError("Could not obtain site URL without user input.")
        else:
            chosen_name = input("What is your website URL? ")
            if not chosen_name:
                raise ConfigurationError("Website URL not provided.")

        cls._validate_site_url(chosen_name)
        return chosen_name
