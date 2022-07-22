from ruamel.yaml import YAML
import requests
yaml=YAML(typ='safe')


def download_packages():
    manifest = yaml.load(open('../hardening_manifest.yaml').read())
    
    urls = [x['url'] for x in manifest['resources']]
    
    for i, url in enumerate(urls):
        fname = url.split('/')[-1].lstrip('_')
        print(f"Downloading {i+1} of {len(urls)}: {fname}")
        with requests.get(url, allow_redirects=True) as r:
            with open(f"../{fname}", 'wb') as f:
                f.write(r.content)

if __name__ == "__main__":
    download_packages()
    
