import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

BASE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02135/north/daily/geotiff/"
ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "all_source"

INCLUDE_KEYWORD = "_extent_v4.0.tif" # "_concentration_v4.0.tif" || "_extent_v4.0.tif" || None
START_YEAR = 2025
END_YEAR = 2025

def safe_request(url):
    for _ in range(5):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            return r
        except Exception as e:
            print(f"request fail {url}: {e}")
            time.sleep(3)
    return None

def crawl(url, local_dir):
    r = safe_request(url)
    if not r:
        return
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):
        href = link.get("href")
        if not href or href.startswith("../"):
            continue
        full_url = urljoin(url, href)

        if href.endswith("/"):
            if href.strip("/").isdigit():
                year = int(href.strip("/"))
                if not (START_YEAR <= year <= END_YEAR):
                    continue
            subdir = local_dir / href.strip("/")
            subdir.mkdir(parents=True, exist_ok=True)
            crawl(full_url, subdir)
        elif href.endswith(".tif"):
            if INCLUDE_KEYWORD and INCLUDE_KEYWORD not in href:
                continue
            file_path = local_dir / os.path.basename(href)
            if file_path.exists():
                print(f"Already exist: {file_path.name}")
                continue
            print(f"download: {href}")
            try:
                with requests.get(full_url, stream=True) as resp:
                    resp.raise_for_status()
                    with open(file_path, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"saved: {file_path}")
            except Exception as e:
                print(f"download fail {href}: {e}")
    time.sleep(0.5)


OUTPUT_DIR.mkdir(exist_ok=True)
crawl(BASE_URL, OUTPUT_DIR)
