import click
import requests
from ib_manifest_util.update_repository import update_repo
from ib_manifest_util.download_conda_packages import download_packages
from ib_manifest_util.version import __version__

@click.group()
@click.version_option(__version__)
def main() -> None:
    """To display help and usage for subcommands, use: ib_manifest_util [COMMAND] --help"""
    pass

main.add_command(update_repo)
main.add_command(download_packages)

if __name__ == "__main__":
    main()
