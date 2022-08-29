import logging
from pathlib import Path

import requests

from ib_manifest_util import PACKAGE_DIR
from ib_manifest_util.util import load_yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_packages(manifest_path: str | Path = None, urls: list = None):
    """Download conda packages from a manifest file or a list of urls.

    Choose either a manifest file or a list of urls, not both.

    Args:
        manifest_path: str | Path
            Optional path to manifest file.  Superseded by urls.
        urls: list
            Optional list of package urls to download.  Supersedes manifest_path.

    """
    # manifest only
    if manifest_path and not urls:
        manifest = load_yaml(manifest_path)
        urls = [x["url"] for x in manifest["resources"]]
    # neither
    elif not urls and not manifest_path:
        manifest_path = Path(PACKAGE_DIR, "hardening_manifest.yaml")
        manifest = load_yaml(manifest_path)
        urls = [x["url"] for x in manifest["resources"]]
    # both
    elif urls and manifest_path:
        logger.warning(
            "Only one parameter, `urls` or `manifest_path`, can be used in download_packages, but both were passed.  Only urls will be used."
        )

    for i, url in enumerate(urls):
        fname = url.split("/")[-1].lstrip("_")
        print(f"Downloading {i + 1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            if r.status_code == 404:
                message = f"URL '{url}'\n was not found.  Package was not downloaded."
                logger.warning(message)
            else:
                with open(Path(PACKAGE_DIR, fname), "wb") as f:
                    f.write(r.content)


if __name__ == "__main__":
    download_packages()
