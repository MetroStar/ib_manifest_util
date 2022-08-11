import click
import requests

from ib_manifest_util.version import __version__


@click.command(
    "download",
    help="Download necessary Python packages given an Iron Bank hardening_manifest.yaml",
)
@click.option("--file", default=None, help="Path to hardening manifest")
def download(file):
    # TODO replace this with ib_manifest_util.util.download_file
    manifest = yaml.load(open(file).read())

    urls = [x["url"] for x in manifest["resources"]]

    for i, url in enumerate(urls):
        fname = url.split("/")[-1].lstrip("_")
        print(f"Downloading {i + 1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            with open(f"../{fname}", "wb") as f:
                f.write(r.content)


@click.group()
@click.version_option(__version__)
def main() -> None:
    """To display help and usage for subcommands, use: ib_manifest_util [COMMAND] --help"""
    pass


@click.command(
    "update_manifest",
    help="Update the local hardening manifest and Dockerfile with necessary packages given an environment file",
)
@click.option("--file", default=None, help="Path to environment file")
@click.option(
    "--startup-scripts-path",
    default=None,
    help="Path to .yaml file containing additional files to copy",
)
@click.option(
    "--dockerfile-version", prompt="Please enter the desired docker image version"
)
def update_manifest(file, dockerfile_version, startup_scripts_path):
    # test_existence_copy_markers()
    create_ib_manifest(file)
    update_hardening_manifest(dockerfile_version, startup_scripts_path)
    copy_text = generate_copy_statements(
        hardening_path=hardening_manifest_path,
        startup_config_path=startup_scripts_config_path,
    )
    # insert_copy_statements(copy_text)


main.add_command(update_manifest)
main.add_command(download)

if __name__ == "__main__":
    main()
