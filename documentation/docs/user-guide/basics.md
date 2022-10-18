---
sidebar_position: 1
sidebar_label: IB Manifest Basics
---


# Running ib_manifest_util

Once you've completed the [installation instructions](../getting-started/installation), downloaded the
[Iron Bank Container repo](https://repo1.dso.mil/dsop), and made changes to the
`local_channel_env.yaml` in the repo, you can run `ib_manifest_util` by running:

```python
update_repository(
    repo_dir='path_to_repo',
    dockerfile_version='dockerfile_version',
)
```

From there, all the files you need to update in the repo will be generated:
`repodata.json`(s), `Dockerfile`, and `hardening_manifest.yaml`.

### API documentation

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

<!-- Links -->
[install]: ./getting-started/installation
