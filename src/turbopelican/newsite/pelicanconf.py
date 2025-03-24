"""Configures Pelican.

Author: Elliot Simpson
"""

import tomllib
from pathlib import Path

with Path("turbopelican.toml").open("rb") as config:
    turbopelican_config = tomllib.load(config)


AUTHOR = turbopelican_config["pelican"]["author"]
SITENAME = turbopelican_config["pelican"]["sitename"]
SITEURL = turbopelican_config["publish"]["site_url"]

PATH = "content"

TIMEZONE = turbopelican_config["pelican"]["timezone"]

DEFAULT_LANG = turbopelican_config["pelican"]["default_lang"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = False
