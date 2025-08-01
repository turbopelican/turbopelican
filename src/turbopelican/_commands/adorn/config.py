import shutil
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Self

from turbopelican._utils.shared.args import (
    CreateConfiguration,
    HandleDefaultsMode,
    InputMode,
    InstallType,
    Verbosity,
)


class AdornConfiguration(CreateConfiguration):
    """The command line arguments to configure the Turbopelican website/project."""

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
        )

    @classmethod
    def _default_site_url(cls, path: Path) -> str | None:
        """Obtains the default site URL if none is provided by the user explicitly.

        Args:
            path: The resolved path to the directory where the project is located.

        Returns:
            The default site URL if it can be obtained.
        """
        git_path = shutil.which("git")
        if not git_path:
            raise RuntimeError("git not installed")

        remote = subprocess.run(
            [git_path, "config", "--get", "remote.origin.url"],
            cwd=path,
            capture_output=True,
            check=False,
        ).stdout

        if not remote:
            return None

        decoded_remote = remote.decode().strip().removesuffix(".git")
        if decoded_remote.startswith("https://"):
            _, owner, repo = decoded_remote.rsplit("/", 2)
        else:
            owner, repo = decoded_remote.rsplit(":", 1)[1].split("/")

        return f"https://{owner}.github.io/{repo}"
