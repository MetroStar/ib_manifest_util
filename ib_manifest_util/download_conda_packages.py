import requests
from ib_manifest_util.util import load_yaml


def download_packages():
    manifest = load_yaml("../hardening_manifest.yaml")

    urls = [x["url"] for x in manifest["resources"]]

    for i, url in enumerate(urls):
        fname = url.split("/")[-1].lstrip("_")
        print(f"Downloading {i + 1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            with open(f"../{fname}", "wb") as f:
                f.write(r.content)


if __name__ == "__main__":
    download_packages()
