import logging
import re
import subprocess
import sys
import time
from cmath import log
from email.mime import image
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML

from ib_manifest_util import TEMPLATE_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def write_templatized_file(
    template_filename: str | Path,
    output_path: str | Path,
    content: dict,
    template_dir: str | Path = TEMPLATE_DIR,
):
    """Generic file writer for Jinja2 templates

    Args:
        template_filename: Filename of Jinja template (not including directory)
        output_path: Full path for the output file to be written
        content: Dictionary with keys matching expected Jinja variables
        template_dir: Path to the Jinja template directory
    """
    environment = Environment(loader=FileSystemLoader(template_dir))
    template = environment.get_template(str(template_filename))

    template_content = template.render(**content)

    if isinstance(output_path, str):
        output_path = Path(output_path)

    # make the output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, mode="w", encoding="utf-8") as message:
        message.write(template_content)


def load_yaml(file_path: str | Path, loader_type: str = "safe") -> dict:
    """Load a yaml file after checking that it exists.

    Args:
        file_path: str | Path
            Full path to yaml file.
        loader_type: str
            Options from yaml docstring:
                'rt'/None -> RoundTripLoader/RoundTripDumper,  (default)
                'safe'    -> SafeLoader/SafeDumper,
                'unsafe'  -> normal/unsafe Loader/Dumper
                'base'    -> baseloader

    Returns: dict

    """
    yaml_loader = YAML(typ=loader_type)

    file_path = Path(file_path).resolve()
    if file_path.exists():
        with open(file_path, "r") as f:
            return yaml_loader.load(f)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")


def dump_yaml(
    source_dict: dict,
    target_path: str | Path,
    dumper_type: str = "safe",
    flow_style: bool = False,
):
    """Write dict as yaml format into a target file.
    Args:
        source_dict: Dictionary to dump into the target file.
        target_path: Full path to target yaml file.
        dumper_type:
            Options from yaml docstring:
                'rt'/None -> RoundTripLoader/RoundTripDumper,  (default)
                'safe'    -> SafeLoader/SafeDumper,
                'unsafe'  -> normal/unsafe Loader/Dumper
                'base'    -> baseloader
        flow_style:
            Options from yaml docstring:
                'True'    -> output dictionary in block style
                'False'   -> output dictionary in flow style
    """
    yaml_dumper = YAML(typ=dumper_type)
    yaml_dumper.default_flow_style = flow_style

    with open(target_path, "w") as target:
        yaml_dumper.dump(source_dict, target)


def run_subprocess(command: str, return_as_str=False):
    """Run generic subprocess command.

    Args:
        command: Command to be run as a subprocess
        return_as_str: Return the subprocess stdout as a string instead of streaming to stdout
    """
    encoding = "utf-8"
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)

    if return_as_str:
        return process.stdout.read().decode(encoding)

    for line in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.write(line.decode(encoding))


def download_files(urls: str | list) -> list:
    """Download files from a list of urls.

    Downloads the files to the current directory and saves as the filename
    found in the urls.

    Args:
        urls: URLs to be downloaded

    Returns:
        Names of downloaded files
    """
    if isinstance(urls, str):
        urls = [urls]

    filenames = []
    for address in urls:
        # extract the filename to save locally
        filename = Path(urlparse(address).path).name

        # download the file
        urlretrieve(address, Path(filename))
        filenames.append(filename)

        logger.info(f"Downloaded file {filename} from {address}.")

    return filenames


def verify_local_channel_environments(
    local_channel_env: str | Path,
    offline_mode: bool = True,
    conda_binary_loc: str | Path | None = None,
):
    """
    Verify that the conda environment (`local_channel_env`) can be successfully created.

    Args:
        local_channel_env: path to local environment yaml
        offline_mode: whether to run `conda env create` with the `--offline` flag, default is true
        conda_binary_loc: path to a `conda` binary, default will try to locate the `conda` binary by using the return value of `$ which conda`

    Returns:
        bool: `True` if successful, `False` if not.

    NOTE: It is assumed that the `conda-vendor vendor` command has already been run and that the `local_channel_env`
    has a single channel set to `path/to/local_channel/folder`.

    NOTE: If the local channel folder is in the current working directory, it is also advised to prepend the folder name with `./`,
    such as `./my_local_channel_env` to ensure that `conda` understands that this is a local channel.
    """

    logger.info(
        "Verifying that the local channel environment can be successfully created"
    )
    if isinstance(local_channel_env, str):
        local_channel_env = Path(local_channel_env)

    if not local_channel_env.exists():
        raise ValueError(
            f"The environment file submitted appears not to exist at location: {local_channel_env.resolve()}"
        )

    env_yaml = load_yaml(local_channel_env)
    channels = env_yaml.get("channels", None)
    name = env_yaml.get("name", None)

    if channels and len(channels) > 1 or not Path(channels[0]).exists():
        raise ValueError(
            f"The `channels` key for {local_channel_env} is misformatted: {channels}. It should only contain one item, the file path to the local channel folder"
        )

    # if conda binary was provided, ensure that it exists
    if conda_binary_loc:
        if isinstance(conda_binary_loc, str):
            conda_binary_loc = Path(conda_binary_loc)
        if not conda_binary_loc.exists():
            raise ValueError(
                f"The `conda` binary provided appears not to exist at location: {conda_binary_loc.resolve()}"
            )
        conda_binary = str(conda_binary_loc)
    # otherwise find conda binary via `which`
    else:
        try:
            # determine location of conda binary
            conda_binary = run_subprocess("which conda", return_as_str=True).strip("\n")
        except Exception as e:
            logger.error(
                "Having trouble determining the location of the `conda` binary."
            )
            raise e
    logger.info(f"Using the following `conda` binary: {Path(conda_binary).resolve()}")

    create_conda_env_command = conda_binary + f" env create --file {local_channel_env}"
    remove_conda_env_command = conda_binary + f" remove --name {name}"

    if offline_mode:
        create_conda_env_command += " --offline"

    try:
        logger.info(f"Creating conda environment, `{name}`, from {local_channel_env}")
        # catch exception if command fails
        subprocess.check_call(
            create_conda_env_command.split(" "), stdout=sys.stdout, stderr=sys.stderr
        )
        logger.info(f"Conda environment, `{name}`, successfully created")
    except Exception as e:
        logger.error(e)
        return False
    finally:
        logger.info(f"Removing conda environment, `{name}`, from {local_channel_env}")
        run_subprocess(remove_conda_env_command)
        logger.info(f"Conda environment, `{name}`, successfully removed")

    logger.info(
        f"The local channel environment, {local_channel_env}, was successfully created (and then promptly removed)"
    )

    return True


def patch_base_image(
    image_name: str | None = None,
    image_tag: str | None = None,
    dockerfile: str | Path = "Dockerfile",
    patch_existing: bool = False,
):
    """
    Replace the base image used by the `dockerfile` with `image_name:image_tag`.
    """

    if isinstance(dockerfile, str):
        dockerfile = Path(dockerfile)

    if image_name and image_tag:
        image_name_tag = f"{image_name}:{image_tag}"
    else:
        raise ValueError("Please provide both image name and image tag.")

    # match on lines that start with `FROM ...`
    pattern = "^(FROM.+)"
    new_base_image = f"FROM {image_name_tag.strip('FROM').strip()}"

    logger.info(f"Replacing existing base image with: {new_base_image}")

    with open(dockerfile, "r") as f:
        filedata = f.read()

    filedata = re.sub(pattern, new_base_image, filedata, flags=re.MULTILINE)

    if patch_existing:
        dockerfile_patched = dockerfile
        logger.info(f"Patching the Dockerfile provided: {dockerfile.resolve()}")
    else:
        dockerfile_patched = dockerfile.with_suffix(".patched")
        logger.info(
            f"Creating a new Dockerfile.patched: {dockerfile_patched.resolve()}"
        )

    with open(dockerfile_patched, "w") as f:
        f.write(filedata)

    logger.info("The Dockerfile base image has been patched successfully.")

    return dockerfile_patched


def verify_dockerfile(
    image_name: str | None = None,
    image_tag: str | None = None,
    dockerfile: str | Path = "Dockerfile.patched",
    base_dir: str | Path = ".",
):
    """
    Build `dockerfile`. To patch base image used, provide `image_name` and `image_tag`.
    """
    if isinstance(dockerfile, str):
        dockerfile = Path(dockerfile)
    if image_name and image_tag:
        image_name_tag = f"{image_name}:{image_tag}"
    elif not (image_name and image_tag):
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        image_name_tag = f"verify_dockerfile:{timestamp}"
    else:
        logger.error(
            "Please provide both `image_name` and `image_tag`, or neither altogether."
        )
        raise ValueError

    build_command = (
        f"docker build -f {dockerfile.resolve()} -t {image_name_tag} {base_dir}"
    )
    remove_command = f"docker rmi --force {image_name_tag}"

    try:
        logger.info(
            f"Building dockerfile: {dockerfile.resolve()} with the following command: {build_command}"
        )
        run_subprocess(build_command)
        logger.info(
            f"Docker image with name << {image_name_tag} >> has successfully been built."
        )

    except Exception as e:
        raise (e)

    finally:
        logger.info(f"Removing the built docker container.")
        run_subprocess(remove_command)
