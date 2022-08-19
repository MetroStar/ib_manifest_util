from pathlib import Path

import pytest

from ib_manifest_util.download_conda_packages import download_packages


def test_download_package_correct_url_list():
    """Download a package and check that it was written successfully."""
    url_l = [
        "https://github.com/dirkcgrunwald/jupyter_codeserver_proxy-/archive/5596bc9c2fbd566180545fa242c659663755a427.tar.gz"
    ]
    expected_file_name = "5596bc9c2fbd566180545fa242c659663755a427.tar.gz"

    # Write the file
    download_packages(urls=url_l)

    # Check that the packages was downloaded
    expected_file = Path("../", expected_file_name)
    assert (
        expected_file.exists()
    ), "Conda package should be written to the expected path."

    # Check that the file is larger than a small number of bytes
    size = expected_file.stat().st_size
    assert size > 100, "Conda package should be larger than 100 bytes."

    # Remove the package (clean up)
    expected_file.unlink()


def test_download_package_incorrect_url_list():
    """Try downloading a dummy url and check that it was not written."""
    url_l = [
        "https://github.com/dummy_url_for_testing.tar.gz"
    ]
    expected_file_name = "dummy_url_for_testing.tar.gz"

    # Try to write the file
    download_packages(urls=url_l)

    # Check that the package file is missing
    expected_file = Path("../", expected_file_name)
    assert (
        not expected_file.exists()
    ), "Conda package should not be written to the expected path because the url was a dummy."


def test_download_package_from_manifest():
    # Pass a manifest file from the tests/data dir
    # Check that the packages were downloaded
    # Remove the packages (clean up)
    pass


def test_download_package_urls_and_manifest():
    pass


def test_download_package_no_urls_no_manifest():
    pass
