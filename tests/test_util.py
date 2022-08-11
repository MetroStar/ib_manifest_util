from ib_manifest_util import TEMPLATE_DIR, TEST_DATA_DIR
from ib_manifest_util.util import write_templatized_file


def test_write_templatized_file_hardening():
    # TODO this is just copied over, may need work
    hardening_manifest_tpl = TEMPLATE_DIR.joinpath("hardening_manifest.tpl")
    hardening_manifest_path = TEST_DATA_DIR.joinpath("harrdening_manifest.yaml")

    content = {
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
        "resources": {
            "url": "https://github.com/dirkcgrunwald/jupyter_codeserver_proxy-/archive/5596bc9c2fbd566180545fa242c659663755a427.tar.gz",
            "filename": "code_server.tar.gz",
            "validation_type": "sha256",
            "validation_value": "7a286d6f201ae651368b65505cba7b0a137c81b2ac0fd637160d082bb14db032",
        },
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
