from pathlib import Path


def read_md(path_file: str | Path):
    with open(path_file, encoding="utf-8") as f:
        file = f.read()
    return file
