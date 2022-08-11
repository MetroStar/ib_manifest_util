from pathlib import Path

VERSION = "0.1.0"

PACKAGE_DIR = Path(__file__).parent.resolve()
DEVELOPMENT_DIR = PACKAGE_DIR.joinpath("..").resolve()
TEMPLATE_DIR = PACKAGE_DIR.joinpath("templates")
TEST_DATA_DIR = DEVELOPMENT_DIR.joinpath("tests", "data")

"""
Iron Bank Manifest Utility

A command line tool to assist with updating and testing Iron Bank images.
"""

__app_name__ = "Iron Bank Manifest Utility"
__version__ = VERSION
__author__ = "Ryan Crow, Tyler Potts"
