import shutil

import pytest

from ib_manifest_util import TEST_DATA_DIR

# @pytest.fixture
# def repo_dir():
#     """Pathlib Path to the sample IB repo folder"""
#     print(f'test data dir: {TEST_DATA_DIR}')
#     return TEST_DATA_DIR.joinpath("sample_repo")


@pytest.fixture(scope="session")
def repo_dir(tmp_path_factory):
    sample_repo_dir = TEST_DATA_DIR.joinpath("sample_repo")
    test_output_dir = "tmp_repo1"
    fn = tmp_path_factory.mktemp(test_output_dir)
    shutil.copytree(sample_repo_dir, fn, dirs_exist_ok=True)
    import glob

    print(glob.glob(f"{fn}/*"))
    return fn
