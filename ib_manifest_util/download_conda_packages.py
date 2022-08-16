from pathlib import Path

import requests

from ib_manifest_util.util import load_yaml


def download_packages(
    manifest_path: str | Path = "../hardening_manifest.yaml", urls: list = None
):
    """Download conda packages from a manifest file or a list of urls.

    Args:
        manifest_path: str | Path
            Path to manifest file.
        urls: list
            Optional list of package urls to download.  Supersedes manifest_path.

    """
    if not urls:
        manifest = load_yaml(manifest_path)
        urls = [x["url"] for x in manifest["resources"]]

    for i, url in enumerate(urls):
        fname = url.split("/")[-1].lstrip("_")
        print(f"Downloading {i + 1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            with open(f"../{fname}", "wb") as f:
                f.write(r.content)


if __name__ == "__main__":
    download_packages()
