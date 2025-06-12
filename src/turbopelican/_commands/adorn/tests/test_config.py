from argparse import Namespace
from pathlib import Path

from turbopelican._commands.adorn.config import AdornConfiguration
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
    )
    config = AdornConfiguration.from_args(namespace)
    assert config.directory == new_repo
    assert config.author == "Fred"
    assert config.input_mode == InputMode.REJECT_INPUT
    assert config.handle_defaults_mode == HandleDefaultsMode.USE_DEFAULTS
    assert config.site_name == "my-website"
    assert config.timezone == "Pacific/Auckland"
    assert config.default_lang == "en"
    assert config.site_url == "https://my-website.github.io"
    assert config.verbosity == Verbosity.QUIET
