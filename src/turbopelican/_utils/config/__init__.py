"""This package contains code for the user to load Pelican configuraiton.

Author: Elliot Simpson.
"""

__all__ = [
    "Configuration",
    "PelicanConfig",
    "PelicanConfiguration",
    "PublishConfiguration",
    "config",
    "load_config",
]

from turbopelican._utils.config.config import PelicanConfig, config
from turbopelican._utils.config.legacy import (
    Configuration,
    PelicanConfiguration,
    PublishConfiguration,
    load_config,
)
