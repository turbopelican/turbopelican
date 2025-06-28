from datetime import datetime
from pathlib import Path
from string import Template
from typing import cast
from zoneinfo import ZoneInfo

import tomlkit
import tomlkit.items

from turbopelican._utils.shared.args import CreateConfiguration


def update_website(config: CreateConfiguration) -> None:
    """Updates the Pelican website to use the provided information.

    Args:
        config: The arguments to configure the website.
    """
    turbopelican_conf = Path(config.directory) / "turbopelican.toml"

    with turbopelican_conf.open(encoding="utf8") as configuration:
        toml = tomlkit.load(configuration)

    pelican = cast("tomlkit.items.Table", toml["pelican"])
    publish = cast("tomlkit.items.Table", toml["publish"])

    pelican["author"] = config.author
    pelican["sitename"] = config.site_name
    pelican["timezone"] = config.timezone
    pelican["default_lang"] = config.default_lang
    publish["site_url"] = config.site_url

    with turbopelican_conf.open("w", encoding="utf8") as configuration:
        tomlkit.dump(toml, configuration)


def update_contents(config: CreateConfiguration) -> None:
    """Updates the Markdown contents to be ready for publication.

    Args:
        config: The arguments to configure the website.
    """
    today = datetime.now(tz=ZoneInfo(config.timezone)).date()
    for file in (config.directory / "content").glob("*.md"):
        text = file.read_text()
        file.write_text(Template(text).safe_substitute(date=today))
