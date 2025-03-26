"""Entry point for turbopelican.

Author: Elliot Simpson.
"""

import sys
from collections.abc import Callable
from typing import TypeVar

from turbopelican.args import get_args
from turbopelican.create import generate_repository, update_pyproject, update_website

T = TypeVar("T")


def suppress(function: Callable[[], T]) -> Callable[[], T]:
    """Suppress traceback messages from any messages in a function.

    Args:
        function: The function for which the tracebacks are to be suppressed.
    """

    def suppressed_function() -> T:
        try:
            return function()
        except Exception as exc:
            print(f"\033[0;31m{exc}\033[0m")
            sys.exit(1)

    return suppressed_function


@suppress
def main() -> None:
    """Parses the command-line arguments and runs."""
    args = get_args()
    generate_repository(args.directory)
    update_website(args)
    update_pyproject(args.directory)


if __name__ == "__main__":
    main()
