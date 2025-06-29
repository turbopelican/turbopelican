"""Stores configuration specific to creating fresh Pelican websites."""

import shutil
from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from turbopelican._utils.shared.args import (
    ConfigurationError,
    CreateConfiguration,
    HandleDefaultsMode,
    InputMode,
    InstallType,
    Verbosity,
)


@dataclass
class InitConfiguration(CreateConfiguration):
    """The command line arguments to configure the turbopelican website/project."""

    commit_changes: bool = True
    use_gh_cli: bool = False

    @classmethod
    def from_args(cls, raw_args: Namespace) -> Self:
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
        commit_changes = cls._get_commit_changes(
            no_commit=raw_args.no_commit, use_gh_cli=raw_args.use_gh_cli
        )

        return cls(
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
            commit_changes=commit_changes,
            use_gh_cli=raw_args.use_gh_cli,
        )

    @classmethod
    def _default_site_url(cls, path: Path) -> str | None:
        """Obtains the default site URL if none is provided by the user explicitly.

        Args:
            path: The resolved path to the directory where the project is located.

        Returns:
            The default site URL if it can be obtained.
        """
        website_name = path.name.removesuffix(".github.io").replace("_", "-")
        filtered_name = "".join(
            char
            for char in website_name
            if char.isalpha() or char.isdigit() or char == "-"
        )
        if filtered_name:
            return f"https://{filtered_name}.github.io"

        return None

    @classmethod
    def _get_commit_changes(cls, *, no_commit: bool, use_gh_cli: bool) -> bool:
        """Ensures that non-conflicting instructions are provided for git actions.

        Args:
            no_commit: If True, does not make any commits.
            use_gh_cli: If True, creates the remote repository on GitHub automatically.

        Returns:
            Whether or not to commit the changes.
        """
        if use_gh_cli and no_commit:
            msg = "Cannot run GitHub CLI without committing changes."
            raise ConfigurationError(msg)

        return not no_commit
