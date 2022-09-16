---
sidebar_label: Creating Dockerfile Templates
---

# Creating Dockerfile Templates

IB Manifest uses Jinja templating to make updating the Dockerfiles in the Iron
Bank (IB) repo as painless as possible. Each IB repo will need a Dockerfile
template located at `/config/Dockerfile.tpl`. This guide will explain how to
create the Dockerfile template for new projects.

## Dockerfile Templates in IB Manifest

For the most part, the Dockerfiles are fairly static with the exception of the
python packages that get copied into them. Every time there is a change to the
IB repo image, these packages get updated. The Dockerfile template allows you
to avoid copy and pasting these COPY blocks or doing large string
concatentations.

An example Dockerfile template is shown in the repository in the `/templates`
directory. One is also provided here for reference, but we recommend starting
with the Dockerfile you are trying to templatize.

<details><summary>Example Dockerfile Template</summary>
<p>

```
ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/metrostar/miniconda
ARG BASE_TAG=4.11.0

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}
WORKDIR /opt
ENV LOCAL_CONDA_CHANNEL="${WORKDIR}/local_channel"
USER root

RUN mkdir /home/${NB_USER} \
    && chown -R ${NB_USER}:${NB_USER} /home/${NB_USER}
RUN mkdir -p ${LOCAL_CONDA_CHANNEL} && chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

COPY --chown=${NB_USER}:${NB_USER} /config/channeldata.json ${LOCAL_CONDA_CHANNEL}/channeldata.json
COPY --chown=${NB_USER}:${NB_USER} /config/linux-64/repodata.json ${LOCAL_CONDA_CHANNEL}/linux-64/repodata.json
COPY --chown=${NB_USER}:${NB_USER} /config/noarch/repodata.json ${LOCAL_CONDA_CHANNEL}/noarch/repodata.json
RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}
RUN dnf update -y && dnf install -y bzip2 gcc


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

RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}
RUN chown -R ${NB_USER}:${NB_USER} /opt/
RUN chown -R ${NB_USER}:${NB_USER} /home/
USER ${NB_USER}
ENV PATH="${CONDA_PATH}/bin:$PATH"
WORKDIR /home/${NB_USER}
USER root

RUN dnf clean all && \
	dnf remove -y bzip2 gcc && \
	rm -rf info && \
	conda clean -yaf && \
	rm -rf /home/${NB_USER}/.conda && \
	rm -rf /opt/conda/pkgs/cache && \
	rm -rf /root/micromamba/pkgs/cache

RUN chown -R ${NB_USER}:${NB_USER} /opt/
RUN chown -R ${NB_USER}:${NB_USER} /home/
USER ${NB_USER}

HEALTHCHECK NONE
```

</p>
</details>

In order to create a Dockerfile, we really only need to account for 3 things:
* a list of noarch packages
* a list of linux packages
* a list of packages which start with an underscore

That last one is rather interesting. Because of the linting stage of the IB
Pipeline, packages that lead with an underscore are deemed a security threat.
To avoid conflicts, we remove the underscore temporarily and add it back on the
other side of the fence.

All you need to do is replace these 3 things with the jinja syntax for handling
those lists. Instead of many lines of `COPY` statments, you'll now have:

```
COPY [ \{%- for pkg in noarch_packages %}
"{{ pkg }}", \
{%- endfor %}
"${LOCAL_CONDA_CHANNEL}/noarch/", \
]
```

for the noarch, linux, and underscore packages.

## Using a template in the workflow

The high level `Update Repository` workflow will determine these package lists
for you and provide them to the template as a dictionary. You can either allow
the code to automatically pull the template from the IB repo by calling:

```python
update_repository(
    repo_dir='path_to_repo',
    dockerfile_version='dockerfile_version',
)
```

Or, you can specify the specific location of a template you'd like to usse.

```python
update_repository(
    repo_dir='path_to_repo',
    dockerfile_version='dockerfile_version',
    dockerfile_template_path='path/to/template.tpl,
)
```


## Building a Dockerfile

If you just want to build an individual Dockerfile from a template, you can
call:

```python
write_dockerfile(
    noarch_packages=["requests-2.28.1-pyhd8ed1ab_1.tar.bz2"],
    linux_packages=["python-3.10.6-h582c2e5_0_cpython.tar.bz2"],
    underscore_packages=["openmp_mutex-4.5-2_gnu.tar.bz2"],
    output_path='Dockerfile,
    dockerfile_template_path='path/to/template.tpl,
)
```
