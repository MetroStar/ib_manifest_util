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

    with open(output_path, mode="w", encoding="utf-8") as message:
        message.write(template_content)


# TODO: Make test
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
        raise FileNotFoundError


def run_subprocess(command: str):
    """Run generic subprocess command.

    Args:
        command: Command to be run as a subprocess
    """
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    for line in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.write(line.decode("utf-8"))


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
