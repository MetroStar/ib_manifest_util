from pathlib import Path

import click

from ib_manifest_util import __version__
from ib_manifest_util.download_conda_packages import download_packages
from ib_manifest_util.update_repository import update_repo


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
@click.option(
    "--local_env_path",
    default="local_channel_env.yaml",
    help="Path to local environment file",
)
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
    local_env_path: str | Path = None,
    startup_scripts_path: str | Path | None = None,
    output_hardening_path: str | Path | None = None,
    output_dockerfile_path: str | Path | None = None,
):
    update_repo(
        repo_dir,
        dockerfile_version,
        local_env_path,
        startup_scripts_path,
        output_hardening_path,
        output_dockerfile_path,
    )


@click.command(
    "download_packages",
    help="Download necessary Python packages given an Iron Bank hardening_manifest.yaml",
)
@click.option(
    "--manifest_path",
    help="Path to the hardening manifest from which to download packages",
)
@click.option(
    "--urls",
    help="List of URLs to download",
    multiple=True,
)
@click.option(
    "--download_path",
    default=Path.cwd(),
    help="Path to where the packages should be downloaded",
)
def download_packages_cli(
    manifest_path: str | Path = None,
    urls: list = None,
    download_path: str | Path = None,
):
    download_packages(manifest_path, urls, download_path)


main.add_command(update_repo_cli)
main.add_command(download_packages_cli)

if __name__ == "__main__":
    main()
