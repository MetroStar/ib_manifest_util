import logging
import shutil
from pathlib import Path

from ib_manifest_util import TEMPLATE_DIR
from ib_manifest_util.util import write_templatized_file

DOCKERFILE_TPL = "Dockerfile_default.tpl"
DEFAULT_DOCKERFILE_PATH = TEMPLATE_DIR.joinpath(DOCKERFILE_TPL)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def copy_docker_template_to_repo(
    repo_dir: str | Path,
    template_file: str | Path = DEFAULT_DOCKERFILE_PATH,
    overwrite: bool = False,
):
    """Copy a Dockerfile template into a new location.
    Used to copy default Dockerfile template(s) from this package into an
    IronBank repo.

    Args:
        repo_dir (str | Path): Repository where the Dockerfile will be stored.
        template_file (str | Path, optional): Full file path to the template
            Dockerfile to be copied. Defaults to DEFAULT_DOCKERFILE_PATH.
        overwrite (bool, optional): If True, the Dockerfile in `repo_dir` will
            be overwritten. Defaults to False.

    Returns:
        bool: True if file was successfully written
    """

    repo_dockerfile = Path(repo_dir).joinpath("Dockerfile")

    if not overwrite and repo_dockerfile.exists():
        # check to see if there is a file there
        logging.warning(
            f"No file written. Dockerfile already exists in "
            f"directory {repo_dir}. Remove this file or pass `overwrite=True`."
        )
        return False

    # copy file from src to dst
    shutil.copy(str(template_file), str(repo_dockerfile))

    return True


def write_dockerfile(
    noarch_packages: list,
    linux_packages: list,
    underscore_packages: list,
    output_path: str | Path,
    dockerfile_template_path: str | Path = None,
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
        output_path: str | Path
            Output path for the created Dockerfile
        dockerfile_template_path: str | Path
            Full path to the template for the dockerfile
    """

    content_dict = {
        "noarch_packages": noarch_packages,
        "linux_packages": linux_packages,
        "underscore_packages": underscore_packages,
    }

    if dockerfile_template_path:
        # ensure path is pathlib.Path
        if isinstance(dockerfile_template_path, str):
            dockerfile_template_path = Path(dockerfile_template_path)
        docker_template = dockerfile_template_path.name
        template_dir = dockerfile_template_path.parent.resolve()
    else:
        logger.info(
            f"Dockerfile not provided or found in repo, using default template, {TEMPLATE_DIR.joinpath(DOCKERFILE_TPL)}"
        )
        docker_template = DOCKERFILE_TPL
        template_dir = TEMPLATE_DIR
    write_templatized_file(
        docker_template,
        output_path,
        content_dict,
        template_dir=template_dir,
    )
