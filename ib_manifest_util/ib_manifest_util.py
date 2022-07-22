import subprocess
import sys
import platform
import requests
from ruamel.yaml import YAML
from ruamel import yaml
import click
from pathlib import Path

from ib_manifest_util.version import __version__

def run_subprocess(command):
    process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
    for c in iter(lambda: process.stdout.read(1), b""):
        sys.stdout.write(c.decode("utf-8"))


def create_ib_manifest(file):
    yaml = YAML(typ="safe")
    yaml.default_flow_style = False

    with open(file, "r") as f:
        env = yaml.load(f)
    env["channels"] = ["conda-forge"]
    with open(file, "w") as f:
        yaml.dump(env, f)

    run_subprocess("conda-vendor ironbank-gen --file local_channel_env.yaml -p linux-64")


def generate_copy_statements(hardening_path="../hardening_manifest.yaml", startup_scripts_config="../start_scripts.yaml"):
    yaml = YAML(typ="safe")
    conda_vendor_manifest = yaml.load(open(hardening_path).read())

    noarch_pkgs = []
    linux_64_pkgs = []
    underscore_copy = ""

    for x in conda_vendor_manifest["resources"]:
        pkg = x["url"].split("/")[-1]

        if "noarch" in x["url"] and pkg[0] != "_":
            noarch_pkgs.append(pkg)

        if "linux-64" in x["url"] and pkg[0] != "_":
            linux_64_pkgs.append(pkg)

        if "noarch" in x["url"] and pkg[0] == "_":
            underscore_copy += f"COPY [\"{pkg.lstrip('_')}\", \"${{LOCAL_CONDA_CHANNEL}}/noarch/{pkg}\"]\n"

        if "linux-64" in x["url"] and pkg[0] == "_":
            underscore_copy += f"COPY [\"{pkg.lstrip('_')}\", \"${{LOCAL_CONDA_CHANNEL}}/linux-64/{pkg}\"]\n"

    noarch_copy = ""
    linux_64_copy = ""

    if len(noarch_pkgs) != 0:
        noarch_copy = "".join(
            ["COPY ["]
            + [f'"{x}", \\\n' for x in noarch_pkgs]
            + ['"${LOCAL_CONDA_CHANNEL}/noarch/"]']
        )

    if len(linux_64_pkgs) != 0:
        linux_64_copy = "".join(
            ["COPY ["]
            + [f'"{x}", \\\n' for x in linux_64_pkgs]
            + ['"${LOCAL_CONDA_CHANNEL}/linux-64/"]']
        )
    startup_text = "COPY ["

    with open(startup_scripts_config, "r") as f:
        startup_names = [_["filename"] for _ in yaml.load(f)["resources"]]

    for name in startup_names:
        startup_text += f'"{name}", \ \n'

    startup_text += '"/home/${NB_USER}/"]'

    copy_text = (
        noarch_copy
        + "\n"
        + linux_64_copy
        + "\n"
        + underscore_copy
        + "\n"
        + startup_text
        + "\n"
    )
    return copy_text


def test_existence_copy_markers(dockerfile_path="../Dockerfile"):
    with open(dockerfile_path, "r") as f:
        docker_buffer = f.read()

    start_marker = "#Start_of_copy_DONT_DELETE"
    end_marker = "#End_of_copy_DONT_DELETE"

    if start_marker not in docker_buffer or end_marker not in docker_buffer:
        print(
            """The comment \"#Start_of_copy_DONT_DELETE\" must exist before the block of copy statements, and the comment \"#End_of_copy_DONT_DELETE\" must exist after it for this script to function. Exiting."""
        )
        sys.exit()


def insert_copy_statements(copy_text, dockerfile_path="../Dockerfile"):

    with open(dockerfile_path, "r") as f:
        docker_buffer = f.read()

    start_marker = "#Start_of_copy_DONT_DELETE"
    end_marker = "#End_of_copy_DONT_DELETE"

    new_dockerfile = (
        docker_buffer.split(start_marker)[0]
        + f"\n{start_marker}\n"
        + copy_text
        + f"\n{end_marker}\n"
        + docker_buffer.split(end_marker)[1]
    )

    with open(dockerfile_path, "w") as f:
        docker_buffer = f.write(new_dockerfile)


def update_hardening_manifest(dockerfile_version, startup_scripts_path, hardening_manifest_path="../hardening_manifest.yaml"):
    run_subprocess("conda-vendor vendor --file local_channel_env.yaml -p linux-64")

    with open("local_channel_env.yaml", "r") as f:
        env = yaml.safe_load(f)
    channel_name = env["name"]

    noarch_raw = "{}/noarch/repodata.json".format(channel_name)
    linux_raw = "{}/linux-64/repodata.json".format(channel_name)

    noarch_path = Path(noarch_raw)
    linux_path = Path(linux_raw)

    noarch_target = Path('../config/noarch/repodata.json')
    linux_target = Path('../config/linux-64/repodata.json')

    noarch_path.rename(noarch_target)
    linux_path.rename(linux_target)

    with open("../hardening_manifest.yaml", "r") as f:
        hardening_manifest = yaml.safe_load(f)

    with open("ib_manifest.yaml", "r") as f:
        ib_manifest = yaml.safe_load(f)

    if startup_scripts_path != None:
        with open(startup_scripts_path, "r") as f:
            startup_scripts = yaml.safe_load(f)
        hardening_manifest["resources"] = ib_manifest["resources"]
        hardening_manifest["resources"] = startup_scripts["resources"] + ib_manifest["resources"]
    else:
        hardening_manifest["resources"] = ib_manifest["resources"]

    hardening_manifest["tags"] = [dockerfile_version]

    class Dumper(yaml.RoundTripDumper):
        def increase_indent(self, *args, **kwargs):
            return super().increase_indent(indentless=False)

    with open("/tmp/ib_temp.yaml", "w") as f:
        yaml.dump(hardening_manifest, f, Dumper=Dumper)

    with open("/tmp/ib_temp.yaml", "r") as f:
        string = f.read()

    with open("../hardening_manifest.yaml", "w") as f:
        dashes = "---\n"
        dashes += string
        f.write(dashes)

    remove_channel = "rm -rf {}/".format(channel_name)
    run_subprocess(remove_channel)
    run_subprocess("rm ib_manifest.yaml")

    with open("local_channel_env.yaml", "r") as f:
        env = yaml.safe_load(f)
    env["channels"] = ["./local-channel"]
    with open("local_channel_env.yaml", "w") as f:
        yaml.dump(env, f)


@click.command("download", help="Download necessary Python packages given an Iron Bank hardening_manifest.yaml")
@click.option("--file", default=None, help="Path to hardening manifest")

def download(file):
    manifest = yaml.safe_load(open(file).read())
    
    urls = [x['url'] for x in manifest['resources']]
    
    for i, url in enumerate(urls):
        fname = url.split('/')[-1].lstrip('_')
        print(f"Downloading {i+1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            with open(f"../{fname}", 'wb') as f:
                f.write(r.content)

@click.group()
@click.version_option(__version__)
def main() -> None:
    """To display help and usage for subcommands, use: ib_manifest_util [COMMAND] --help"""
    pass


@click.command("update_manifest", help="Update the local hardening manifest and Dockerfile with necessary packages given an environment file")
@click.option("--file", default=None, help="Path to environment file")
@click.option("--startup-scripts-path", default=None, help="Path to .yaml file containing additional files to copy")

@click.option("--dockerfile-version", prompt="Please enter the desired docker image version")

def update_manifest(file, dockerfile_version, startup_scripts_path):
    test_existence_copy_markers()
    create_ib_manifest(file)
    update_hardening_manifest(dockerfile_version, startup_scripts_path)
    copy_text = generate_copy_statements()
    insert_copy_statements(copy_text)

main.add_command(update_manifest)
main.add_command(download)


if __name__ == "__main__":
    main()
