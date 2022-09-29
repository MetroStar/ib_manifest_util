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

## Generate the updated repository files

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


To get started, ensure that you have the `ib_manifest_util` package installed. To verify, the following command from you terminal:

```bash
$ ib_manifest_util --version
ib_manifest_util, version 0.1.0
```

And for help:

```shell
$ ib_manifest_util --help

Usage: ib_manifest_util [OPTIONS] COMMAND [ARGS]...

  To display help and usage for subcommands, use: ib_manifest_util [COMMAND]
  --help

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  download_packages  Download necessary Python packages given an Iron...
  update_repo        Update the local hardening manifest and Dockerfile...
```

:::info
If these commands don't work for you, double-check you have the package installed. See the [installation instructions](../getting-started/installation.md) for details.
::::

As the help page outlines, there are currently two high-level commands, `download_packages` and `update_repo`. To make the same changes as [above](updating_repos.md#running-ib-manifest-from-python),
we will use the `update_repo` command. To get a better understanding of how to use it, run the `--help` command:

```shell
$ ib_manifest_util update_repo --help
Usage: ib_manifest_util update_repo [OPTIONS]

  Update the local hardening manifest and Dockerfile with necessary packages
  given an environment file

Options:
  --repo_dir TEXT
  --dockerfile_version TEXT
  --local_env_path TEXT          Path to local environment file
  --startup_scripts_path TEXT    (Optional) Path to .yaml file containing
                                 additional files to copy
  --output_hardening_path TEXT   (Optional) Path to location in which the
                                 hardening manifest will be placed
  --output_dockerfile_path TEXT  (Optional) Path to location in which the
                                 Dockerfile will be placed
  --help                         Show this message and exit.
```


Okay, so assuming the Iron Bank repository has been cloned locally, then we can running the following command.
This will update the two `repodata.json` files, the `Dockerfile` and `hardening_manifest.yaml`.


```shell
ib_manifest_util update_repo --repo_dir ~/path/to/ib-repo --dockerfile_version 9999
```

As stated, this command will accomplish the same thing as the running `update_repo` as a Python module.


## Push the updated files to the Iron Bank repository

Now that you've updated all of the required files, you'll need to manually
commit these files back to the Iron Bank repo.

Once that's complete, you're done :tada:
