import logging
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML

from ib_manifest_util import TEMPLATE_DIR
from ib_manifest_util.version import __version__

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

    NOTE: It is assumed that the `conda-vendor vendor` command has already been run and that the `local_channel_env`
    has a single channel set to `path/to/local_channel/folder`.
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
    channels = env_yaml["channels"]
    name = env_yaml["name"]

    if channels and len(channels) > 1 or not Path(channels[0]).exists():
        raise ValueError(
            f"The `channels` key for {local_channel_env} is misformatted: {channels}. It should only contain one item, the file path to the local channel folder"
        )

    if conda_binary_loc:
        if isinstance(conda_binary_loc, str):
            conda_binary_loc = Path(conda_binary_loc)
        if not conda_binary_loc.exists():
            raise ValueError(
                f"The `conda` binary provided appears not to exist at location: {conda_binary_loc.resolve()}"
            )
        conda_binary = str(conda_binary_loc)
    else:
        try:
            # determine location of conda binary
            conda_binary = run_subprocess("which conda", return_as_str=True).strip("\n")
        except Exception as e:
            logger.warning(
                "Having trouble determine the location of the `conda` binary, falling back to simply using `conda`"
            )
    logger.info(f"Using the following `conda` binary: {conda_binary}")

    create_conda_env_command = conda_binary + f" env create -f {local_channel_env}"
    remove_conda_env_command = conda_binary + f" env remove -n {name}"

    if offline_mode:
        create_conda_env_command += " --offline"

    try:
        logger.info(f"Creating conda environment, `{name}`, from {local_channel_env}")
        run_subprocess(create_conda_env_command)
        logger.info(f"Conda environment, `{name}`, successfully created")
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        logger.info(f"Removing conda environment, `{name}`, from {local_channel_env}")
        run_subprocess(remove_conda_env_command)
        logger.info(f"Conda environment, `{name}`, successfully removed")

    logger.info(
        f"The local channel environment, {local_channel_env}, was successfully created (and then promptly removed)"
    )

    return True
