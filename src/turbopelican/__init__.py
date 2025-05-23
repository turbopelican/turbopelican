"""turbopelican - the fastest way to set up GitHub Pages with Pelican.

Author: Elliot Simpson.
"""

__all__ = [
    "Configuration",
    "PelicanConfig",
    "PelicanConfiguration",
    "PublishConfiguration",
    "TurbopelicanError",
    "config",
    "load_config",
]

from turbopelican._utils.config import (
    Configuration,
    PelicanConfig,
    PelicanConfiguration,
    PublishConfiguration,
    config,
    load_config,
)
from turbopelican._utils.errors import TurbopelicanError
