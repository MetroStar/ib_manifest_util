from ib_manifest_util.config import DockerCondaConfig, HardeningManifestConfig
from ib_manifest_util.util import load_yaml, write_templatized_file


def write_templatized_file_test(config_class):
    """Test ability to write file with a template."""

    write_templatized_file(
        template_filename=config_class.template_name,
        output_path=config_class.output_path,
        content=config_class.content,
        template_dir=config_class.template_dir,
    )

    # Check that the file was written
    assert (
        config_class.output_path.exists()
    ), f"Templatized file should exist here: {config_class.output_path}"

    # Compare file content with expected content
    output = load_yaml(config_class.output_path)
    expected = load_yaml(config_class.expected_output_path)
    assert output == expected


def test_write_templatized_file_hardening():
    """Test hardening_manifest.yaml"""
    write_templatized_file_test(HardeningManifestConfig())


# def test_write_templatized_file_docker_conda():
#     write_templatized_file_test(DockerCondaConfig())


def write_templatized_file_ib_manifest():
    pass


def write_templatized_file_local_channel_env():
    pass


def test_write_templatized_file_start_scripts():
    pass
