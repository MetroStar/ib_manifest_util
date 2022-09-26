from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.create_hardening_manifest import update_hardening_manifest

# This example demonstrates how to update ONLY the hardening manifest

hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")
ib_manifest_path = TEST_DATA_DIR.joinpath("ib_manifest.yaml")

update_hardening_manifest(
    dockerfile_version="9999",
    hardening_manifest_path=hardening_manifest_path,
    ib_manifest_path=ib_manifest_path,
    output_path="output_hardening_manifest.yaml",
)
