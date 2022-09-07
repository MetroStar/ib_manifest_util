import logging
from pathlib import Path

import click
import requests

from ib_manifest_util import DEFAULT_MANIFEST_FILENAME, PACKAGE_DIR
from ib_manifest_util.util import load_yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_packages(
    manifest_path: str | Path = None,
    urls: list = None,
    download_path: str | Path = Path.cwd(),
):
    """
    Download conda packages from a manifest file or a list of urls.
    Choose either a manifest file or a list of urls, not both.

    Args:
        manifest_path: str | Path
            Optional path to manifest file.  Superseded by urls.
        urls: list
            Optional list of package urls to download.  Supersedes manifest_path.
        download_path: str | Path
            Optional path to download package. Default: current working directory

    """

    if isinstance(manifest_path, str):
        manifest_path = Path(manifest_path)

    if isinstance(download_path, str):
        download_path = Path(download_path)

    def _get_urls_from_manifest(path):
        try:
            manifest = load_yaml(path)
            return [x["url"] for x in manifest["resources"]]
        except FileNotFoundError as e:
            logger.error(f" No manifest file found at specified path: {path.resolve()}")
            raise e

    if manifest_path and urls:
        logger.warning(
            " Only one parameter, `urls` or `manifest_path`, can be used in download_packages, but both were passed.  Only `urls` will be used."
        )

    elif urls:
        pass

    elif manifest_path:
        urls = _get_urls_from_manifest(manifest_path)

    elif not manifest_path and not urls:
        manifest_path = Path.cwd() / DEFAULT_MANIFEST_FILENAME
        logger.info(
            f" No `urls` or `manifest_path` specified. An attempt will be made using the default manifest file: {manifest_path}"
        )
        urls = _get_urls_from_manifest(manifest_path)

    logger.info(f" Downloading packages to: {download_path.resolve()}")
    for i, url in enumerate(urls):
        fname = url.split("/")[-1].lstrip("_")
        print(f"Downloading {i + 1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            if r.status_code == 404:
                logger.warning(
                    f" URL '{url}'\n was not found.  Package was not downloaded."
                )
            else:
                with open(download_path / fname, "wb") as f:
                    f.write(r.content)


if __name__ == "__main__":
    download_packages()
