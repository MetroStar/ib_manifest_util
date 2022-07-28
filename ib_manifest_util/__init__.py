import pkg_resources

from ib_manifest_util.ib_manifest_util import main

__all__ = ["main"]

"""
Iron Bank Manifest Utility

A command line tool to assist with updating and testing Iron Bank images.
"""

try:
    __version__ = pkg_resources.get_distribution("ib_manifest_util").version
except Exception:
    __version__ = "unknown"

__app_name__ = "Iron Bank Manifest Utility"
__version__ = "0.1.0"
__author__ = "Ryan Crow, Tyler Potts"
