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

#RUN groupadd -r ${NB_USER} \
#RUN useradd -l -r -g ${NB_GID} -u ${NB_UID} ${NB_USER} \
RUN mkdir /home/${NB_USER} \
    && chown -R ${NB_USER}:${NB_USER} /home/${NB_USER}

ENV LOCAL_CONDA_CHANNEL="/home/${NB_USER}/local-channel"

#create directory for our local conda channel
RUN mkdir -p ${LOCAL_CONDA_CHANNEL} && chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

#copy over local-channel metadata configuration files
COPY --chown=${NB_USER}:${NB_USER} /config/linux-64/repodata.json ${LOCAL_CONDA_CHANNEL}/linux-64/repodata.json
COPY --chown=${NB_USER}:${NB_USER} /config/noarch/repodata.json ${LOCAL_CONDA_CHANNEL}/noarch/repodata.json
RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

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

COPY --chown=${NB_USER}:${NB_USER} scripts/local_channel_env.yaml ${LOCAL_CONDA_CHANNEL}/

USER ${NB_USER}

ENV PATH="${CONDA_PATH}/bin:$PATH"

WORKDIR /home/${NB_USER}

USER root
#remove cve findings and cleanup
RUN dnf clean all && \
    dnf remove -y bzip2 gcc && \
    rm -rf info && \
    conda clean -yaf && \
    rm -rf /var/cache/dnf && \
    rm -rf /opt/conda/singleuser/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /opt/conda/envs/singleuser/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /root/micromamba/pkgs/tornado-6.1-py39h3811e60_1/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/path-parse/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/@npmcli/arborist/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/tar/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/@npmcli/git/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/string-width/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/cli-table3/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/tar/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/path-parse/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/string-width/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/yargs/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/cliui/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/json-schema/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/wrap-ansi/node_modules/ansi-regex/package.json && \
    rm -rf /root/micromamba/pkgs/cache && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/wrap-ansi/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/string-width/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/yargs/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/json-schema/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/path-parse/package.json && \
    rm -rf /opt/conda/envs/singleuser/lib/node_modules/npm/node_modules/json-schema/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/node_modules/npm/node_modules/cliui/node_modules/ansi-regex/package.json && \
    rm -rf /opt/conda/envs/tip-singleuser/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /info && \
    rm -rf /home/${NB_USER}/.conda


USER ${NB_USER}

EXPOSE 8888

#ENV PATH="${CONDA_PATH}/envs/singleuser/bin:$PATH"

# Configure container startup
ENTRYPOINT ["tini", "--", "/usr/bin/bash"]

HEALTHCHECK NONE