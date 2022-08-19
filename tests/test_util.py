from ib_manifest_util.config import HardeningManifestConfig
from ib_manifest_util.util import load_yaml, write_templatized_file


def test_write_templatized_file_hardening():
    """Test the ability to write the hardening_manifest.yaml file with a template."""
    hmc = HardeningManifestConfig()

    write_templatized_file(
        template_filename=hmc.template_name,
        output_path=hmc.output_path,
        content=hmc.content,
    )

    # Check that the file was written
    assert (
        hmc.output_path.exists()
    ), f"Hardening manifest file should exist here: {hmc.output_path}"

    # Compare file content with expected content
    output_manifest = load_yaml(hmc.output_path)
    expected_manifest = load_yaml(hmc.output_expected_path)
    assert output_manifest == expected_manifest
