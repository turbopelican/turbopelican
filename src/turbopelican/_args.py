"""Parses the CLI arguments to turbopelican.

Author: Elliot Simpson.
"""

import argparse
import io
from contextlib import redirect_stderr

from turbopelican._commands.init import init


def get_raw_args_without_subcommand(
    *,
    inputs: list[str] | None = None,
) -> argparse.Namespace | None:
    """If no subcommand was passed to the parser, operates without it.

    Args:
        inputs: The list of inputs to the parser. Defaults to None, in which
            case it uses the command-line arguments.

    Returns:
        If valid without a subcommand, the corresponding namespace. Otherwise,
        None.
    """
    parser = argparse.ArgumentParser(
        prog="turbopelican",
        description="Generates a GitHub Page website with Pelican.",
    )
    init.add_options(parser)

    try:
        f = io.StringIO()
        with redirect_stderr(f):
            args = parser.parse_args(inputs)
    except SystemExit:
        return None
    else:
        warning_prefix = "\033[93m\033[1mDEPRECATION WARNING:\033[0m"
        message_contents = (
            "use `turbopelican init` instead of `turbopelican` without subcommand."
        )
        print(f"{warning_prefix} \033[93m{message_contents}\033[0m")

    args.func = init.command
    return args


def get_raw_args(*, inputs: list[str] | None = None) -> argparse.Namespace:
    """Defines the turbopelican API and returns the provided CLI arguments.

    Args:
        inputs: The list of inputs to the parser. Defaults to None, in which
            case it uses the command-line arguments.

    Returns:
        The argparse namespace for the project.
    """
    parser = argparse.ArgumentParser(
        prog="turbopelican",
        description="Make websites for GitHub Pages uber-fast.",
    )
    subparsers = parser.add_subparsers(required=True)
    subparsers.metavar = "subcommand"

    init_parser = subparsers.add_parser(
        "init",
        help="Generates a GitHub Page website with Pelican.",
        description="Creates a new turbopelican repository at the specified location.",
    )
    init.add_options(init_parser)

    f = io.StringIO()
    try:
        with redirect_stderr(f):
            return parser.parse_args(inputs)
    except SystemExit as exc:
        if not exc.code:
            raise
        raw_args = get_raw_args_without_subcommand(inputs=inputs)

        # Raises the original error if needed.
        if raw_args is None:
            print(f.getvalue(), end="")
            raise

        return raw_args
