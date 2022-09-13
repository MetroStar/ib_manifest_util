# ib_manifest_util: Open Source tool for updating Iron Bank Images

## Overview

Updating packages for a docker image in the Iron Bank Image Repository can be
time consuming since it requires that you rebuild multiple files and run
multiple separate processes. This tool captures all those tasks and provides
a single function that can be run to update all the necessary files.

The high level workflow:
1) User manually updates/adds a package into local_channel_env.yaml
2) run conda-vendor vendor using the local_channel_env.yaml to construct a local channel
3) copy both linux-64/repodata.json and noarch/repodata.json from the local channel to /config in the IB repo
4) run conda-vendor ironbank-gen using the local_channel_env.yaml to create ib_manifest.yaml
5) copy the ib_manifest.yaml contents into hardening_manifest.yaml
6) Create a new Dockerfile with updated COPY statements for new package(s)

Once those steps are done, users manually commit linux-64/repodata.json,
noarch/repodata.json, hardening_manifest.yaml and Dockerfile to git, which
then kicks off an Iron Bank pipeline

## Running ib_manifest_util

Once you've completed the installation instructions below, downloaded the IB
repo, and made changes to the `local_channel_env.yaml` in the repo, you can run
ib_manifest_util by running from within python:

```python
update_repository(
    repo_dir='path_to_repo',
    dockerfile_version='dockerfile_version',
)
```

From there, all the files you need to update in the repo will be generated

(`repodata.json`(s), `Dockerfile`, and `hardening_manifest.yaml`).

### Additional usage options

```python
def update_repo(
    repo_dir: str | Path,
    dockerfile_version: str,
    local_env_path: str | Path = "local_channel_env.yaml",
    startup_scripts_path: str | Path | None = None,
    output_hardening_path: str | Path | None = None,
    output_dockerfile_path: str | Path | None = None,
    dockerfile_template_path: str | Path = None,
):
    """High level function to update an Iron Bank repository with a new environment.

    The workflow:
    1) User manually updates/adds a package into local_channel_env.yaml
    2) run conda-vendor vendor using the local_channel_env.yaml to construct a local channel
    3) copy both linux-64/repodata.json and noarch/repodata.json from the local channel to /config in the IB repo
    4) run conda-vendor ironbank-gen using the local_channel_env.yaml to create ib_manifest.yaml
    5) copy the ib_manifest.yaml contents into hardening_manifest.yaml
    6) Create a new Dockerfile with updated COPY statements for new package(s)

    Once those steps are done, users manually commit linux-64/repodata.json,
    noarch/repodata.json, hardening_manifest.yaml and Dockerfile to git, which
    then kicks off an Iron Bank pipeline

    Args:
        repo_dir: Full path to local copy of Iron Bank manifest repository.
        dockerfile_version: dockerfile version to add to hardening manifest.
        local_env_path: Optional. Full path to updated version of
            `local_channel_env.yaml`.Default: 'local_channel_env.yaml'
        startup_scripts_path: Optional. Full path to yaml file with additional startup scripts.
        output_hardening_path: output path for the new `hardening_manifest.yaml`. Use `None` to
            overwrite the version in the repo
        output_dockerfile_path: output path for the new `Dockerfile`. Use `None` to
            overwrite the version in the repo
```

## Installation instructions

`ib_manifest_util` is run inside of a conda environment. From the package direcory, create
the conda environment:
```bash
conda env create -f environment.yml
```
Activate the environment:
```bash
conda activate ib_manifest_env
```
Install the ib_manifest_env package into this environment:
```bash
pip install -e .
```

### Installing a specific release

To install a specific release of this repo, clone the repo and then checkout
the tag of your choice. For example, to get version 0.0.5:

```bash
git checkout 0.0.5
```

This will put your git repo in a detached state since you haven't created a
new, editable branch at this location in the history. If you plan to make
edits which will eventually become a PR, you should branch off of the live
`dev` branch.


## Developer instructions

Follow the installation instructions above. You'll need to add the pre-commit
hooks which help keep the codebase consistent across developers. All pre-commit
hooks are run as part of CI.

From the package directory, with your conda env activated:

```bash
pre-commit install
```

This will run the pre-commit hooks every time you commit changes. You can
also run pre-commit on all files:

```bash
pre-commit run --all
```

### Running the test suite

The GitHub Actions CI runs the test suite (as well as the pre-commit hooks) once a
PR is opened.

```bash
pytest tests -vvv
```

Some tests require external internet access to run. These tests are marked with
`web`. To run only the tests available in an air-gapped system, ue:

```bash
pytest tests -vvv -m "not web"
```
