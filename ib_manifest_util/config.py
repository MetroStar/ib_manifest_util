from ib_manifest_util import DEVELOPMENT_DIR, TEMPLATE_DIR, TEST_DATA_DIR


class HardeningManifestConfig:
    """A class to hold the hardening manifest config_class data.

    Attributes:
        template_name: str
        template_dir: str | Path
        output_path: str | Path
        expected_output_path: str | Path
        content: dict

    """

    def __init__(self):
        self.template_name = "hardening_manifest.tpl"
        self.template_dir = TEMPLATE_DIR
        self.output_path = DEVELOPMENT_DIR.joinpath("hardening_manifest.yaml")
        self.expected_output_path = TEST_DATA_DIR.joinpath(
            "hardening_manifest_expected.yaml"
        )
        self.content = {
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


class DockerCondaConfig:
    """A class to hold the Docker config_class data.

    Attributes:
    template_name: str
    template_dir: str | Path
    output_path: str | Path
    expected_output_path: str | Path
    content: dict

    """

    def __init__(self):
        self.template_name = "Dockerfile_conda.tpl"
        self.template_dir = TEMPLATE_DIR
        self.output_path = DEVELOPMENT_DIR.joinpath("Dockerfile")
        self.expected_output_path = TEST_DATA_DIR.joinpath("dockerfile_expected")
        # TODO: Fill with content
        self.content = {}
