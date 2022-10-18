ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/metrostar/miniconda
ARG BASE_TAG=4.11.0

FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${BASE_TAG}

SHELL ["/usr/bin/bash", "-c"]

ENV LOCAL_CONDA_CHANNEL="/home/${NB_USER}/local-channel"

USER root

#create directory for our local conda channel
RUN mkdir -p ${LOCAL_CONDA_CHANNEL} && chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

RUN dnf update -y && dnf install -y bzip2 gcc

#copy over local-channel metadata configuration files
COPY --chown=${NB_USER}:${NB_USER} /config/channeldata.json ${LOCAL_CONDA_CHANNEL}/channeldata.json
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

USER ${NB_USER}

ENV PATH="${CONDA_PATH}/bin:$PATH"

WORKDIR /home/${NB_USER}

RUN conda install \
    aiohttp \
    dask \
    distributed \
    numpy \
    pandas \
    tini \
    pyarrow \
    fastparquet \
    s3fs \
    scikit-learn \
    dask-ml \
    pyyaml \
    python-blosc \
    cytoolz \
    -c ${LOCAL_CONDA_CHANNEL} --override-channels --offline -y && \
    conda clean -yaf


#copy over dask-gateway app pulled from github
USER root
COPY "dask-gateway-0.9.0.tar.gz" "dask-gateway-0.9.0.tar.gz"
RUN tar -xvf dask-gateway-0.9.0.tar.gz
RUN chown -R ${NB_USER}:${NB_USER} dask-gateway-0.9.0

USER ${NB_USER}

# Install dask-gateway into the dask-gateway conda environment
RUN cd dask-gateway-0.9.0/dask-gateway && \
    pip install . --no-cache-dir --no-deps

USER root
#remove cve findings and cleanup
RUN dnf clean all && \
    dnf remove -y bzip2 gcc && \
    rm -rf info && \
    conda clean -yaf && \
    rm -rf /var/cache/dnf && \
    rm -rf ${LOCAL_CONDA_CHANNEL} && \
    rm -rf /opt/conda/dask-gateway/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /opt/conda/envs/dask-gateway/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /root/micromamba/pkgs/tornado-6.1-py39h3811e60_1/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf /opt/conda/envs/dask-gateway/lib/node_modules/npm/node_modules/path-parse/package.json && \
    rm -rf /opt/conda/lib/python3.9/site-packages/tornado/test/test.key && \
    rm -rf dask-gateway-0.9.0 && \
    rm -rf dask-gateway-0.9.0.tar.gz && \
    rm -rf /home/${NB_USER}/.conda

USER ${NB_USER}

ENV PATH="/opt/conda/envs/dask-gateway/bin:$PATH"

ENTRYPOINT ["tini", "-g", "--"]

HEALTHCHECK NONE