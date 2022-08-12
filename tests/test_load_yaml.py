import pytest

from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.util import load_yaml


def test_path_types():
    """Test load_yaml file_path arg"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

    # Test path type str
    hardening_manifest = load_yaml(file_path=str(hardening_manifest_path))
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."

    # Test path type Path
    hardening_manifest = load_yaml(file_path=hardening_manifest_path)
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."

    # Test missing file
    with pytest.raises(FileNotFoundError):
        load_yaml("this_file_does_not_exist.yaml")


def test_return_type():
    """Test load_yaml return type"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")
    hardening_manifest = load_yaml(file_path=hardening_manifest_path)
    assert isinstance(
        hardening_manifest, dict
    ), "Returned object should be a dictionary."


def test_loaders():
    """Test load_yaml loader_type arg"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

    # Test safe load
    hardening_manifest = load_yaml(
        file_path=hardening_manifest_path, loader_type="safe"
    )
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."

    # TODO: Test round trip

    # TODO: Test other loaders
