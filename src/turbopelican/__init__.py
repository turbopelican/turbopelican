"""turbopelican - the fastest way to set up GitHub Pages with Pelican.

Author: Elliot Simpson.
"""

__all__ = ["Configuration", "PelicanConfiguration", "TurbopelicanError", "load_config"]

from turbopelican._utils.config import Configuration, PelicanConfiguration, load_config
from turbopelican._utils.errors import TurbopelicanError
