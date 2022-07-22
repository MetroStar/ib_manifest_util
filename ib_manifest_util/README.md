# IronBank Image Update Process for Conda Packages

Goal: create a local conda package repository (conda channel) that can be moved to an airgapped network so we can install everything that an image needs from that channel, rather than an open internet channel.

A conda channel just needs a certain folder structure and a repodata.json file. If this exists locally, existing conda tools can do all the install / dependency resolution steps.

## Files that matter

- local_channel_env.yaml
  - defines a conda environment
  - has all desired python packages with versions
- ironbank_manifest.yaml
  - top: IB specific configuration such as image tag
  - lists all files that will be downloaded: url, filename, sha hash
  - in this case, specifies files to be downloaded to the local conda channel
- repodata.json (multiple locations - linux-64, noarch)
  - index for the conda channel, conda uses this to do specify available packages and their dependencies
  - mostly a dictionary of { package : package_metadata, dependencies, etc. }
- Dockerfile
  - used to create image with local conda channel inside of it

## The process

1. IB manifest tool creates the ironbank_manifest, repodata, and Dockerfile files from the local_channel_env file. User provides an image version.
2. Ironbank then downloads the files listed by the ironbank_manifest to a build environment for its CI/CD pipeline.
3. Ironbank builds the docker image from the dockerfile in the build environment using the files downloaded in step 2.
4. The image is scanned for CVEs
5. Dev resolves CVEs, opens Merge Request from `<arbitrary_branch>` to `dev`, and creates new issue from `Application Update` template
6. Dev follows steps and clicks checkboxes under `contributor`, ensuring the label`Hardening|Review` is applied upon completion
7. IronBank personnel review software update issue. Changes may be requested. Upon approval they will merge to `dev`, and then merge to `master`
8. The image is published to the ironbank image registry.
