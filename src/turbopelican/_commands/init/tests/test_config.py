from argparse import Namespace
from pathlib import Path

from turbopelican._commands.init.config import InitConfiguration
from turbopelican._utils.shared.args import HandleDefaultsMode, InputMode, Verbosity


def test_turbo_configuration_from_args(tmp_path: Path) -> None:
    """Check namespace is parsed/validated correctly.

    Args:
        tmp_path: The path in which the reposiotry is to be initialized.
            Provided by fixture.
    """
    new_repo = tmp_path / "my-website"
    namespace = Namespace(
        directory=str(new_repo),
        author="Fred",
        no_input=True,
        use_defaults=True,
        site_name=None,
        timezone="Pacific/Auckland",
        default_lang=None,
        site_url=None,
        quiet=True,
        minimal_install=False,
        no_commit=False,
        use_gh_cli=False,
    )
    config = InitConfiguration.from_args(namespace)
    assert config.directory == new_repo
    assert config.author == "Fred"
    assert config.input_mode == InputMode.REJECT_INPUT
    assert config.handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS
    assert config.site_name == "my-website"
    assert config.timezone == "Pacific/Auckland"
    assert config.default_lang == "en"
    assert config.site_url == "https://my-website.github.io"
    assert config.verbosity == Verbosity.QUIET


def test_turbo_configuration_default_site_url_regular(tmp_path: Path) -> None:
    """Checks a valid site URL can be inferred from a repository."""
    assert (
        InitConfiguration._default_site_url(tmp_path / "repo-name")
        == "https://repo-name.github.io"
    )


def test_turbo_configuration_default_site_url_explicit(tmp_path: Path) -> None:
    """Checks a valid site URL can be inferred from a repository with explicit name."""
    assert (
        InitConfiguration._default_site_url(tmp_path / "repo_name.github.io")
        == "https://repo-name.github.io"
    )


def test_turbo_configuration_default_site_url_invalid(tmp_path: Path) -> None:
    """Checks a valid site URL can be inferred from a repository with explicit name."""
    assert InitConfiguration._default_site_url(tmp_path / "?") is None
