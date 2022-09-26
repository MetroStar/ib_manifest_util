import urllib
from ast import Call
from distutils.command.install_egg_info import safe_name
from pathlib import Path
from subprocess import CalledProcessError

import pytest
from ruamel.yaml import YAML

from ib_manifest_util import TEST_DATA_DIR
from ib_manifest_util.util import (
    download_files,
    dump_yaml,
    load_yaml,
    run_subprocess,
    verify_local_channel_environments,
    write_templatized_file,
)


def test_write_templatized_file_hardening(
    hardening_manifest_tpl, tmpdir, hardening_manifest_content
):
    """Test writing a hardening manifest file via template"""
    template_filename = hardening_manifest_tpl.name
    template_dir = hardening_manifest_tpl.parent.resolve()
    output_path = Path(tmpdir.join("test_hardening_manifest.yaml"))

    write_templatized_file(
        template_filename=template_filename,
        output_path=output_path,
        content=hardening_manifest_content,
        template_dir=template_dir,
    )


def test_write_templatized_file_dockefile_default(
    dockerfile_default_tpl, tmpdir, dockerfile_default_content
):
    """Test writing a dockerfile (default) via template"""
    template_filename = dockerfile_default_tpl.name
    template_dir = dockerfile_default_tpl.parent.resolve()
    output_path = Path(tmpdir.join("test_dockerfile"))

    write_templatized_file(
        template_filename=template_filename,
        output_path=output_path,
        content=dockerfile_default_content,
        template_dir=template_dir,
    )


@pytest.mark.web
def test_download_file_good_url(cleanup):
    """Test downloading from good URLs."""

    url = "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2"
    f_name = download_files(urls=[url])[0]
    f_path = Path(f_name).resolve()

    cleanup.append(f_path)

    assert f_name == "backports-1.0-py_2.tar.bz2", "Filename should match name in URL."

    assert f_path.exists(), f"File should be written to {f_path}."

    size = f_path.stat().st_size
    assert 3000 < size < 4000, "File size should be around 3.6kB."


@pytest.mark.web
def test_download_file_bad_url():
    """Test downloading from bad URLs, with typos, incomplete paths, etc."""

    # Unknown URL type: ValueError (Missing https://)
    url = "conda.anaconda.org"
    with pytest.raises(ValueError):
        download_files(urls=[url])

    # Forbidden (No path to file)
    url = "https://conda.anaconda.org"
    with pytest.raises(urllib.error.HTTPError):
        download_files(urls=[url])

    # Not found (Dummy package name)
    url = "https://conda.anaconda.org/conda-forge/noarch/dd812b10e81f8afcf74310a39b69fca49c27d847.tar.bz2"
    with pytest.raises(urllib.error.HTTPError):
        download_files(urls=[url])


@pytest.mark.web
def test_download_file_multiple_urls(cleanup):
    """Test downloading more than one file."""
    urls = [
        "https://conda.anaconda.org/conda-forge/noarch/backports-1.0-py_2.tar.bz2",
        "https://conda.anaconda.org/conda-forge/noarch/typing-extensions-4.3.0-hd8ed1ab_0.tar.bz2",
    ]
    f_names = download_files(urls=urls)

    for f_name in f_names:
        f_path = Path(f_name).resolve()
        cleanup.append(f_path)
        assert f_path.exists(), f"File should be written to {f_path}."


def test_dump_yaml(cleanup):
    """Test that dictionary is correctly written to .yaml file"""
    sample_yaml_path = TEST_DATA_DIR.joinpath("sample_yaml.yaml")
    tempfile_path = Path("tempfile.yaml").resolve()
    cleanup.append(tempfile_path)

    sample_yaml_dict = load_yaml(sample_yaml_path)

    # Test path type Path
    dump_yaml(sample_yaml_dict, target_path=tempfile_path)
    tempfile_dict = load_yaml(tempfile_path)
    assert (
        tempfile_dict["myKey"] == "myValue"
    ), "Loaded yaml file should provide correct key-value pair."


def test_load_yaml_path_types():
    """Test load_yaml file_path arg"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

    # Test path type str
    hardening_manifest = load_yaml(file_path=str(hardening_manifest_path))
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."

    # Test path type Path
    hardening_manifest = load_yaml(file_path=hardening_manifest_path)
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."

    # Test missing file
    with pytest.raises(FileNotFoundError):
        load_yaml("this_file_does_not_exist.yaml")


def test_load_yaml_return_type():
    """Test load_yaml return type"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")
    hardening_manifest = load_yaml(file_path=hardening_manifest_path)
    assert isinstance(
        hardening_manifest, dict
    ), "Returned object should be a dictionary."


def test_load_yaml_loaders():
    """Test load_yaml loader_type arg"""
    hardening_manifest_path = TEST_DATA_DIR.joinpath("hardening_manifest.yaml")

    # Test safe load
    hardening_manifest = load_yaml(
        file_path=hardening_manifest_path, loader_type="safe"
    )
    assert (
        hardening_manifest["apiVersion"] == "v1"
    ), "Loaded yaml file should provide correct key-value pair."


def test_run_subprocess(capsys):
    """Test a subprocess call."""
    command_test = "echo hello"
    run_subprocess(command_test)
    captured = capsys.readouterr()
    assert captured.err == "", "No errors should result from subprocess."
    assert captured.out == "hello\n", "Subprocess output should match the test string."


@pytest.mark.web
def test_verify_local_channel_environment(conda_vendor_data):
    """Test verify_local_channel_environment using actual conda-vendor data."""

    conda_vendor_dir, env_name = conda_vendor_data

    # load existing env file
    tmp_env_file = conda_vendor_dir / f"{env_name}.yaml"
    env = load_yaml(tmp_env_file)

    # swap out channels: `conda-forge` for `./my_local_channel_env` dir
    env["channels"][0] = str(conda_vendor_dir / env_name)
    dump_yaml(env, tmp_env_file)

    assert verify_local_channel_environments(tmp_env_file)
