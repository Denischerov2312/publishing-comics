from pathlib import Path, PurePosixPath

import requests


def download_picture(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    make_directory(filepath)
    with open(filepath, "wb") as file:
        file.write(response.content)


def make_directory(filepath):
    path = PurePosixPath(filepath)
    directory_path = list(path.parents)[0]
    Path(directory_path).mkdir(parents=True, exist_ok=True)
