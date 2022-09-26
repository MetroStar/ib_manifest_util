---
sidebar_position: 1
sidebar_label: Installation
---

# Installation instructions

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
