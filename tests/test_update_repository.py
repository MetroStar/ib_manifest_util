from pathlib import Path
import pytest

from ib_manifest_util import update_repository


@pytest.mark.web
def test_update_repository(repo_dir, tmpdir):
    update_repository.update_repo(
        repo_dir=repo_dir,
        dockerfile_version="9999",
        local_env_path=repo_dir.joinpath("scripts", "local_channel_env.yaml"),
        output_hardening_path=Path(tmpdir.join("output_hardening_manifest.yaml")),
        output_dockerfile_path=Path(tmpdir.join("output_dockerfile")),
        dockerfile_template_path=None,
    )
