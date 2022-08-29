from ib_manifest_util import update_repository


def test_update_repository(repo_dir, tmpdir):
    update_repository.update_repo(
        repo_dir=repo_dir,
        dockerfile_version="9999",
        output_hardening_path=tmpdir.join("output_hardening_manifest.yaml"),
        output_dockerfile_path=tmpdir.join("output_dockerfile"),
        dockerfile_template_path=tmpdir.join("output_dockerfile.tpl"),
    )
