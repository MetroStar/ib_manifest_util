from pathlib import Path

import pytest
from ruamel.yaml import YAML

from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.util import dump_yaml


def load_yaml_for_testing(file_path: str | Path) -> dict:
    """Load a yaml file.

    This provides a method for loading yaml files independent of utils.load_yaml.
    Args:
        file_path: str | Path
            Path to yaml file.
    Returns: dict
    """

    yaml_loader = YAML(typ="safe")
    file_path = Path(file_path).resolve()
    if file_path.exists():
        with open(file_path, "r") as f:
            return yaml_loader.load(f)
    else:
        raise FileNotFoundError


def test_path_types():
    """Test load_yaml file_path arg"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

    sample_yaml = load_yaml_for_testing("sample_yaml.yaml")
    print(sample_yaml)

    # Test path type str
    dump_yaml(
        sample_yaml, target_path=str(hardening_manifest_path), dumper_type=str("unsafe")
    )
    hardening_manifest = load_yaml_for_testing(hardening_manifest_path)
    print(hardening_manifest)
    assert (
        hardening_manifest["myKey"] == "myValue"
    ), "Loaded yaml file should provide correct key-value pair."

    # Test path type Path
    dump_yaml(
        sample_yaml, target_path=hardening_manifest_path, dumper_type=str("unsafe")
    )
    hardening_manifest = load_yaml_for_testing(hardening_manifest_path)
    assert (
        hardening_manifest["myKey"] == "myValue"
    ), "Loaded yaml file should provide correct key-value pair."


# def test_loaders():
#    """Test load_yaml loader_type arg"""
#    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

# Test safe load
#    hardening_manifest = dump_yaml(
#        file_path=hardening_manifest_path, loader_type="safe"
#    )
#    assert (
#        hardening_manifest["apiVersion"] == "v1"
#    ), "Loaded yaml file should provide correct key-value pair."

# TODO: Test round trip

# TODO: Test other loaders
