from argparse import Namespace

from turbopelican._args import get_raw_args, get_raw_args_without_subcommand
from turbopelican._commands.adorn import adorn
from turbopelican._commands.init import init


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
        minimal_install=False,
        no_commit=False,
        use_gh_cli=False,
    )


def test_get_raw_args_init() -> None:
    """Check namespace contains expected values for `init` subcommand."""
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
        minimal_install=False,
        no_commit=False,
        use_gh_cli=False,
    )


def test_get_raw_args_adorn() -> None:
    """Check namespace contains expected values for `adorn` subcommand."""
    args = get_raw_args(inputs=["adorn", "myproj", "--quiet"])
    assert args == Namespace(
        directory="myproj",
        author=None,
        site_name=None,
        timezone=None,
        default_lang=None,
        site_url=None,
        quiet=True,
        no_input=False,
        use_defaults=False,
        minimal_install=False,
        func=adorn.command,
    )
