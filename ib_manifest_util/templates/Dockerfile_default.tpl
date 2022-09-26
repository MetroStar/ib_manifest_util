ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=opensource/metrostar/miniconda
ARG BASE_TAG=4.12.0

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

{%- if copy_notebook_config is true %}
COPY --chown=${NB_USER}:${NB_USER} config/jupyter_notebook_config.py /home/${NB_USER}/.jupyter/
{%- endif %}

# make additional directories
{%- for dir in mkdirs %}
RUN mkdir "{{ dir }}"
{%- endfor %}

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
