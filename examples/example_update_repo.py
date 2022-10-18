from pathlib import Path

from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.update_repository import update_repo

repo_dir = TEST_DATA_DIR.joinpath("sample_repo")
output_dir = Path(".").joinpath("example_output")

update_repo(
    repo_dir=repo_dir,  # path to the IB Repo
    dockerfile_version="9999",  # incremental IB Repo version for dockerfile
    local_env_path=repo_dir.joinpath("scripts", "local_channel_env.yaml"),  # defaults to the one in `repo_dir`
    output_hardening_path=output_dir.joinpath("output_hardening_manifest.yaml"),  # defaults to overwrite the one in `repo_dir`
    output_dockerfile_path=output_dir.joinpath("output_dockerfile"), # defaults to overwrite the one in `repo_dir`
    dockerfile_template_path=None,  # defaults to `repo_dir/scripts/Dockerfile.tpl`
)
