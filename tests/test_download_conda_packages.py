from pathlib import Path

import pytest

from ib_manifest_util.download_conda_packages import download_packages


def assert_file_exists_and_has_data_then_delete(
    file_path: str | Path, file_size_minimum: int = 100
):
    """Assert that a file exists, assert that it has a minimum size, then delete it.

    Args:
        file_path: str | Path
            Path to file.
        file_size_minimum: int
            Minimum size of file in bytes.
    """
    expected_file = Path(file_path)
    assert expected_file.exists(), "File should be written to the expected path."

    size = expected_file.stat().st_size
    assert (
        size >= file_size_minimum
    ), f"File size should be at least {file_size_minimum} bytes."

    # Remove the file (clean up)
    expected_file.unlink()


def test_download_package_correct_url_list():
    """Download a package and check that it was written successfully."""
    url_l = [
        "https://github.com/dirkcgrunwald/jupyter_codeserver_proxy-/archive/5596bc9c2fbd566180545fa242c659663755a427.tar.gz"
    ]
    expected_file_path = Path("../5596bc9c2fbd566180545fa242c659663755a427.tar.gz")

    # Write the file
    download_packages(urls=url_l)

    # Check that the package was downloaded
    assert_file_exists_and_has_data_then_delete(file_path=expected_file_path)


def test_download_package_incorrect_url_list():
    """Try downloading a dummy url and check that it was not written."""
    url_l = ["https://github.com/dummy_url_for_testing.tar.gz"]
    expected_file_name = "dummy_url_for_testing.tar.gz"

    # Try to write the file
    download_packages(urls=url_l)

    # Check that the package file is missing
    expected_file = Path("../", expected_file_name)
    assert (
        not expected_file.exists()
    ), "Conda package should not be written to the expected path because the url was a dummy."


def test_download_package_from_manifest():
    # Pass a manifest file from the tests/data dir to download_packages()
    manifest_file_path = "data/hardening_manifest.yaml"
    download_packages(manifest_path=manifest_file_path)

    # Just check that the last file was downloaded
    expected_file_path = Path("../tzdata-2022a-h191b570_0.tar.bz2")
    assert_file_exists_and_has_data_then_delete(file_path=expected_file_path)


def test_download_package_urls_and_manifest():
    pass


def test_download_package_no_urls_no_manifest():
    pass
