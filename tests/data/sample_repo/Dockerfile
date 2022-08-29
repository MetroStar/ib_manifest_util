ARG BASE_REGISTRY=registry1.dso.mil
ARG BASE_IMAGE=ironbank/opensource/metrostar/miniconda
ARG BASE_TAG=4.11.0

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


#Start_of_copy_DONT_DELETE
COPY ["typing-extensions-4.3.0-hd8ed1ab_0.tar.bz2", \
"backports-1.0-py_2.tar.bz2", \
"cachetools-5.0.0-pyhd8ed1ab_0.tar.bz2", \
"tzdata-2022a-h191b570_0.tar.bz2", \
"font-ttf-source-code-pro-2.038-h77eed37_0.tar.bz2", \
"pyparsing-3.0.9-pyhd8ed1ab_0.tar.bz2", \
"jupyter-server-proxy-3.2.1-pyhd8ed1ab_0.tar.bz2", \
"rshiny-server-cmd-0.0.2-py_0.tar.bz2", \
"munkres-1.1.4-pyh9f0ad1d_0.tar.bz2", \
"prompt-toolkit-3.0.30-pyha770c72_0.tar.bz2", \
"backports.functools_lru_cache-1.6.4-pyhd8ed1ab_0.tar.bz2", \
"python-fastjsonschema-2.15.3-pyhd8ed1ab_0.tar.bz2", \
"s3transfer-0.4.2-pyhd8ed1ab_0.tar.bz2", \
"intake-parquet-0.2.3-py_0.tar.bz2", \
"prometheus_client-0.14.1-pyhd8ed1ab_0.tar.bz2", \
"idna-3.3-pyhd8ed1ab_0.tar.bz2", \
"param-1.12.2-pyh6c4a22f_0.tar.bz2", \
"pamela-1.0.0-py_0.tar.bz2", \
"jupyter_server-1.18.1-pyhd8ed1ab_0.tar.bz2", \
"importlib_resources-5.8.0-pyhd8ed1ab_0.tar.bz2", \
"jsonschema-4.6.1-pyhd8ed1ab_0.tar.bz2", \
"datashader-0.13.0-pyh6c4a22f_0.tar.bz2", \
"jmespath-0.10.0-pyh9f0ad1d_0.tar.bz2", \
"holoviews-1.14.8-pyhd8ed1ab_0.tar.bz2", \
"colorcet-3.0.0-pyhd8ed1ab_0.tar.bz2", \
"xarray-2022.3.0-pyhd8ed1ab_0.tar.bz2", \
"matplotlib-inline-0.1.3-pyhd8ed1ab_0.tar.bz2", \
"wheel-0.37.1-pyhd8ed1ab_0.tar.bz2", \
"jhsingle-native-proxy-0.8.0-pyhd8ed1ab_0.tar.bz2", \
"oauthlib-3.2.0-pyhd8ed1ab_0.tar.bz2", \
"babel-2.10.3-pyhd8ed1ab_0.tar.bz2", \
"nest-asyncio-1.5.5-pyhd8ed1ab_0.tar.bz2", \
"threadpoolctl-3.1.0-pyh8a188c0_0.tar.bz2", \
"altair-4.2.0-pyhd8ed1ab_1.tar.bz2", \
"traitlets-5.3.0-pyhd8ed1ab_0.tar.bz2", \
"joblib-1.1.0-pyhd8ed1ab_0.tar.bz2", \
"python-json-logger-2.0.1-pyh9f0ad1d_0.tar.bz2", \
"nbclient-0.6.6-pyhd8ed1ab_0.tar.bz2", \
"python-dateutil-2.8.2-pyhd8ed1ab_0.tar.bz2", \
"aioitertools-0.10.0-pyhd8ed1ab_0.tar.bz2", \
"base58-2.1.1-pyhd8ed1ab_0.tar.bz2", \
"nbformat-5.4.0-pyhd8ed1ab_0.tar.bz2", \
"parquet-cpp-1.5.1-2.tar.bz2", \
"ptyprocess-0.7.0-pyhd3deb0d_0.tar.bz2", \
"toolz-0.11.2-pyhd8ed1ab_0.tar.bz2", \
"dask-core-2022.1.0-pyhd8ed1ab_0.tar.bz2", \
"colorama-0.4.5-pyhd8ed1ab_0.tar.bz2", \
"mako-1.2.1-pyhd8ed1ab_0.tar.bz2", \
"cdsdashboards-singleuser-0.6.0-hd8ed1ab_0.tar.bz2", \
"jupyterhub-2.1.1-hd8ed1ab_0.tar.bz2", \
"sortedcontainers-2.4.0-pyhd8ed1ab_0.tar.bz2", \
"pickleshare-0.7.5-py_1003.tar.bz2", \
"nbconvert-6.5.0-pyhd8ed1ab_0.tar.bz2", \
"pip-22.0.3-pyhd8ed1ab_0.tar.bz2", \
"font-ttf-inconsolata-3.000-h77eed37_0.tar.bz2", \
"typing_extensions-4.3.0-pyha770c72_0.tar.bz2", \
"jupyter_telemetry-0.1.0-pyhd8ed1ab_1.tar.bz2", \
"jupyterlab_pygments-0.2.2-pyhd8ed1ab_0.tar.bz2", \
"stack_data-0.3.0-pyhd8ed1ab_0.tar.bz2", \
"markdown-3.3.7-pyhd8ed1ab_0.tar.bz2", \
"geopandas-base-0.11.0-pyha770c72_0.tar.bz2", \
"cloudpickle-2.1.0-pyhd8ed1ab_0.tar.bz2", \
"async-timeout-4.0.2-pyhd8ed1ab_0.tar.bz2", \
"soupsieve-2.3.1-pyhd8ed1ab_0.tar.bz2", \
"tinycss2-1.1.1-pyhd8ed1ab_0.tar.bz2", \
"zict-2.2.0-pyhd8ed1ab_0.tar.bz2", \
"ipython_genutils-0.2.0-py_1.tar.bz2", \
"parso-0.8.3-pyhd8ed1ab_0.tar.bz2", \
"webencodings-0.5.1-py_1.tar.bz2", \
"pyviz_comms-2.2.0-pyhd8ed1ab_0.tar.bz2", \
"jupyter_client-7.3.4-pyhd8ed1ab_0.tar.bz2", \
"dask-2022.1.0-pyhd8ed1ab_0.tar.bz2", \
"nbconvert-pandoc-6.5.0-pyhd8ed1ab_0.tar.bz2", \
"gitdb-4.0.9-pyhd8ed1ab_0.tar.bz2", \
"pyopenssl-22.0.0-pyhd8ed1ab_0.tar.bz2", \
"wcwidth-0.2.5-pyh9f0ad1d_2.tar.bz2", \
"multipledispatch-0.6.0-py_0.tar.bz2", \
"tenacity-8.0.1-pyhd8ed1ab_0.tar.bz2", \
"smmap-3.0.5-pyh44b312d_0.tar.bz2", \
"plotlydash-tornado-cmd-0.0.6-pyhd8ed1ab_0.tar.bz2", \
"flit-core-3.7.1-pyhd8ed1ab_0.tar.bz2", \
"geoviews-1.9.5-pyhd8ed1ab_0.tar.bz2", \
"geoviews-core-1.9.5-pyha770c72_0.tar.bz2", \
"defusedxml-0.7.1-pyhd8ed1ab_0.tar.bz2", \
"ipywidgets-7.6.5-pyhd8ed1ab_0.tar.bz2", \
"aiosignal-1.2.0-pyhd8ed1ab_0.tar.bz2", \
"requests-2.28.1-pyhd8ed1ab_0.tar.bz2", \
"zipp-3.8.0-pyhd8ed1ab_0.tar.bz2", \
"certipy-0.1.3-py_0.tar.bz2", \
"json5-0.9.5-pyh9f0ad1d_0.tar.bz2", \
"alembic-1.8.0-pyhd8ed1ab_0.tar.bz2", \
"gitpython-3.1.27-pyhd8ed1ab_0.tar.bz2", \
"websocket-client-1.3.3-pyhd8ed1ab_0.tar.bz2", \
"entrypoints-0.4-pyhd8ed1ab_0.tar.bz2", \
"asttokens-2.0.5-pyhd8ed1ab_0.tar.bz2", \
"pyjwt-2.4.0-pyhd8ed1ab_0.tar.bz2", \
"pygments-2.12.0-pyhd8ed1ab_0.tar.bz2", \
"partd-1.2.0-pyhd8ed1ab_0.tar.bz2", \
"ipympl-0.8.8-pyhd8ed1ab_0.tar.bz2", \
"confuse-1.7.0-pyhd8ed1ab_0.tar.bz2", \
"iniconfig-1.1.1-pyh9f0ad1d_0.tar.bz2", \
"fonts-conda-ecosystem-1-0.tar.bz2", \
"plotly-5.6.0-pyhd8ed1ab_0.tar.bz2", \
"pytz-2022.1-pyhd8ed1ab_0.tar.bz2", \
"attrs-21.4.0-pyhd8ed1ab_0.tar.bz2", \
"pexpect-4.8.0-pyh9f0ad1d_2.tar.bz2", \
"pydeck-0.7.1-pyh6c4a22f_0.tar.bz2", \
"jinja2-3.1.2-pyhd8ed1ab_1.tar.bz2", \
"urllib3-1.26.9-pyhd8ed1ab_0.tar.bz2", \
"boto3-1.17.106-pyhd8ed1ab_0.tar.bz2", \
"pure_eval-0.2.2-pyhd8ed1ab_0.tar.bz2", \
"cdsdashboards-0.6.0-pyhd8ed1ab_0.tar.bz2", \
"streamlit-1.5.1-pyhd8ed1ab_1.tar.bz2", \
"pyct-core-0.4.6-py_0.tar.bz2", \
"python-tzdata-2022.1-pyhd8ed1ab_0.tar.bz2", \
"ipykernel-6.15.0-pyh210e3f2_0.tar.bz2", \
"appdirs-1.4.4-pyh9f0ad1d_0.tar.bz2", \
"toml-0.10.2-pyhd8ed1ab_0.tar.bz2", \
"tomli-2.0.1-pyhd8ed1ab_0.tar.bz2", \
"tblib-1.7.0-pyhd8ed1ab_0.tar.bz2", \
"pympler-0.9-pyh9f0ad1d_0.tar.bz2", \
"datashape-0.5.4-py_1.tar.bz2", \
"jupyterlab_server-2.15.0-pyhd8ed1ab_0.tar.bz2", \
"jupyterlab-3.3.0-pyhd8ed1ab_0.tar.bz2", \
"locket-1.0.0-pyhd8ed1ab_0.tar.bz2", \
"beautifulsoup4-4.11.1-pyha770c72_0.tar.bz2", \
"font-ttf-ubuntu-0.83-hab24e00_0.tar.bz2", \
"astor-0.8.1-pyh9f0ad1d_0.tar.bz2", \
"nbclassic-0.3.7-pyhd8ed1ab_0.tar.bz2", \
"fsspec-2021.11.0-pyhd8ed1ab_0.tar.bz2", \
"validators-0.18.2-pyhd3deb0d_0.tar.bz2", \
"tqdm-4.64.0-pyhd8ed1ab_0.tar.bz2", \
"bokeh-root-cmd-0.1.2-pyhd8ed1ab_0.tar.bz2", \
"botocore-1.20.106-pyhd8ed1ab_0.tar.bz2", \
"nbconvert-core-6.5.0-pyhd8ed1ab_0.tar.bz2", \
"notebook-6.4.3-pyha770c72_0.tar.bz2", \
"py-1.11.0-pyh6c4a22f_0.tar.bz2", \
"jupyterhub-base-2.1.1-pyhd8ed1ab_0.tar.bz2", \
"pandocfilters-1.5.0-pyhd8ed1ab_0.tar.bz2", \
"notebook-shim-0.1.0-pyhd8ed1ab_0.tar.bz2", \
"importlib_metadata-4.11.4-hd8ed1ab_0.tar.bz2", \
"font-ttf-dejavu-sans-mono-2.37-hab24e00_0.tar.bz2", \
"cycler-0.11.0-pyhd8ed1ab_0.tar.bz2", \
"decorator-5.1.1-pyhd8ed1ab_0.tar.bz2", \
"pyshp-2.3.0-pyhd8ed1ab_0.tar.bz2", \
"packaging-21.3-pyhd8ed1ab_0.tar.bz2", \
"aiobotocore-1.4.1-pyhd8ed1ab_0.tar.bz2", \
"simpervisor-0.4-pyhd8ed1ab_0.tar.bz2", \
"backcall-0.2.0-pyh9f0ad1d_0.tar.bz2", \
"intake-0.6.5-pyhd8ed1ab_0.tar.bz2", \
"send2trash-1.8.0-pyhd8ed1ab_0.tar.bz2", \
"bleach-5.0.1-pyhd8ed1ab_0.tar.bz2", \
"six-1.16.0-pyh6c4a22f_0.tar.bz2", \
"blinker-1.4-py_1.tar.bz2", \
"pycparser-2.21-pyhd8ed1ab_0.tar.bz2", \
"heapdict-1.0.1-py_0.tar.bz2", \
"charset-normalizer-2.1.0-pyhd8ed1ab_0.tar.bz2", \
"pynndescent-0.5.7-pyh6c4a22f_0.tar.bz2", \
"fonts-conda-forge-1-0.tar.bz2", \
"async_generator-1.10-py_0.tar.bz2", \
"panel-0.12.6-pyhd8ed1ab_0.tar.bz2", \
"argon2-cffi-21.3.0-pyhd8ed1ab_0.tar.bz2", \
"executing-0.8.3-pyhd8ed1ab_0.tar.bz2", \
"jupyterlab_widgets-1.1.1-pyhd8ed1ab_0.tar.bz2", \
"pyct-0.4.6-py_0.tar.bz2", \
"s3fs-2021.11.0-pyhd8ed1ab_0.tar.bz2", \
"${LOCAL_CONDA_CHANNEL}/noarch/"]
COPY ["libpng-1.6.37-h753d276_3.tar.bz2", \
"libclang-14.0.6-default_h2e3cab8_0.tar.bz2", \
"pcre2-10.37-h032f7d1_0.tar.bz2", \
"libbrotlidec-1.0.9-h166bdaf_7.tar.bz2", \
"libclang13-14.0.6-default_h3a83d3e_0.tar.bz2", \
"bzip2-1.0.8-h7f98852_4.tar.bz2", \
"cytoolz-0.11.2-py39hb9d737c_2.tar.bz2", \
"frozenlist-1.3.0-py39hb9d737c_1.tar.bz2", \
"libvorbis-1.3.7-h9c3ff4c_0.tar.bz2", \
"libfuse-2.9.9-ha1f6473_1.tar.bz2", \
"alsa-lib-1.2.6.1-h7f98852_0.tar.bz2", \
"re2-2022.04.01-h27087fc_0.tar.bz2", \
"pycurl-7.45.1-py39hd73adbb_2.tar.bz2", \
"mysql-common-8.0.29-haf5c9bc_1.tar.bz2", \
"msgpack-python-1.0.3-py39hf939315_1.tar.bz2", \
"sip-6.5.1-py39he80948d_2.tar.bz2", \
"c-ares-1.18.1-h7f98852_0.tar.bz2", \
"libdeflate-1.12-h166bdaf_0.tar.bz2", \
"cryptography-37.0.4-py39hd97740a_0.tar.bz2", \
"matplotlib-base-3.5.1-py39h2fa2bec_0.tar.bz2", \
"jpeg-9e-h166bdaf_2.tar.bz2", \
"pillow-9.2.0-py39hae2aec6_0.tar.bz2", \
"abseil-cpp-20211102.0-h27087fc_1.tar.bz2", \
"libedit-3.1.20191231-he28a2e2_2.tar.bz2", \
"libxcb-1.13-h7f98852_1004.tar.bz2", \
"brotli-bin-1.0.9-h166bdaf_7.tar.bz2", \
"hdf5-1.12.1-nompi_h2386368_104.tar.bz2", \
"hdf4-4.2.15-h10796ff_3.tar.bz2", \
"python-3.9.7-hb7a2778_3_cpython.tar.bz2", \
"pytz-deprecation-shim-0.1.0.post0-py39hf3d152e_2.tar.bz2", \
"widgetsnbextension-3.5.2-py39hf3d152e_1.tar.bz2", \
"pyzmq-23.2.0-py39headdf64_0.tar.bz2", \
"pyrsistent-0.18.1-py39hb9d737c_1.tar.bz2", \
"libpq-14.4-hd77ab85_0.tar.bz2", \
"libuv-1.43.0-h7f98852_0.tar.bz2", \
"tzlocal-4.2-py39hf3d152e_1.tar.bz2", \
"tini-0.18.0-h14c3975_1001.tar.bz2", \
"ruamel.yaml.clib-0.2.6-py39hb9d737c_1.tar.bz2", \
"libnl-3.7.0-h166bdaf_0.tar.bz2", \
"pytest-7.1.2-py39hf3d152e_0.tar.bz2", \
"aws-c-event-stream-0.2.7-h3541f99_13.tar.bz2", \
"libopenblas-0.3.20-pthreads_h78a6416_0.tar.bz2", \
"zeromq-4.3.4-h9c3ff4c_1.tar.bz2", \
"pyyaml-5.4.1-py39hb9d737c_2.tar.bz2", \
"numpy-1.22.1-py39h91f2184_0.tar.bz2", \
"libblas-3.9.0-15_linux64_openblas.tar.bz2", \
"kiwisolver-1.4.3-py39hf939315_0.tar.bz2", \
"curl-7.83.1-h7bff187_0.tar.bz2", \
"numba-0.55.2-py39h66db6d7_0.tar.bz2", \
"cffi-1.15.1-py39he91dace_0.tar.bz2", \
"anyio-3.6.1-py39hf3d152e_0.tar.bz2", \
"aws-c-io-0.10.5-hfb6a706_0.tar.bz2", \
"libtiff-4.4.0-hc85c160_1.tar.bz2", \
"arrow-cpp-6.0.1-py39h461039b_20_cpu.tar.bz2", \
"sniffio-1.2.0-py39hf3d152e_3.tar.bz2", \
"cartopy-0.20.2-py39ha2ae0e9_6.tar.bz2", \
"dbus-1.13.6-h5008d03_3.tar.bz2", \
"gstreamer-1.20.3-hd4edc92_0.tar.bz2", \
"libthrift-0.16.0-h519c5ea_1.tar.bz2", \
"expat-2.4.8-h27087fc_0.tar.bz2", \
"nss-3.78-h2350873_0.tar.bz2", \
"libevent-2.1.10-h9b69904_4.tar.bz2", \
"nodejs-16.14.2-h96d913c_1.tar.bz2", \
"lcms2-2.12-hddcbb42_0.tar.bz2", \
"lz4-c-1.9.3-h9c3ff4c_1.tar.bz2", \
"geos-3.10.3-h27087fc_0.tar.bz2", \
"icu-70.1-h27087fc_0.tar.bz2", \
"multidict-6.0.2-py39hb9d737c_1.tar.bz2", \
"pyarrow-6.0.1-py39h42d110c_20_cpu.tar.bz2", \
"matplotlib-3.5.1-py39hf3d152e_0.tar.bz2", \
"ncurses-6.3-h27087fc_1.tar.bz2", \
"distributed-2022.1.0-py39hf3d152e_0.tar.bz2", \
"s2n-1.0.10-h9b69904_0.tar.bz2", \
"libgomp-12.1.0-h8d9b700_16.tar.bz2", \
"libllvm14-14.0.6-he0ac6c6_0.tar.bz2", \
"bokeh-2.4.2-py39hf3d152e_1.tar.bz2", \
"snappy-1.1.9-hbd366e4_1.tar.bz2", \
"netcdf4-1.6.0-nompi_py39hf5a3a3f_100.tar.bz2", \
"libflac-1.3.4-h27087fc_0.tar.bz2", \
"pandoc-2.18-ha770c72_0.tar.bz2", \
"libwebp-1.2.2-h3452ae3_0.tar.bz2", \
"jupyter_core-4.10.0-py39hf3d152e_0.tar.bz2", \
"libgfortran5-12.1.0-hdcd56e2_16.tar.bz2", \
"libogg-1.3.4-h7f98852_1.tar.bz2", \
"gst-plugins-base-1.20.3-hf6a322e_0.tar.bz2", \
"grpc-cpp-1.46.3-hc275302_1.tar.bz2", \
"readline-8.1.2-h0f457ee_0.tar.bz2", \
"brotlipy-0.7.0-py39hb9d737c_1004.tar.bz2", \
"libssh2-1.10.0-ha56f1ee_2.tar.bz2", \
"argon2-cffi-bindings-21.2.0-py39hb9d737c_2.tar.bz2", \
"libgfortran-ng-12.1.0-h69a702a_16.tar.bz2", \
"aiohttp-3.8.1-py39hb9d737c_1.tar.bz2", \
"fftw-3.3.10-nompi_h77c792f_102.tar.bz2", \
"portaudio-19.6.0-h57a0ea0_5.tar.bz2", \
"nb_conda_kernels-2.3.1-py39hf3d152e_1.tar.bz2", \
"xcb-util-keysyms-0.4.0-h166bdaf_0.tar.bz2", \
"zstd-1.5.2-h8a70e8d_2.tar.bz2", \
"pyqt5-sip-12.9.0-py39h5a03fae_1.tar.bz2", \
"liblapack-3.9.0-15_linux64_openblas.tar.bz2", \
"sqlite-3.39.0-h4ff8645_0.tar.bz2", \
"fastparquet-0.8.1-py39hd257fcd_0.tar.bz2", \
"nspr-4.32-h9c3ff4c_1.tar.bz2", \
"wrapt-1.14.1-py39hb9d737c_0.tar.bz2", \
"htop-3.1.2-h46c0cb4_0.tar.bz2", \
"pulseaudio-14.0-h7f54b18_8.tar.bz2", \
"libprotobuf-3.20.1-h6239696_0.tar.bz2", \
"python_abi-3.9-2_cp39.tar.bz2", \
"perl-5.32.1-2_h7f98852_perl5.tar.bz2", \
"xcb-util-renderutil-0.3.9-h166bdaf_0.tar.bz2", \
"libwebp-base-1.2.2-h7f98852_1.tar.bz2", \
"brotli-1.0.9-h166bdaf_7.tar.bz2", \
"libutf8proc-2.7.0-h7f98852_0.tar.bz2", \
"openssl-1.1.1q-h166bdaf_0.tar.bz2", \
"libzip-1.9.2-hc869a4a_0.tar.bz2", \
"libudev1-249-h166bdaf_4.tar.bz2", \
"mistune-0.8.4-py39h3811e60_1005.tar.bz2", \
"libcap-2.64-ha37c62d_0.tar.bz2", \
"attr-2.5.1-h166bdaf_0.tar.bz2", \
"orc-1.7.5-h6c59b99_0.tar.bz2", \
"libbrotlicommon-1.0.9-h166bdaf_7.tar.bz2", \
"zlib-1.2.12-h166bdaf_1.tar.bz2", \
"pyqt-5.15.4-py39h18e9c17_1.tar.bz2", \
"giflib-5.2.1-h36c2ea0_2.tar.bz2", \
"pysocks-1.7.1-py39hf3d152e_5.tar.bz2", \
"libzlib-1.2.12-h166bdaf_1.tar.bz2", \
"freetype-2.10.4-h0708190_1.tar.bz2", \
"libtool-2.4.6-h9c3ff4c_1008.tar.bz2", \
"mysql-libs-8.0.29-h28c427c_1.tar.bz2", \
"yarl-1.7.2-py39hb9d737c_2.tar.bz2", \
"shapely-1.8.2-py39h4fbd0eb_2.tar.bz2", \
"pluggy-1.0.0-py39hf3d152e_3.tar.bz2", \
"xorg-libxau-1.0.9-h7f98852_0.tar.bz2", \
"pcre-8.45-h9c3ff4c_0.tar.bz2", \
"libcups-2.3.3-hf5a7f15_1.tar.bz2", \
"qt-main-5.15.4-ha5833f6_2.tar.bz2", \
"xz-5.2.5-h516909a_1.tar.bz2", \
"libllvm11-11.1.0-hf817b99_3.tar.bz2", \
"s3fs-fuse-1.91-h6a471ff_0.tar.bz2", \
"gflags-2.2.2-he1b5a44_1004.tar.bz2", \
"libxkbcommon-1.0.3-he3ba5ed_0.tar.bz2", \
"code-server-4.4.0-ha770c72_0.tar.bz2", \
"yaml-0.2.5-h7f98852_2.tar.bz2", \
"libcurl-7.83.1-h7bff187_0.tar.bz2", \
"pandas-1.4.0-py39hde0f152_0.tar.bz2", \
"cftime-1.6.1-py39hd257fcd_0.tar.bz2", \
"libxml2-2.9.14-h22db469_3.tar.bz2", \
"watchdog-2.1.9-py39hf3d152e_0.tar.bz2", \
"xcb-util-image-0.4.0-h166bdaf_0.tar.bz2", \
"xcb-util-0.4.0-h166bdaf_0.tar.bz2", \
"cramjam-2.5.0-py39h860a657_0.tar.bz2", \
"fontconfig-2.14.0-h8e229c2_0.tar.bz2", \
"markupsafe-2.1.1-py39hb9d737c_1.tar.bz2", \
"proj-9.0.1-h93bde94_1.tar.bz2", \
"libsndfile-1.0.31-h9c3ff4c_1.tar.bz2", \
"tbb-2021.5.0-h924138e_1.tar.bz2", \
"umap-learn-0.5.2-py39hf3d152e_1.tar.bz2", \
"glib-2.70.2-h780b84a_4.tar.bz2", \
"libgcc-ng-12.1.0-h8d9b700_16.tar.bz2", \
"aws-c-cal-0.5.11-h95a6274_0.tar.bz2", \
"sqlalchemy-1.4.39-py39hb9d737c_0.tar.bz2", \
"libglib-2.70.2-h174f98d_4.tar.bz2", \
"tornado-6.2-py39hb9d737c_0.tar.bz2", \
"scikit-learn-1.1.1-py39h4037b75_0.tar.bz2", \
"unicodedata2-14.0.0-py39hb9d737c_1.tar.bz2", \
"libbrotlienc-1.0.9-h166bdaf_7.tar.bz2", \
"libnghttp2-1.47.0-h727a467_0.tar.bz2", \
"importlib-metadata-4.11.4-py39hf3d152e_0.tar.bz2", \
"lerc-3.0-h9c3ff4c_0.tar.bz2", \
"libsodium-1.0.18-h36c2ea0_1.tar.bz2", \
"libdb-6.2.32-h9c3ff4c_0.tar.bz2", \
"libuuid-2.32.1-h7f98852_1000.tar.bz2", \
"libiconv-1.16-h516909a_0.tar.bz2", \
"click-8.0.3-py39hf3d152e_1.tar.bz2", \
"tk-8.6.12-h27826a3_0.tar.bz2", \
"glib-tools-2.70.2-h780b84a_4.tar.bz2", \
"krb5-1.19.3-h3790be6_0.tar.bz2", \
"keyutils-1.6.1-h166bdaf_0.tar.bz2", \
"xorg-libxdmcp-1.1.3-h7f98852_0.tar.bz2", \
"libopus-1.3.1-h7f98852_1.tar.bz2", \
"aws-checksums-0.1.11-ha31a3da_7.tar.bz2", \
"libstdcxx-ng-12.1.0-ha89aaad_16.tar.bz2", \
"debugpy-1.6.0-py39h5a03fae_0.tar.bz2", \
"fonttools-4.34.2-py39hb9d737c_0.tar.bz2", \
"protobuf-3.20.1-py39h5a03fae_0.tar.bz2", \
"greenlet-1.1.2-py39h5a03fae_2.tar.bz2", \
"libnsl-2.0.0-h7f98852_0.tar.bz2", \
"ca-certificates-2022.6.15-ha878542_0.tar.bz2", \
"pyproj-3.3.1-py39hdcf6798_1.tar.bz2", \
"libcblas-3.9.0-15_linux64_openblas.tar.bz2", \
"ld_impl_linux-64-2.36.1-hea4e1c9_2.tar.bz2", \
"jedi-0.18.1-py39hf3d152e_1.tar.bz2", \
"scipy-1.8.1-py39he49c0e8_0.tar.bz2", \
"openjpeg-2.4.0-hb52868f_1.tar.bz2", \
"libffi-3.4.2-h7f98852_5.tar.bz2", \
"pthread-stubs-0.4-h36c2ea0_1001.tar.bz2", \
"setuptools-59.8.0-py39hf3d152e_1.tar.bz2", \
"terminado-0.15.0-py39hf3d152e_0.tar.bz2", \
"configurable-http-proxy-4.5.1-node16_h3b247e2_1.tar.bz2", \
"git-2.35.0-pl5321hc30692c_0.tar.bz2", \
"glog-0.6.0-h6f12383_0.tar.bz2", \
"aws-c-common-0.6.2-h7f98852_0.tar.bz2", \
"ruamel.yaml-0.17.21-py39hb9d737c_1.tar.bz2", \
"certifi-2022.6.15-py39hf3d152e_0.tar.bz2", \
"aws-sdk-cpp-1.8.186-hb4091e7_3.tar.bz2", \
"psutil-5.9.1-py39hb9d737c_0.tar.bz2", \
"libnetcdf-4.8.1-nompi_h329d8a1_102.tar.bz2", \
"jack-1.9.18-h8c3723f_1002.tar.bz2", \
"ipython-8.4.0-py39hf3d152e_0.tar.bz2", \
"gettext-0.19.8.1-h73d1719_1008.tar.bz2", \
"libev-4.33-h516909a_1.tar.bz2", \
"llvmlite-0.38.1-py39h7d9a04d_0.tar.bz2", \
"xcb-util-wm-0.4.1-h166bdaf_0.tar.bz2", \
"${LOCAL_CONDA_CHANNEL}/linux-64/"]
COPY ["openmp_mutex-4.5-2_gnu.tar.bz2", "${LOCAL_CONDA_CHANNEL}/linux-64/_openmp_mutex-4.5-2_gnu.tar.bz2"]
COPY ["libgcc_mutex-0.1-conda_forge.tar.bz2", "${LOCAL_CONDA_CHANNEL}/linux-64/_libgcc_mutex-0.1-conda_forge.tar.bz2"]

COPY ["code_server.tar.gz", \ 
"start.sh", \ 
"start-notebook.sh", \ 
"start-singleuser.sh", \ 
"/home/${NB_USER}/"]

#End_of_copy_DONT_DELETE


RUN mv "/home/${NB_USER}/code_server.tar.gz" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start.sh" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start-notebook.sh" /usr/local/bin/ \
    && mv "/home/${NB_USER}/start-singleuser.sh" /usr/local/bin/ \
    && chmod +x /usr/local/bin/start.sh \
    && chmod +x /usr/local/bin/start-notebook.sh \
    && chmod +x /usr/local/bin/start-singleuser.sh
    

RUN chown -R ${NB_USER}:${NB_USER} ${LOCAL_CONDA_CHANNEL}

RUN chown -R ${NB_USER}:${NB_USER} /opt/
RUN chown -R ${NB_USER}:${NB_USER} /home/

COPY --chown=${NB_USER}:${NB_USER} config/jupyter_notebook_config.py /home/${NB_USER}/.jupyter/
COPY --chown=${NB_USER}:${NB_USER} scripts/local_channel_env.yaml ${LOCAL_CONDA_CHANNEL}/

USER ${NB_USER}

RUN mkdir "/home/${NB_USER}/work"

# Create directories for TIP
RUN mkdir "/home/${NB_USER}/conf"
RUN mkdir "/home/${NB_USER}/tip_scripts"
 
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
#WORKDIR "/home/${NB_USER}/"
ENTRYPOINT ["tini", "--", "/usr/bin/bash",".init/start.sh"]

HEALTHCHECK NONE
