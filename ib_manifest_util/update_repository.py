import logging
import shutil
from pathlib import Path

from ib_manifest_util.create_hardening_manifest import (
    create_ib_manifest,
    create_local_conda_channel,
    update_hardening_manifest,
)
from ib_manifest_util.dockerfiles import write_dockerfile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def update_repo(
    repo_dir: str | Path,
    dockerfile_version: str,
    local_env_path: str | Path = "local_channel_env.yaml",
    startup_scripts_path: str | Path | None = None,
    output_hardening_path: str | Path | None = None,
    output_dockerfile_path: str | Path | None = None,
    dockerfile_template_path: str | Path = None,
):
    """High level function to update an Iron Bank repository with a new environment.

    The workflow:
    1) User manually updates/adds a package into local_channel_env.yaml
    2) run conda-vendor vendor using the local_channel_env.yaml to construct a local channel
    3) copy both linux-64/repodata.json and noarch/repodata.json from the local channel to /config in the IB repo
    4) run conda-vendor ironbank-gen using the local_channel_env.yaml to create ib_manifest.yaml
    5) copy the ib_manifest.yaml contents into hardening_manifest.yaml
    6) Create a new Dockerfile with updated COPY statements for new package(s)

    Once those steps are done, users manually commit linux-64/repodata.json,
    noarch/repodata.json, hardening_manifest.yaml and Dockerfile to git, which
    then kicks off an Iron Bank pipeline

    Args:
        repo_dir: Full path to local copy of Iron Bank manifest repository.
        dockerfile_version: dockerfile version to add to hardening manifest.
        local_env_path: Optional. Full path to updated version of
            `local_channel_env.yaml`.Default: 'local_channel_env.yaml'
        startup_scripts_path: Optional. Full path to yaml file with additional startup scripts.
        output_hardening_path: output path for the new `hardening_manifest.yaml`. Use `None` to
            overwrite the version in the repo
        output_dockerfile_path: output path for the new `Dockerfile`. Use `None` to
            overwrite the version in the repo
    Returns:
        None
    """
    # ensure repo_dir is a Path object
    if isinstance(repo_dir, str):
        repo_dir = Path(repo_dir)

    # ensure local_env_path is a Path object
    if isinstance(local_env_path, str):
        local_env_path = Path(local_env_path)

    # if an output path for the Dockerfile is not provided, overwrite the one
    # in the repo
    if not output_dockerfile_path:
        output_dockerfile_path = repo_dir.joinpath("Dockerfile")

    hardening_manifest_path = repo_dir.joinpath("hardening_manifest.yaml")

    # create local channel using conda-vendor
    logger.info(f"Creating local conda channel")
    local_channel_path = create_local_conda_channel(env_path=local_env_path)

    # copy repodata.json back to the repo
    architectures = ["noarch", "linux-64"]
    filename = "repodata.json"

    # move updated repodata into repo
    for arch in architectures:
        old_path = local_channel_path.joinpath(arch, filename)
        new_path = repo_dir.joinpath("config", arch, filename)
        old_path.rename(new_path)

    # create ib_manifest using conda-vendor
    logger.info(f"Creating ib_manifest.yaml")
    ib_manifest_path = create_ib_manifest(local_env_path)

    # update hardening_manifest fom ib_manifest
    logger.info(f"Updating hardening manifest. Writing to {output_hardening_path}")
    resources = update_hardening_manifest(
        dockerfile_version=dockerfile_version,
        hardening_manifest_path=hardening_manifest_path,
        ib_manifest_path=ib_manifest_path,
        startup_scripts_path=startup_scripts_path,
        output_path=output_hardening_path,
    )
    noarch_packages = []
    linux_packages = []
    startup_scripts = []
    underscore_packages = []

    for resource in resources:
        if "noarch" in resource["url"]:
            if resource["filename"][0] == "_":
                underscore_packages.append(resource["filename"][1:])
            else:
                noarch_packages.append(resource["filename"])
        elif "linux-64" in resource["url"]:
            if resource["filename"][0] == "_":
                underscore_packages.append(resource["filename"][1:])
            else:
                linux_packages.append(resource["filename"])
        else:
            startup_scripts.append(resource["filename"])

    run_startup_scripts = 'mv "/home/${NB_USER}/code_server.tar.gz" /usr/local/bin/ \
        && mv "/home/${NB_USER}/start.sh" /usr/local/bin/ \
        && mv "/home/${NB_USER}/start-notebook.sh" /usr/local/bin/ \
        && mv "/home/${NB_USER}/start-singleuser.sh" /usr/local/bin/ \
        && chmod +x /usr/local/bin/start.sh \
        && chmod +x /usr/local/bin/start-notebook.sh \
        && chmod +x /usr/local/bin/start-singleuser.sh'

    # update the Dockerfile
    logger.info(f"Writing Dockerfile to {output_dockerfile_path}")
    write_dockerfile(
        noarch_packages,
        linux_packages,
        underscore_packages,
        startup_scripts,
        run_startup_scripts,
        output_path=output_dockerfile_path,
        dockerfile_template_path=dockerfile_template_path,
    )

    # clean up ib_manifest.yaml
    logger.info(
        f"Cleaning up. Removing {ib_manifest_path} and local conda channel {local_channel_path}"
    )
    ib_manifest_path.unlink()
    shutil.rmtree(local_channel_path)
