import click
import requests

from ib_manifest_util.download_conda_packages import download_packages
from ib_manifest_util.update_repository import update_repo
from ib_manifest_util.version import __version__
from pathlib import Path

@click.group()
@click.version_option(__version__)
def main() -> None:
    """To display help and usage for subcommands, use: ib_manifest_util [COMMAND] --help"""
    pass

@click.command(
    "update_repo",
    help="Update the local hardening manifest and Dockerfile with necessary packages given an environment file",
)
@click.option(
    "--repo_dir",
    prompt="Please enter the absolute path of the Iron Bank repo to modify",
)
@click.option(
    "--dockerfile_version", prompt="Please enter the desired docker image version"
)
@click.option("--local_env_path", help="Path to local environment file")
@click.option(
    "--startup_scripts_path",
    help="(Optional) Path to .yaml file containing additional files to copy",
)
@click.option(
    "--output_hardening_path",
    help="(Optional) Path to location in which the hardening manifest will be placed",
)
@click.option(
    "--output_dockerfile_path",
    help="(Optional) Path to location in which the Dockerfile will be placed",
)
def update_repo_cli(
    repo_dir: str | Path,
    dockerfile_version: str,
    local_env_path: str | Path = "local_channel_env.yaml",
    startup_scripts_path: str | Path | None = None,
    output_hardening_path: str | Path | None = None,
    output_dockerfile_path: str | Path | None = None,
):
    update_repo(repo_dir, dockerfile_version, local_env_path, startup_scripts_path, output_dockerfile_path, output_dockerfile_path)


main.add_command(update_repo)
main.add_command(download_packages)

if __name__ == "__main__":
    main()
