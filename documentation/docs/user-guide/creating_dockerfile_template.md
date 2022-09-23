---
sidebar_label: Creating a Dockerfile Template
title: Creating a Dockerfile Template
description: How to build a Dockerfile Template for your repo
---

# Creating a Dockerfile Template

The IB Manifest package uses
[Jinja templating](https://jinja.palletsprojects.com/) for efficiently creating
the `Dockerfile`.

The `Dockerfile` is closely tied to the individual IB Repo; therefore, each IB
Repo will need it's own `Dockerfile` template. This guide will walk you through
creating this template.

:::note
The hardening manifest is also built with a Jinja template, but since it's the
same for all repos, it is located inside the repo. You won't need to
modify it.
:::

## Understanding Jinja templating

Jinja templates are wonderful tools that not only allow us to write a template
with placeholders, but we can also performs some simple code within template.
This allows us to pass in things like lists in order to generate multiple
items without having to explicitely write them all out or know exactly how many
items we have.

First, we'll create a templatized version of our Dockerfile.
Then we'll explain how each of these get populated.
Finally, we'll test it out.

## Make a copy of the final Dockerfile

The best approach to creating the Jinja template is to start with what will
be your final output Dockerfile. This is the Dockerfile that is currently
operational in your IB Repo.

As an example, we provide a sample one here (this has been pared down a bit so
dont expect it to work):

<details>
<summary> Click here for Sample Dockerfile
</summary>

```dockerfile
ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/metrostar/miniconda
ARG BASE_TAG=4.12.0

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

SHELL ["/usr/bin/bash", "-c"]

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

ENV CONDA_PATH="/opt/conda" \
    NB_USER="${NB_USER}" \
    NB_UID="${NB_UID}" \
    NB_GID="${NB_GID}"

USER root
RUN yum install mesa-libGL -y && yum clean all

RUN mkdir /home/${NB_USER} \
    && chown -R ${NB_USER}:${NB_USER} /home/${NB_USER}

ENV LOCAL_CONDA_CHANNEL="/home/${NB_USER}/local-channel"

#create directory for our local conda channel
RUN mkdir -p ${LOCAL_CONDA_CHANNEL} && chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

#copy over local-channel metadata configuration files
COPY --chown=${NB_USER}:${NB_USER} /config/linux-64/repodata.json ${LOCAL_CONDA_CHANNEL}/linux-64/repodata.json
COPY --chown=${NB_USER}:${NB_USER} /config/noarch/repodata.json ${LOCAL_CONDA_CHANNEL}/noarch/repodata.json
RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}


COPY ["fonts-conda-ecosystem-1-0.tar.bz2", \
"geopandas-base-0.11.1-pyha770c72_0.tar.bz2", \
"cloudpickle-2.1.0-pyhd8ed1ab_0.tar.bz2", \
"${LOCAL_CONDA_CHANNEL}/noarch/"]
COPY ["libnetcdf-4.8.1-nompi_h21705cb_104.tar.bz2", \
"tornado-6.1-py39hb9d737c_3.tar.bz2", \
"curl-7.83.1-h7bff187_0.tar.bz2", \
"${LOCAL_CONDA_CHANNEL}/linux-64/"]
COPY ["openmp_mutex-4.5-2_gnu.tar.bz2", "${LOCAL_CONDA_CHANNEL}/linux-64/_openmp_mutex-4.5-2_gnu.tar.bz2"]
COPY ["libgcc_mutex-0.1-conda_forge.tar.bz2", "${LOCAL_CONDA_CHANNEL}/linux-64/_libgcc_mutex-0.1-conda_forge.tar.bz2"]

# additional scripts that get added
COPY ["code_server.tar.gz", \
"start.sh", \
"start-notebook.sh", \
"start-singleuser.sh", \
"/home/${NB_USER}/"]

RUN mv "/home/${NB_USER}/code_server.tar.gz" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start.sh" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start-notebook.sh" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start-singleuser.sh" /usr/local/bin/ \
    && chmod +x /usr/local/bin/start.sh \
    && chmod +x /usr/local/bin/start-notebook.sh \
    && chmod +x /usr/local/bin/start-singleuser.sh

RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}
ENV PATH="${CONDA_PATH}/bin:$PATH"
WORKDIR /home/${NB_USER}
USER root

#remove cve findings and cleanup
RUN dnf clean all && \
    dnf remove -y bzip2 gcc && \
    rm -rf info && \
    conda clean -yaf && \
    rm -rf /root/micromamba/pkgs/tornado-6.1-py39h3811e60_1/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /info && \
    rm -rf /home/${NB_USER}/.conda

USER ${NB_USER}

# Configure container startup
ENTRYPOINT ["tini", "--", "/usr/bin/bash",".init/start.sh"]
```
</details>

As you can see, we have a lot going on in this Dockerfile. However, we only
need to make changes to the package list. When we run IB Manifest, it will
generate an updated list of packages. These will be fed into our Jinja template
in order to update the Dockerfile.

## Templatizing the Dockerfile

Now we'll replace the sections of the Dockefile which contain the packages with
Jinja template code.

IB Manifest will generate a dictionary of variables. The Jinja template engine
will consume this dictionary and use it to construct our Dockerfile.

You can immediately replace the COPY sections with packages with the template
commands, but we recommend the following approach which lends itself well to
testing.

Below is the structure of the dictionary that our Jinja template is going
to expect. You can see we have separate items for `noarch_packages`,
`linux_packages`, and `underscore_packages` (these need special handling to
pass Iron Bank security screening). Let's begin by copying the package lists
from your Dockerfile into this dictionary. Note that the final item in the
COPY list is the location to which they will be copied. We won't need that here.

```python
content = {
    "noarch_packages": [
        "fonts-conda-ecosystem-1-0.tar.bz2",
        "geopandas-base-0.11.1-pyha770c72_0.tar.bz2",
        "cloudpickle-2.1.0-pyhd8ed1ab_0.tar.bz2"
        ],
    "linux_packages": [
        "libnetcdf-4.8.1-nompi_h21705cb_104.tar.bz2",
        "tornado-6.1-py39hb9d737c_3.tar.bz2",
        "curl-7.83.1-h7bff187_0.tar.bz2"
        ],
    "underscore_packages": [
        "openmp_mutex-4.5-2_gnu.tar.bz2",
        "libgcc_mutex-0.1-conda_forge.tar.bz2"
        ],
}
```

Now that we have those copied over, we are ready to copy in our Jinja commands.
Replace the COPY statements for those sections with:

```dockerfile
# noarch packages
COPY [ \{%- for pkg in noarch_packages %}
"{{ pkg }}", \
{%- endfor %}
"${LOCAL_CONDA_CHANNEL}/noarch/", \
]

# linux packages
COPY [ \{%- for pkg in linux_packages %}
"{{ pkg }}", \
{%- endfor %}
"${LOCAL_CONDA_CHANNEL}/linux-64/", \
]

# special handling for packages with underscores
{%- for pkg in underscore_packages %}
COPY ["{{ pkg }}", "${LOCAL_CONDA_CHANNEL}/linux-64/_{{ pkg }}"]
{%- endfor %}
```

We suggest saving this file in your IB Repo as `/config/Dockerfile.tpl`.

The Jinja template engine will accept the variable lists from our `content`
dictionary and unpack them for us!

## Using the template to create a Dockerfile

At this point, you are ready to run `update_repo`. However, a little
testing would be prudent.

There is an example script in the package that can be modified.

We can use the low-level function `write_templatized_file` to test out if our
changes above worked as expected. Below is a sample script that you can use
for testing (adapted from
`ib_manifest_util/examples/create_dockerfile_template.py`).

```python
from ib_manifest_util.util import write_templatized_file

template_filename = 'Dockerfile.tpl'
template_dir = 'template/directory/'

output_path = 'output_Dockerfile'

content = {
    "noarch_packages": [
        "fonts-conda-ecosystem-1-0.tar.bz2",
        "geopandas-base-0.11.1-pyha770c72_0.tar.bz2",
        "cloudpickle-2.1.0-pyhd8ed1ab_0.tar.bz2"
        ],
    "linux_packages": [
        "libnetcdf-4.8.1-nompi_h21705cb_104.tar.bz2",
        "tornado-6.1-py39hb9d737c_3.tar.bz2",
        "curl-7.83.1-h7bff187_0.tar.bz2"
        ],
    "underscore_packages": [
        "openmp_mutex-4.5-2_gnu.tar.bz2",
        "libgcc_mutex-0.1-conda_forge.tar.bz2"
        ],
}

write_templatized_file(
    template_filename=template_filename,
    output_path=output_path,
    content=content,
    template_dir=template_dir,
)
```

Confirm that the output Dockerfile looks as expected and you've done it! Now
all that's left is to push the Dockerfile template up to the IB Repo! :sparkles:
