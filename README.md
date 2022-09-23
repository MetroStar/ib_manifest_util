# IB Manifest Util:
# an Open Source tool for updating Iron Bank Images

https://metrostar.github.io/ib_manifest_util/

## Overview

Updating packages for a docker image in the Iron Bank Image Repository can be
time consuming since it requires that you rebuild multiple files and run
multiple separate processes. This tool captures all those tasks and provides
a single function that can be run to update all the necessary files.

```python
update_repository(
    repo_dir='path_to_repo',
    dockerfile_version='dockerfile_version',
)
```

The high level workflow:
1) Download your [Iron Bank repo](https://repo1.dso.mil/dsop)
2) Manually updates/add a package into `local_channel_env.yaml`
3) Run IB Manifest using the command above
4) Manually commit `linux-64/repodata.json`,
`noarch/repodata.json`, `hardening_manifest.yaml` and `Dockerfile` to git, which
then kicks off an automated Iron Bank pipeline


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

### Making a release

IB Manifest uses a dev/main git workflow. All development work happens on `dev`,
then when we're ready to release, we merge `dev` into `main` and release from
`main`. Here are the basic steps:

1) Ensure version number on `dev` has been incremented in `_version.py`
2) PR from `dev` into `main`
3) If there are conflicts, you'll have to create a new branch for the fix and
the PR will then be from the new branch into main
4) Tag a release on Github using the version number in `_version.py`
