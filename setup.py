from setuptools import setup, find_packages, find_namespace_packages
from pathlib import Path

root_dir = Path(__file__).absolute().parent

__version__ = None
exec(open(root_dir / "ib_manifest_util/version.py").read())

setup(
    name="ib_manifest_util",
    version=__version__,
    install_requires=["click", "ruamel.yaml", "conda_vendor"],
    packages=find_packages(),
    entry_points={"console_scripts": ["ib_manifest_util = ib_manifest_util.__main__:main"]}   
)