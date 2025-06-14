"""Updates an existing repository to deploy a Pelican website to GitHub Pages."""

from __future__ import annotations

from typing import TYPE_CHECKING

from turbopelican._commands.adorn.config import AdornConfiguration
from turbopelican._commands.adorn.create import (
    check_repository,
    copy_files,
    install_packages,
    report_completion,
)
from turbopelican._utils.shared.create import update_contents, update_website

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace


def add_options(parser: ArgumentParser) -> None:
    """Adds the options for the adorn subparser.

    Args:
        parser: The parser/subparser to be updated.
    """
    parser.add_argument(
        "directory",
        help="Path to the repository to be modified.",
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
    parser.set_defaults(func=command)


def command(raw_args: Namespace) -> None:
    """Uses the provided configuration to modify an existing repository.

    Args:
        raw_args: The command-line provided arguments.
    """
    config = AdornConfiguration.from_args(raw_args)
    check_repository(config)
    copy_files(config)
    update_website(config)
    update_contents(config)
    install_packages(config)
    report_completion(config)
