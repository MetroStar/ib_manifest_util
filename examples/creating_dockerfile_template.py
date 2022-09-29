from ib_manifest_util import TEMPLATE_DIR
from ib_manifest_util.util import write_templatized_file

template_filename = "Dockerfile_default.tpl"
template_dir = TEMPLATE_DIR

output_path = "example_Dockerfile"

content = {
    "noarch_packages": [
        "fonts-conda-ecosystem-1-0.tar.bz2",
        "geopandas-base-0.11.1-pyha770c72_0.tar.bz2",
        "cloudpickle-2.1.0-pyhd8ed1ab_0.tar.bz2",
    ],
    "linux_packages": [
        "libnetcdf-4.8.1-nompi_h21705cb_104.tar.bz2",
        "tornado-6.1-py39hb9d737c_3.tar.bz2",
        "curl-7.83.1-h7bff187_0.tar.bz2",
    ],
    "underscore_packages": [
        "openmp_mutex-4.5-2_gnu.tar.bz2",
        "libgcc_mutex-0.1-conda_forge.tar.bz2",
    ],
}

write_templatized_file(
    template_filename=template_filename,
    output_path=output_path,
    content=content,
    template_dir=template_dir,
)
