import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from ib_manifest_util import TEMPLATE_DIR, TEST_DATA_DIR
from ib_manifest_util.util import dump_yaml, load_yaml


@pytest.fixture(scope="session")
def repo_dir(tmp_path_factory):
    sample_repo_dir = TEST_DATA_DIR.joinpath("sample_repo")
    test_output_dir = "tmp_repo1"
    fn = tmp_path_factory.mktemp(test_output_dir)
    shutil.copytree(sample_repo_dir, fn, dirs_exist_ok=True)

    return fn


@pytest.fixture(scope="session")
def dockerfile_default_tpl():
    template_path = TEMPLATE_DIR.joinpath("Dockerfile_default.tpl")
    return template_path


@pytest.fixture(scope="session")
def hardening_manifest_tpl():
    template_path = TEMPLATE_DIR.joinpath("hardening_manifest.tpl")
    return template_path


@pytest.fixture(scope="session")
def hardening_manifest_content():
    content = {
        "apiVersion": "v1",
        "name": "opensource/metrostar/singleuser",
        "tags": ["singeluser_v12"],
        "args": {
            "base_image": "opensource/metrostar/miniconda",
            "base_tag": "4.12.0",
        },
        "labels": {
            "title": "singleuser",
            "description": "A base-notebook Singleuser image to use with JupyterHub",
            "licenses": "BSD 3-Clause",
            "url": "https://repo1.dso.mil/dsop/opensource/metrostar/singleuser",
            "vendor": "MetroStar Systems",
            "version": "singleuser_v11",
            "keywords": "conda,python,jupyter,jupyterhub,jupyterlab",
            "type": "opensource",
            "name": "metrostar",
        },
        "resources": [
            {
                "url": "https://github.com/dirkcgrunwald/jupyter_codeserver_proxy-/archive/5596bc9c2fbd566180545fa242c659663755a427.tar.gz",
                "filename": "code_server.tar.gz",
                "validation": {
                    "type": "sha256",
                    "value": "7a286d6f201ae651368b65505cba7b0a137c81b2ac0fd637160d082bb14db032",
                },
            }
        ],
        "maintainers": [
            {
                "email": "example@example.com",
                "name": "John Dor",
                "username": "user",
                "cht_member": "false",
            }
        ],
    }
    return content


@pytest.fixture(scope="session")
def dockerfile_default_content():
    content = {
        "noarch_packages": ["requests-2.28.1-pyhd8ed1ab_1.tar.bz2"],
        "linux_packages": ["python-3.10.6-h582c2e5_0_cpython.tar.bz2"],
        "underscore_packages": ["openmp_mutex-4.5-2_gnu.tar.bz2"],
    }

    return content


@pytest.fixture
def cleanup():
    """Ensure removal of test files after testing is done.

    Call this function from the test function and append Path objects
    to it for cleaning up, even if the assertion fails.

    """
    to_delete = []
    yield to_delete
    for item in to_delete:
        if Path(item).exists:
            item.unlink()


@pytest.fixture
@pytest.mark.web
def conda_vendor_data(tmp_path_factory):
    """Run `conda-vendor vendor` and run location of temp dir. Clean up when done.

    NOTE: This fixture attempts to download packages from the `conda-forge` channel and store
    them in a temporary directory. This will likely take 30-60 seconds to run.
    """

    env_name = "my_local_channel_env"

    env = {
        "name": env_name,
        "channels": ["conda-forge"],
        "dependencies": [
            "tzdata",
            "python-json-logger",
        ],
    }

    conda_vendor_dir = tmp_path_factory.mktemp("conda_vendor_data")
    tmp_env_file = conda_vendor_dir / f"{env_name}.yaml"
    dump_yaml(env, tmp_env_file)

    try:
        shutil.rmtree(conda_vendor_dir / env_name)
    except FileNotFoundError:
        pass

    os.chdir(conda_vendor_dir)
    command = (
        f"conda-vendor vendor --file {tmp_env_file} --solver conda --platform linux-64"
    )

    proc = subprocess.check_call(
        command.split(" "), stdout=sys.stdout, stderr=sys.stderr
    )

    yield conda_vendor_dir, env_name

    shutil.rmtree(conda_vendor_dir)
