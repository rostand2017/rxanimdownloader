from tqdm import tqdm
import requests
import os
import json
import sys

DOWNLOAD_FILE = "./downloader/"
os.makedirs(DOWNLOAD_FILE, exist_ok=True)
print(sys.argv[1])
with open(sys.argv[1]) as file:
    download_list = json.load(file)
i = 1
for download_item in download_list:
    res = requests.get(download_item.get('download_link'), stream=True)
    total_size = int(res.headers['content-length'])
    filename = "{}{}".format(DOWNLOAD_FILE, download_item.get('title'), download_item.get('download_link').split(".")[-1])

    total_kb = total_size / 1024
    total_mb = total_size / (1024 * 1024)

    unit = "MB" if total_mb >= 1 else "KB"
    total = total_mb if total_mb >= 1 else total_kb
    chunk_size = (1024 * 1024) if total_mb >= 1 else 1024

    with open(filename, "wb") as f:
        for data in tqdm(iterable=res.iter_content(chunk_size=chunk_size), total=total, unit=unit):
            f.write(data)
    print("file %s completed !" % i)
    i += 1

print(">>>>>>  All downloads completed !  <<<<<<")