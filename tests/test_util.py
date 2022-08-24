import shutil
import urllib
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from ib_manifest_util import TEMPLATE_DIR, TEST_DATA_DIR
from ib_manifest_util.config import DockerCondaConfig, HardeningManifestConfig
from ib_manifest_util.util import download_files, write_templatized_file


@pytest.fixture
def cleanup():
    """Ensure removal of test files after testing is done.

    Call this function from the test function and append Path objects
    to it for cleaning up, even if the assertion fails.

    """
    to_delete = []
    yield to_delete
    for item in to_delete:
        if Path(item).exists:
            item.unlink()


def load_yaml_for_tests(file_path: str | Path, loader_type: str = "safe") -> dict:
    """Load a yaml file.

    This provides a method for loading yaml files independent of utils.load_yaml.

    Args:
        file_path: Path to yaml file.
        loader_type: Type of loader to use (see ruamel.yaml).

    Returns: dict
    """
    yaml_loader = YAML(typ=loader_type)
    file_path = Path(file_path).resolve()
    with open(file_path, "r") as f:
        return yaml_loader.load(f)


def write_templatized_file_test(config_class):
    """Test ability to write file with a template.

    Args:
        config_class:
            Class that holds configuration data

    """

    write_templatized_file(
        template_filename=config_class.template_name,
        output_path=config_class.output_path,
        content=config_class.content,
        template_dir=config_class.template_dir,
    )

    # Check that the file was written
    assert (
        config_class.output_path.exists()
    ), f"Templatized file should exist here: {config_class.output_path}"

    # Compare file content with expected content
    output = load_yaml_for_tests(config_class.output_path)
    expected = load_yaml_for_tests(config_class.expected_output_path)
    assert output == expected


def test_write_templatized_file_hardening():
    """Test hardening_manifest.yaml"""
    write_templatized_file_test(HardeningManifestConfig())


def test_write_templatized_file_ib_manifest():
    pass


def test_write_templatized_file_local_channel_env():
    pass


def test_write_templatized_file_start_scripts():
    pass


def test_download_file_good_url(cleanup):
    """Test downloading from good URLs."""

    url = "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2"
    f_name = download_files(urls=[url])[0]
    f_path = Path(f_name).resolve()

    cleanup.append(f_path)

    assert f_name == "backports-1.0-py_2.tar.bz2", "Filename should match name in URL."

    assert f_path.exists(), f"File should be written to {f_path}."

    size = f_path.stat().st_size
    assert 3000 < size < 4000, "File size should be around 3.6kB."


def test_download_file_bad_url():
    """Test downloading from bad URLs, with typos, incomplete paths, etc."""

    # Unknown URL type: ValueError (Missing https://)
    url = "conda.anaconda.org"
    with pytest.raises(ValueError):
        download_files(urls=[url])

    # Forbidden (No path to file)
    url = "https://conda.anaconda.org"
    with pytest.raises(urllib.error.HTTPError):
        download_files(urls=[url])

    # Not found (Dummy package name)
    url = "https://conda.anaconda.org/conda-forge/noarch/dd812b10e81f8afcf74310a39b69fca49c27d847.tar.bz2"
    with pytest.raises(urllib.error.HTTPError):
        download_files(urls=[url])


def test_download_file_multiple_urls(cleanup):
    """Test downloading more than one file."""
    urls = [
        "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2",
        "https://conda.anaconda.org/conda-forge/noarch/typing-extensions-4.3.0-hd8ed1ab_0.tar.bz2",
    ]
    f_names = download_files(urls=urls)

    for f_name in f_names:
        f_path = Path(f_name).resolve()
        cleanup.append(f_path)
        assert f_path.exists(), f"File should be written to {f_path}."
