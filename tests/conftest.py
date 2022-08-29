import pytest

from ib_manifest_util import TEST_DATA_DIR


@pytest.fixture
def repo_dir():
    """Pathlib Path to the sample IB repo folder"""
    return TEST_DATA_DIR.joinpath("sample_repo")
