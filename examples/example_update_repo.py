from pathlib import Path

from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.update_repository import update_repo

repo_dir = Path("/Users/kcp/projects/metrostar/demo/singleuser")
output_dir = Path(".").joinpath("example_output")

update_repo(
    repo_dir=repo_dir,
    dockerfile_version="9999",
    # local_env_path=repo_dir.joinpath("scripts", "local_channel_env.yaml"),
    startup_scripts_path="None",
    # output_hardening_path=output_dir.joinpath("output_hardening_manifest.yaml"),
    # output_dockerfile_path=output_dir.joinpath("output_dockerfile"),
    # dockerfile_template_path=None,
)
