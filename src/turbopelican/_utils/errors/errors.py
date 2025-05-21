"""Defines any errors that Turbopelican users should be able to catch.

Author: Elliot Simpson
"""

__all__ = ["TurbopelicanError"]


class TurbopelicanError(ValueError):
    """Error to be raised when turbopelican raises any generic error."""
