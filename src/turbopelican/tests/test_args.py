from argparse import Namespace

from turbopelican.args import get_raw_args, get_raw_args_without_subcommand
from turbopelican.commands.init import init


def test_get_raw_args_without_subcommand() -> None:
    """Check namespace contains expected values, even when missing subcommand."""
    args = get_raw_args_without_subcommand(
        inputs=["myproj", "-d", "--quiet"],
    )
    assert args == Namespace(
        directory="myproj",
        use_defaults=True,
        quiet=True,
        author=None,
        site_name=None,
        timezone=None,
        default_lang=None,
        site_url=None,
        no_input=False,
        func=init.command,
    )


def test_get_raw_args() -> None:
    """Check namespace contains expected values."""
    args = get_raw_args(inputs=["init", "myproj", "-d", "--quiet"])
    assert args == Namespace(
        directory="myproj",
        use_defaults=True,
        quiet=True,
        author=None,
        site_name=None,
        timezone=None,
        default_lang=None,
        site_url=None,
        no_input=False,
        func=init.command,
    )
