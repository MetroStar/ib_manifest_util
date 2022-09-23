---
sidebar_position: 1
sidebar_label: Updating an Iron Bank Repo
---

# Updating an Iron Bank Repo

This guide will walk you through using `IB Manifest` to update an Iron Bank
Repository (IB Repo).

Common usecases for the `IB Manifest` are:
* Adding/Removing a package in `local_channel_env.yaml`
* Bringing all the packages in the IB Repo up-to-date

## Preparing your environment

If you haven't already, get your local environment set up by following the
[Installation guide](/getting-started/installation).

## Downloading the Iron Bank repo

You'll need to download a copy of the
[Iron Bank Repo](https://repo1.dso.mil/dsop) you wish to update. You could go
to the IB Repo and click the "Download" button to get a compressed copy of the
repo. However, we recommend using `git` to create a clone of the repo.

From your local terminal, clone the repo:

```bash
git clone https://repo1.dso.mil/dsop/opensource/<your_org>/<your_repo>.git
```

Take note of the location of the repo, this is now what we'll call the
variable `repo_dir`.

## Make changes to the IB Repo files

At this point, you should make the changes you'd like to see to your local
repo files. You may need to add or removed packages in `local_channel_env.yaml`
or you may simply be updating the current channel with the most up-to-date
packages.

## Update the repository files

Finally, we get to run `IB Manifest`!

There are a couple of options for running
`IB Manifest`. You can choose to run it from Python or from the CLI.

### Running IB Manifest from Python

You can run the IB Manifest `update_repo` function from Python by writing a
small python script. First, let's look at the simplest possible call, then
we'll add in more details.


Create a new file `simple_example.py` with the following contents:

```python
from ib_manifest_util.update_repository import update_repo

repo_dir = 'path/to/repo_dir'
ib_repo_tag = '9999'

update_repo(
    repo_dir=repo_dir,
    dockerfile_version=ib_repo_tag,
)
```

Where `repo_dir` is the location of your downloaded copy of the IB Repo and
`ib_repo_tag` is the tag, or version number, of the Dockerfile and the hardening
manifest in your repo (you may want to increment this to signify a change).

Then from the command line (with your IB Manifest conda environment activated),
run:

```bash
python simple_example.py
```

An similar example script can be found in the IB Manifest repo.

<details>
<summary> Click here for an example that avoids overwriting IB repository files
</summary>

The following is an example script for running the `update_repo` function while
outputting to a new directory ("/example_output").

```python
from pathlib import Path

from ib_manifest_util.update_repository import update_repo

repo_dir = 'path/to/repo_dir'
output_dir = Path(".").joinpath("example_output")

update_repo(
    repo_dir=repo_dir,
    dockerfile_version="9999",
    local_env_path=repo_dir.joinpath("scripts", "local_channel_env.yaml"),
    output_hardening_path=output_dir.joinpath("output_hardening_manifest.yaml"),
    output_dockerfile_path=output_dir.joinpath("output_dockerfile"),
    dockerfile_template_path=None,
)
```
</details>

### Running IB Manifest from the command line

IB Manifest also includes a command line interface (CLI).
