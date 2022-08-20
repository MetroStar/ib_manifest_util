import urllib
from pathlib import Path

import pytest

from ib_manifest_util import TEMPLATE_DIR, TEST_DATA_DIR
from ib_manifest_util.util import download_file, write_templatized_file


def test_write_templatized_file_hardening():
    hardening_manifest_tpl = "hardening_manifest.tpl"
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

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
                "email": "jvelando@metrostarsystems.com",
                "name": "Jonathan Velando",
                "username": "jvelando",
                "cht_member": "false",
            }
        ],
    }

    write_templatized_file(hardening_manifest_tpl, hardening_manifest_path, content)


def test_download_file_good_url():
    """Test downloading good URLs."""

    url = "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2"
    f_name = download_file(url=url)

    assert f_name == "backports-1.0-py_2.tar.bz2", "Filename should match name in URL."

    f_path = Path(f_name).resolve()
    assert f_path.exists(), f"File should be written to {f_path}."

    size = f_path.stat().st_size
    assert 4000 > size > 3000, "File size should be around 3.6kB."

    # Remove the file (clean up)
    f_path.unlink()


def test_download_file_bad_url():
    """Test downloading bad URLs with typos, incomplete paths, etc."""

    # Unknown URL type: ValueError (Missing https://)
    url = "conda.anaconda.org"
    with pytest.raises(ValueError):
        download_file(url=url)

    # Forbidden (No path to file)
    url = "https://conda.anaconda.org"
    with pytest.raises(urllib.error.HTTPError):
        download_file(url=url)

    # Not found (Dummy package name)
    url = "https://conda.anaconda.org/conda-forge/noarch/dd812b10e81f8afcf74310a39b69fca49c27d847.tar.bz2"
    with pytest.raises(urllib.error.HTTPError):
        download_file(url=url)
