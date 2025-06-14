"""Initializes a dedicated repository to deploy a Pelican website to GitHub Pages."""

from __future__ import annotations

from typing import TYPE_CHECKING

from turbopelican._commands.init.config import InitConfiguration
from turbopelican._commands.init.create import (
    commit_changes,
    generate_repository,
    report_completion,
    run_gh_cli,
    update_pyproject,
    uv_sync,
)
from turbopelican._utils.shared.create import update_contents, update_website

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace


def add_options(parser: ArgumentParser) -> None:
    """Adds the options for the init subparser.

    Args:
        parser: The parser/subparser to be updated.
    """
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
    parser.add_argument(
        "--minimal-install",
        help="Do not install turbopelican in the virtual environment.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--no-commit",
        help="Do not commit initial code.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--use-gh-cli",
        help="Create the remote GitHub repository and deploy website automatically.",
        action="store_true",
        default=False,
    )
    parser.set_defaults(func=command)


def command(raw_args: Namespace) -> None:
    """Uses the provided configuration to initialize a new repository.

    Args:
        raw_args: The command-line provided arguments.
    """
    config = InitConfiguration.from_args(raw_args)
    generate_repository(config)
    update_website(config)
    update_pyproject(config.directory)
    update_contents(config)
    uv_sync(directory=config.directory, verbosity=config.verbosity)
    commit_changes(config)
    run_gh_cli(config)
    report_completion(config)
