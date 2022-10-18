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

RUN groupadd docker && usermod -aG docker jovyan

ENV LOCAL_CONDA_CHANNEL="/home/${NB_USER}/local-channel"

#create directory for our local conda channel
RUN mkdir -p ${LOCAL_CONDA_CHANNEL} && chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

#copy over local-channel metadata configuration files
COPY --chown=${NB_USER}:${NB_USER} /config/linux-64/repodata.json ${LOCAL_CONDA_CHANNEL}/linux-64/repodata.json
COPY --chown=${NB_USER}:${NB_USER} /config/noarch/repodata.json ${LOCAL_CONDA_CHANNEL}/noarch/repodata.json
COPY --chown=${NB_USER}:${NB_USER} /scripts/local_channel_env.yaml /home/${NB_USER}/local_channel_env.yaml
RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}


# noarch packages
COPY [ \{%- for pkg in noarch_packages %}
"{{ pkg }}", \
{%- endfor %}
"${LOCAL_CONDA_CHANNEL}/noarch/" \
]

# linux packages
COPY [ \{%- for pkg in linux_packages %}
"{{ pkg }}", \
{%- endfor %}
"${LOCAL_CONDA_CHANNEL}/linux-64/" \
]

# special handling for packages with underscores
{%- for pkg in underscore_packages %}
COPY ["{{ pkg }}", "${LOCAL_CONDA_CHANNEL}/linux-64/_{{ pkg }}"]
{%- endfor %}



RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

RUN chown -R ${NB_USER}:${NB_USER} /opt/
RUN chown -R ${NB_USER}:${NB_USER} /home/

COPY --chown=${NB_USER}:${NB_USER} scripts/start.sh /home/${NB_USER}/.init/

USER ${NB_USER}

RUN mkdir "/home/${NB_USER}/work"

ENV PATH="${CONDA_PATH}/bin:$PATH"

WORKDIR /home/${NB_USER}

RUN conda env create -f /home/${NB_USER}/local_channel_env.yaml --offline

USER root
#remove cve findings and cleanup
RUN dnf clean all && \
    dnf remove -y bzip2 gcc && \
    rm -rf info && \
    conda clean -yaf && \
    rm -rf /var/cache/dnf && \
    rm -rf ${LOCAL_CONDA_CHANNEL} && \
    rm -rf /opt/conda/envs/jupyterhub/lib/python3.9/site-packages/tornado/test/test.key  && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/path-parse/package.json && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/tar/package.json && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/string-width/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/yargs/node_modules/ansi-regex/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/json-schema/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/rc/package.json && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/editor/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/minimist/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/mkdirp/node_modules/minimist/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/opener/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/through/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/wrap-ansi/node_modules/ansi-regex/package.json && \
	rm -rf /opt/conda/envs/jupyterhub/lib/python3.10/site-packages/tornado/test/test.key && \
    rm -rf /opt/conda/envs/jupyterhub/lib/node_modules/npm/node_modules/cliui/node_modules/ansi-regex/package.json && \
    rm -rf /home/${NB_USER}/.conda

RUN chown -R ${NB_USER}:${NB_USER} /opt/
RUN chown -R ${NB_USER}:${NB_USER} /home/

USER ${NB_USER}

EXPOSE 8000

ENV PATH="${CONDA_PATH}/envs/jupyterhub/bin:$PATH"
# Configure container startup
WORKDIR "/home/${NB_USER}/"
ENTRYPOINT ["tini", "--", "/usr/bin/bash",".init/start.sh"]

HEALTHCHECK NONE