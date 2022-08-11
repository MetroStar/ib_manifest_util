from pathlib import Path

from ib_manifest_util import TEMPLATE_DIR
from ib_manifest_util.util import write_templatized_file

DOCKERFILE_TPL = "Dockerfile_conda.tpl"


def write_dockerfile(
    noarch_packages: list,
    linux_packages: list,
    underscore_packages: list,
    startup_scripts: list,
    run_startup_scripts: list,
    output_path: str | Path,
):
    """Write Dockerfile for Iron Bank Container.

    The Iron Bank Dockerfiles follow a specific format. This function
    covers most usecases, but should be reviewed for accuracy.

    Args:
        noarch_packages: list
            List of noarch packages to be copied into `/noarch` dir
        linux_packages: list
            List of Linux-64 packages to be copied into `/linux-64` dir
        underscore_packages: list
            List of packages with an leading underscore. These requiring
            special handling in Iron Bank
        startup_scripts: list
            List of additional files to be copied into the Dockerfile
        run_startup_scripts: list
            List of RUN statements for the startup_scripts
        output_path: str | Path
            Output path for the created Dockerfile
    """

    copy_notebook_config = True

    mkdirs = [
        "/home/${NB_USER}/work",
        "/home/${NB_USER}/conf",
        "/home/${NB_USER}/tip_scripts",
    ]

    extra_entrypoints = [
        ".init/start.sh",
    ]

    content_dict = {
        "base_image": "ironbank/opensource/metrostar/miniconda",
        "base_tag": "4.11.0",
        "noarch_packages": noarch_packages,
        "linux_packages": linux_packages,
        "underscore_packages": underscore_packages,
        "startup_scripts": startup_scripts,
        "run_startup_scripts": run_startup_scripts,
        "copy_notebook_config": copy_notebook_config,
        "mkdirs": mkdirs,
        "extra_entrypoints": extra_entrypoints,
    }

    write_templatized_file(
        DOCKERFILE_TPL, output_path, content_dict, template_dir=TEMPLATE_DIR
    )
