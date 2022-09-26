import logging
import shutil
from copy import deepcopy
from pathlib import Path

from ruamel.yaml import YAML

from ib_manifest_util.util import load_yaml, run_subprocess, write_templatized_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

HARDENING_MANIFEST_TPL = "hardening_manifest.tpl"


def create_local_conda_channel(
    env_path: str | Path = "local_channel_env.yaml",
    root_channel_dir: str | Path = Path("."),
):
    """Create a local conda channel with Conda-Vendor.

    conda-vendor currently does not allow for a specified output path. Therefore,
    we'll return the path so that users can track where the new files were
    created.

    A temporary file is used to ensure that the evironment file has conda-forge
    as the only channel while preserving the original file.

    Args:
        env_path:
            Full path to `local_channel_env.yaml` that the channel will be
            based upon. Defaults to 'local_channel_env.yaml'.
        root_channel_dir:
            The root directory where the channel will be created (not
            including the channel directory itself)
    """
    # read the env file
    env = load_yaml(env_path)

    tempfile = Path("temp_env.yaml")

    # ensure that conda-forge is the only channel
    env["channels"] = ["conda-forge"]

    with open(tempfile, "w") as f:
        yaml = YAML(pure=True)
        yaml.dump(env, f)

    # get the channel name
    channel_name = env["name"]

    if isinstance(root_channel_dir, str):
        root_channel_dir = Path(root_channel_dir)

    output_path = root_channel_dir.joinpath(channel_name).resolve()

    # remove local conda channel dir if it already exists
    # TODO: remove this when conda-vendor is no longer called from subprocess
    if output_path.exists():
        logger.warning(
            f"Local channel path ({output_path}) already exists, removing existing directory before creating a new the channel"
        )
        shutil.rmtree(output_path)

    # run conda-vendor to create the local conda channel
    # this may take a while, it performs the solves and downloads all packages
    run_subprocess(f"conda-vendor vendor --file {tempfile} -p linux-64")

    return output_path


def create_ib_manifest(file: str | Path):
    """Run conda-vendor to create ib_manifest.yaml.

    Takes in a `local_channel_env.yaml` and feeds it to
    `conda-vendor ironbank-gen` which outputs a temp file `ib_manifest.yaml`.
    The `ib_manifest.yaml` file is then loaded and has its contents dumped
    into the hardening_manifest.

    conda-vendor currently does not allow for a specified output path. Therefore,
    we'll return the path so that users can track where the new files were
    created.

    A temporary file is used to ensure that the evironment file has conda-forge
    as the only channel while preserving the original file.

    Args:
        file: full path to local_channel_env.yaml
    Output:
        ib_manifest.yaml
    """
    tempfile = Path("temp_env.yaml")

    # read the local env yaml
    env = load_yaml(file)

    # ensure that conda-forge is the only channel
    env["channels"] = ["conda-forge"]

    with open(tempfile, "w") as f:
        yaml = YAML(pure=True)
        yaml.dump(env, f)

    # run conda-vendor to generate `ib_manifest.yaml`
    run_subprocess(f"conda-vendor ironbank-gen --file {tempfile} -p linux-64")
    # remove temporary file
    tempfile.unlink()

    out_path = Path(".").joinpath("ib_manifest.yaml").resolve()

    return out_path


def update_hardening_manifest(
    dockerfile_version: str,
    hardening_manifest_path: str | Path,
    ib_manifest_path: str | Path,
    startup_scripts_path=None,
    output_path=None,
):
    """Update hardening_manifest.yaml with the resouces from ib_manifest.yaml.

    Also updates the dockefile version and adds any additional startup
    scripts needed.

    Args:
        dockerfile_version:
            Dockerfile version for the hardening manifest
        hardening_manifest_path:
            Full path to the hardening_manifest.yaml
        ib_manifest_path:
            Full path to the ib_manifest.yaml
        startup_scripts_path:
            Full path to startup scripts yaml. Defaults to None.
        output_path:
            Full path to write hardening manifest. If None, the source
            `hardening_manifest_path` will be ovewritten. Defaults to None.
    """
    if not output_path:
        output_path = hardening_manifest_path
        logger.warning(
            "Separate output path for hardening_manifest.yaml has not been provided. The source hardening_manifest.yaml will be modified in place."
        )

    # Copy resources from ib_manifest into the hardening manifest
    # load the hardening manifest
    hardening_data = load_yaml(hardening_manifest_path)
    # load the ib manifest (just includes resources)
    ib_manifest = load_yaml(ib_manifest_path)

    # get the resources from the ib_manifest
    hardening_data["resources"] = ib_manifest["resources"]

    # add startup scripts to the front of the resources list
    if startup_scripts_path:
        startup_scripts = load_yaml(startup_scripts_path)
        hardening_data["resources"] = startup_scripts["resources"].extend(
            hardening_data["resources"]
        )
    hardening_data["tags"] = [dockerfile_version]

    # store resources with underscores (we'll need to flag them later)
    unclean_resources = deepcopy(hardening_data["resources"])

    # clean the leading underscores for the hardening_manifest
    for idx, resource in enumerate(hardening_data["resources"]):
        if resource["filename"].startswith("_"):
            hardening_data["resources"][idx]["filename"] = resource["filename"].lstrip(
                "_"
            )

    write_templatized_file(HARDENING_MANIFEST_TPL, output_path, hardening_data)

    return unclean_resources
