import os
import json

def _open_file(path, mode):
    parent = os.path.dirname(path)

    if parent:
        os.makedirs(parent, exist_ok=True)

    return open(path,mode)

def log(path, data):
    with _open_file(path, "a") as f:
        f.seek(0, os.SEEK_END)
        f.write(json.dumps(data) + "\n")

def read(path):
    with _open_file(path, "r") as f:
        f.seek(0)
        return [json.loads(line) for line in f if line]
