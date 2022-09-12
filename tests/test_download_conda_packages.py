from pathlib import Path

import pytest

from ib_manifest_util import PACKAGE_DIR, TEST_DATA_DIR
from ib_manifest_util.download_conda_packages import download_packages
from ib_manifest_util.util import load_yaml


@pytest.fixture()
def small_package_url_and_filename():
    return (
        "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2",
        "backports-1.0-py_2.tar.bz2",
    )


def assert_exist_then_delete(file_path: str | Path, file_size_minimum: int = 100):
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


@pytest.mark.web
def test_download_package_correct_url_list(small_package_url_and_filename):
    """Download a package and check that it was written successfully."""

    url_l = [small_package_url_and_filename[0]]
    expected_file_path = Path(PACKAGE_DIR, small_package_url_and_filename[1])

    # Write the file
    download_packages(urls=url_l)

    # Check that the package was downloaded
    assert_exist_then_delete(file_path=expected_file_path)


@pytest.mark.web
def test_download_package_incorrect_url_list():
    """Try downloading a dummy url and check that it was not written."""

    url_l = ["https://github.com/dummy_url_for_testing.tar.gz"]
    expected_file_name = "dummy_url_for_testing.tar.gz"

    # Try to write the file
    download_packages(urls=url_l)

    # Check that the package file is missing
    expected_file = Path(PACKAGE_DIR, expected_file_name)
    assert (
        not expected_file.exists()
    ), "Conda package should not be written to the expected path because the url was a dummy."


@pytest.mark.web
def test_download_package_from_manifest():
    """Download packages from a manifest file and check that all files were written successfully."""

    # Pass a manifest file from the tests/data dir to download_packages()
    manifest_file_path = Path(TEST_DATA_DIR, "hardening_manifest.yaml")
    download_packages(manifest_path=manifest_file_path)

    # Get list of file names for checking
    manifest = load_yaml(file_path=manifest_file_path)
    file_names = [x["url"].split("/")[-1].lstrip("_") for x in manifest["resources"]]

    # Check that files were downloaded and then delete them (clean up)
    for fn in file_names:
        expected_file_path = Path(PACKAGE_DIR, fn)
        assert_exist_then_delete(file_path=expected_file_path)


@pytest.mark.web
def test_download_package_urls_and_manifest(small_package_url_and_filename):
    """Test both url list and manifest path passed to function."""

    url_l = [small_package_url_and_filename[0]]
    expected_file_path = Path(PACKAGE_DIR, small_package_url_and_filename[1])

    download_packages(
        manifest_path=Path(TEST_DATA_DIR, "hardening_manifest.yaml"), urls=url_l
    )

    # Check that small package in the url list was downloaded
    assert_exist_then_delete(file_path=expected_file_path)

    # Check that one of the manifest packages was not downloaded
    expected_file = Path(PACKAGE_DIR, "tzdata-2022a-h191b570_0.tar.bz2")
    assert (
        not expected_file.exists()
    ), "Conda package should not be written to the expected path because manifest urls should not have been used."


@pytest.mark.web
def test_download_package_no_urls_no_manifest():
    """Test neither url list nor manifest path passed to function.

    download_packages() should look for the default manifest file in the parent directory.
    If one does not exist, test for FileNotFoundError.
    """
    manifest_path = Path(PACKAGE_DIR, "hardening_manifest.yaml")
    if manifest_path.exists():
        download_packages()

        # Get list of file names for checking
        manifest = load_yaml(file_path=manifest_path)
        file_names = [
            x["url"].split("/")[-1].lstrip("_") for x in manifest["resources"]
        ]

        # Check that files were downloaded and then delete them (clean up)
        for fn in file_names:
            expected_file_path = Path(PACKAGE_DIR, fn)
            assert_exist_then_delete(file_path=expected_file_path)
    else:
        with pytest.raises(expected_exception=FileNotFoundError):
            download_packages()
