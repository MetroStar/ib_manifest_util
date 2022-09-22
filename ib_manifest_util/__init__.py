from pathlib import Path

from ._version import __version__

PACKAGE_DIR = Path(__file__).parent.resolve()
DEVELOPMENT_DIR = PACKAGE_DIR.joinpath("..").resolve()
TEMPLATE_DIR = PACKAGE_DIR.joinpath("templates")
TEST_DATA_DIR = DEVELOPMENT_DIR.joinpath("tests", "data")

"""
Iron Bank Manifest Utility

A command line tool to assist with updating and testing Iron Bank images.
"""

__app_name__ = "Iron Bank Manifest Utility"
__author__ = "Ryan Crow, Tyler Potts"


DEFAULT_MANIFEST_FILENAME = "hardening_manifest.yaml"
