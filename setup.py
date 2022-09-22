from pathlib import Path

from setuptools import find_packages, setup

# get the vesion number
root_dir = Path(__file__).absolute().parent
# import __version__
exec(open(root_dir / "ib_manifest_util/_version.py").read())

setup(
    name="ib_manifest_util",
    version=__version__,
    install_requires=["click", "ruamel.yaml", "conda_vendor", "jinja2"],
    packages=find_packages(),
    package_data={"ib_manifest_util": ["templates/*"]},
    entry_points={"console_scripts": ["ib_manifest_util = ib_manifest_util.cli:main"]},
)
