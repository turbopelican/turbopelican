import datetime
import subprocess
from argparse import Namespace
from collections.abc import Generator
from contextlib import nullcontext
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import pytest

from turbopelican._commands.init import config
from turbopelican._commands.init.config import (
    ConfigurationError,
    HandleDefaultsMode,
    InitConfiguration,
    InputMode,
    Verbosity,
)

EnterContext = Generator[None, None, None]


@pytest.fixture
def git_cannot_get_author() -> EnterContext:
    """Mock out the subprocess.run function to fail."""
    with mock.patch.object(
        subprocess,
        "run",
        mock.Mock(return_value=mock.Mock(returncode=1)),
    ):
        yield


@pytest.fixture
def git_get_author_fred() -> EnterContext:
    """Mock out the subprocess.run function to fail."""
    with mock.patch.object(
        subprocess,
        "run",
        mock.Mock(return_value=mock.Mock(stdout="Fred\n", returncode=0)),
    ):
        yield


@pytest.fixture
def input_sam() -> EnterContext:
    """Mock out the input function to always return 'Sam'."""
    with mock.patch("builtins.input", mock.Mock(return_value="Sam")):
        yield


@pytest.fixture
def input_nothing() -> EnterContext:
    """Mock out the input function to always return an empty string."""
    with mock.patch("builtins.input", mock.Mock(return_value="")):
        yield


@pytest.fixture
def input_my_page() -> EnterContext:
    """Mock out the input function to always return 'My Page'."""
    with mock.patch("builtins.input", mock.Mock(return_value="My Page")):
        yield


@pytest.fixture
def input_asia_tbilisi() -> EnterContext:
    """Mock out the input function to always return 'Asia/Tbilisi'."""
    with mock.patch(
        "builtins.input",
        mock.Mock(return_value="Asia/Tbilisi"),
    ):
        yield


@pytest.fixture
def input_elf() -> EnterContext:
    """Mock out the input function to always return 'elf'."""
    with mock.patch("builtins.input", mock.Mock(return_value="elf")):
        yield


@pytest.fixture
def input_es() -> EnterContext:
    """Mock out the input function to always return 'es'."""
    with mock.patch("builtins.input", mock.Mock(return_value="es")):
        yield


@pytest.fixture
def input_site_name() -> EnterContext:
    """Mock out the input function to always return 'https://mysite.github.io'."""
    with mock.patch(
        "builtins.input",
        mock.Mock(return_value="https://mysite.github.io"),
    ):
        yield


@pytest.fixture
def get_localzone_utc() -> EnterContext:
    """Mock out the get_localzone function to always return a non-ZoneInfo instance."""
    with mock.patch.object(
        config,
        "get_localzone",
        mock.Mock(return_value=datetime.UTC),
    ):
        yield


@pytest.fixture
def get_localzone_zoneinfo() -> EnterContext:
    """Mock out the get_localzone function to always return a ZoneInfo instance."""
    with mock.patch.object(
        config,
        "get_localzone",
        mock.Mock(return_value=ZoneInfo("America/Los_Angeles")),
    ):
        yield


@pytest.fixture
def available_timezones() -> EnterContext:
    """Mock out the available_timezones function to return test timezone strings."""
    with mock.patch.object(
        config,
        "available_timezones",
        mock.Mock(return_value=["America/Los_Angeles", "Asia/Tbilisi"]),
    ):
        yield


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


def test_turbo_configuration_get_author_cli_provided() -> None:
    """Ensure that the CLI-provided author takes precedence."""
    author = InitConfiguration._get_author(
        "Fred",
        git_path="",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert author == "Fred"


def test_turbo_configuration_get_author_unavailable() -> None:
    """Ensure that an error is raised when the author cannot be obtained."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_author(
            None,
            git_path="",
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("git_cannot_get_author")
def test_turbo_configuration_get_author_git_failure_no_input() -> None:
    """Ensure when git author search fails and input not permitted, error is raised."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_author(
            None,
            git_path="",
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("git_cannot_get_author", "input_sam")
def test_turbo_configuration_get_author_git_failure_use_input() -> None:
    """Ensure when git author search fails and input permitted, standard input works."""
    author = InitConfiguration._get_author(
        None,
        git_path="",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert author == "Sam"


@pytest.mark.usefixtures("git_get_author_fred")
def test_turbo_configuration_get_author_via_git_succeed_use_default() -> None:
    """Ensure when git author search succeeds, defaults can be returned."""
    author = InitConfiguration._get_author(
        None,
        git_path="",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert author == "Fred"


@pytest.mark.usefixtures("git_get_author_fred", "input_nothing")
def test_turbo_configuration_get_author_via_git_succeed_empty_input() -> None:
    """Ensure when git author search succeeds, defaults can be shown."""
    author = InitConfiguration._get_author(
        None,
        git_path="",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert author == "Fred"


@pytest.mark.usefixtures("git_get_author_fred", "input_sam")
def test_turbo_configuration_get_author_via_git_succeed_take_input() -> None:
    """Ensure when git author search succeeds, standard input can be returned."""
    author = InitConfiguration._get_author(
        None,
        git_path="",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert author == "Sam"


def test_turbo_configuration_get_site_name_cli_provided() -> None:
    """Ensure that the CLI-provided author takes precedence."""
    site_name = InitConfiguration._get_site_name(
        cli_site_name="My Website",
        path=Path("/path/to/website"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert site_name == "My Website"


def test_turbo_configuration_get_site_name_use_defaults() -> None:
    """Ensure that the site name can be inferred from the path name."""
    site_name = InitConfiguration._get_site_name(
        cli_site_name=None,
        path=Path("/path/to/website"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert site_name == "website"


def test_turbo_configuration_get_site_name_unavailable() -> None:
    """Ensure that an error is raised when the path name cannot be obtained."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_name(
            cli_site_name=None,
            path=Path("/path/to/website"),
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("input_my_page")
def test_turbo_configuration_get_site_name_take_input() -> None:
    """Ensure that the site name can be received via standard input."""
    site_name = InitConfiguration._get_site_name(
        cli_site_name=None,
        path=Path("/path/to/website"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert site_name == "My Page"


@pytest.mark.usefixtures("input_nothing")
def test_turbo_configuration_get_site_name_empty_input() -> None:
    """Ensure that the site name, when the user provides no input, can be defaulted."""
    site_name = InitConfiguration._get_site_name(
        cli_site_name=None,
        path=Path("/path/to/website"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert site_name == "website"


def test_turbo_configuration_get_timezone_cli_provided() -> None:
    """Ensure that the timezone can be provided via the CLI."""
    timezone = InitConfiguration._get_timezone(
        "fr",
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert timezone == "fr"


def test_turbo_configuration_get_timezone_unavailable() -> None:
    """Ensures that an error is raised when the timezone cannot be obtained."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_timezone(
            None,
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("get_localzone_utc")
def test_turbo_configuration_get_timezone_default_unavailable_no_input() -> None:
    """Ensures error is raised when timezone cannot be obtained and input is blocked."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_timezone(
            None,
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("get_localzone_utc", "input_nothing")
def test_turbo_configuration_get_timezone_default_unavailable_input_empty() -> None:
    """Ensures error is raised when timezone can't be obtained and user inputs blank."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_timezone(
            None,
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("get_localzone_zoneinfo")
def test_turbo_configuration_get_timezone_use_default() -> None:
    """Ensures default timezone can be used."""
    timezone = InitConfiguration._get_timezone(
        None,
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert timezone == "America/Los_Angeles"


@pytest.mark.usefixtures("get_localzone_zoneinfo", "input_sam", "available_timezones")
def test_turbo_configuration_get_timezone_found_default_input_invalid() -> None:
    """Ensures error is raised if after default found, invalid timezone inputted."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_timezone(
            None,
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("get_localzone_utc", "input_sam", "available_timezones")
def test_turbo_configuration_get_timezone_found_no_default_input_invalid() -> None:
    """Ensures error is raised if no default found, invalid timezone inputted."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_timezone(
            None,
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures(
    "get_localzone_utc",
    "input_asia_tbilisi",
    "available_timezones",
)
def test_turbo_configuration_get_timezone_found_no_default_input_valid() -> None:
    """Ensures success if when no default found, a valid timezone is inputted."""
    timezone = InitConfiguration._get_timezone(
        None,
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert timezone == "Asia/Tbilisi"


@pytest.mark.usefixtures(
    "get_localzone_zoneinfo",
    "input_asia_tbilisi",
    "available_timezones",
)
def test_turbo_configuration_get_timezone_found_default_input_valid() -> None:
    """Ensures success if after default found, a valid timezone is inputted."""
    timezone = InitConfiguration._get_timezone(
        None,
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert timezone == "Asia/Tbilisi"


@pytest.mark.usefixtures(
    "get_localzone_zoneinfo",
    "input_nothing",
    "available_timezones",
)
def test_turbo_configuration_get_timezone_found_default_input_empty() -> None:
    """Ensures success if after default found, it is manually chosen."""
    timezone = InitConfiguration._get_timezone(
        None,
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert timezone == "America/Los_Angeles"


def test_turbo_configuration_get_default_lang_cli_provided() -> None:
    """Ensures CLI-provided default langauge takes precedence."""
    default_lang = InitConfiguration._get_default_lang(
        "fr",
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert default_lang == "fr"


def test_turbo_configuration_get_default_lang_default_used() -> None:
    """Ensures that the default language is used when defaults can be used."""
    default_lang = InitConfiguration._get_default_lang(
        None,
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert default_lang == "en"


def test_turbo_configuration_get_default_lang_reject_input() -> None:
    """Ensures error raised when no default can be used and input is not allowed."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_default_lang(
            None,
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("input_nothing")
def test_turbo_configuration_get_default_lang_input_empty() -> None:
    """Ensures default language returned when user inputs blank default language."""
    default_lang = InitConfiguration._get_default_lang(
        None,
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert default_lang == "en"


@pytest.mark.usefixtures("input_asia_tbilisi")
def test_turbo_configuration_get_default_lang_input_unparseable() -> None:
    """Ensures error when an unparseable language is provided."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_default_lang(
            None,
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("input_elf")
def test_turbo_configuration_get_default_lang_input_unrecognized() -> None:
    """Ensures error when an unrecognized language is provided."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_default_lang(
            None,
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("input_es")
def test_turbo_configuration_get_default_lang_input_recognized() -> None:
    """Ensures error when a recognized language is provided."""
    default_lang = InitConfiguration._get_default_lang(
        None,
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert default_lang == "es"


@pytest.mark.parametrize(
    ("site_url", "valid"),
    [
        ("mywebsite", False),
        ("https://mywebsite", False),
        ("mywebsite.github.io", False),
        ("https://.github.io", False),
        ("https://my$website.github.io", False),
        ("https://abc-123.github.io", True),
    ],
)
def test_turbo_configuration_validate_site_url(site_url: str, *, valid: bool) -> None:
    """Ensures an error is raised if and only if the provided site URL is invalid."""
    context = pytest.raises(ConfigurationError) if not valid else nullcontext()
    with context:
        InitConfiguration._validate_site_url(site_url)


def test_turbo_configuration_get_site_url_cli_provided() -> None:
    """Ensures that the CLI-provided site URL takes precedence."""
    site_url = InitConfiguration._get_site_url(
        "https://hello-world-123.github.io",
        Path(),
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert site_url == "https://hello-world-123.github.io"


def test_turbo_configuration_get_site_url_no_user_input() -> None:
    """Ensures error is raised when no way for URL to be obtained."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_url(
            None,
            Path(),
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


def test_turbo_configuration_get_site_url_valid_path_use_default() -> None:
    """Ensures that when path is valid and defaults used, the URL is appropriate."""
    site_url = InitConfiguration._get_site_url(
        None,
        Path("valid_website_name"),
        input_mode=InputMode.REJECT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert site_url == "https://valid-website-name.github.io"


@pytest.mark.usefixtures("input_nothing")
def test_turbo_configuration_get_site_url_valid_path_input_empty() -> None:
    """Ensures that the user can enter nothing and let the default URL be chosen."""
    site_url = InitConfiguration._get_site_url(
        None,
        Path("valid_website_name"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert site_url == "https://valid-website-name.github.io"


def test_turbo_configuration_get_site_url_invalid_path_reject_input() -> None:
    """Ensures error raised if input not allowed and website name can't be inferred."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_url(
            None,
            Path("^$"),
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("input_nothing")
def test_turbo_configuration_get_site_url_invalid_path_input_empty() -> None:
    """Ensures error raised if URL can't be inferred and user doesn't enter one."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_url(
            None,
            Path("^$"),
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("input_sam")
def test_turbo_configuration_get_site_url_valid_path_input_invalid() -> None:
    """Ensures error raised if URL can be inferred but user enters badly."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_url(
            None,
            Path("valid-website-name"),
            input_mode=InputMode.REJECT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
        )


@pytest.mark.usefixtures("input_sam")
def test_turbo_configuration_get_site_url_invalid_path_input_invalid() -> None:
    """Ensures error raised if URL can't be inferred and user enters badly."""
    with pytest.raises(ConfigurationError):
        InitConfiguration._get_site_url(
            None,
            Path("^$"),
            input_mode=InputMode.ACCEPT_INPUT,
            handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
        )


@pytest.mark.usefixtures("input_site_name")
def test_turbo_configuration_get_site_url_valid_path_input_valid() -> None:
    """Ensures error raised if URL can be inferred but user enters differently."""
    site_url = InitConfiguration._get_site_url(
        None,
        Path("valid-website-name"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.REQUIRE_STANDARD_INPUT,
    )
    assert site_url == "https://mysite.github.io"


@pytest.mark.usefixtures("input_site_name")
def test_turbo_configuration_get_site_url_invalid_path_input_valid() -> None:
    """Ensures error raised if URL can't be inferred and user enters one."""
    site_url = InitConfiguration._get_site_url(
        None,
        Path("^$"),
        input_mode=InputMode.ACCEPT_INPUT,
        handle_defaults_mode=HandleDefaultsMode.USE_DEFAULTS,
    )
    assert site_url == "https://mysite.github.io"
