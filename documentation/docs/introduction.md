---
sidebar_position: 1
sidebar_label: Introduction
---

# Iron Bank Manifest Utility (IB Manifest)

## An Open Source tool for updating Iron Bank Images

## Overview

Updating packages for a Docker Image in the [Iron Bank Image Repository][ib-repo] can be
time consuming since it requires that you rebuild multiple files and run
multiple separate processes. `IB Manifest` captures all those tasks and provides
a single function that can be run to update all the necessary files.

What's happening behind the scenes:
1. User manually updates/adds a package into `local_channel_env.yaml`
2. Run conda-vendor vendor using the `local_channel_env.yaml` to construct a local channel
3. Copy both `linux-64/repodata.json` and `noarch/repodata.json` from the local channel to /config in the IB repo
4. Run `conda-vendor ironbank-gen` using the `local_channel_env.yaml` to create `ib_manifest.yaml`
5. Copy the `ib_manifest.yaml` contents into `hardening_manifest.yaml`
6. Create a new `Dockerfile` with the new package(s)

Once those steps are done, users manually commit `linux-64/repodata.json`,
`noarch/repodata.json`, `hardening_manifest.yaml` and `Dockerfile` to git, which
then kicks off an Iron Bank pipeline.

### Next Steps
From here, you may be interested in reviewing the [Getting Started]("getting-started/installation")
section, or if you've already installed IB Manifest, you can check out the docs on the
[Basics](user-guide/basics).

<!-- Links -->
[ib-repo]: https://repo1.dso.mil/dsop
