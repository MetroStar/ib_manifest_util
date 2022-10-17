from ib_manifest_util.create_hardening_manifest import update_hardening_manifest
from ib_manifest_util import PACKAGE_DIR, TEST_DATA_DIR

DOCKERFILE_VERSION = 9999
HARDENING_MANIFEST_PATH = TEST_DATA_DIR.joinpath('hardening_manifest.yaml')
IB_MANIFEST_PATH = TEST_DATA_DIR.joinpath('ib_manifest.yaml')
STARTUP_SCRIPTS_PATH = TEST_DATA_DIR.joinpath('start_scripts.yaml')


def test_update_hardening_manifest_no_start_scripts():
    update_hardening_manifest(
        dockerfile_version=DOCKERFILE_VERSION,
        hardening_manifest_path=HARDENING_MANIFEST_PATH,
        ib_manifest_path=IB_MANIFEST_PATH,
        startup_scripts_path=None,
        output_path='tmp',
    )

def test_update_hardening_manifest_with_start_scripts():
    update_hardening_manifest(
        dockerfile_version=DOCKERFILE_VERSION,
        hardening_manifest_path=HARDENING_MANIFEST_PATH,
        ib_manifest_path=IB_MANIFEST_PATH,
        startup_scripts_path=STARTUP_SCRIPTS_PATH,
        output_path='tmp',
    )