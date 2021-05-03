import pickle as pk
from pathlib import Path


# -----------------------------------------------------------------------------
# Load from disk
# -----------------------------------------------------------------------------
def open_file(path_to: str):
    path_to_load = Path(path_to)
    if not path_to_load.exists():
        return None
    with open(path_to, 'rb') as file:
        obj = pk.load(file)
    return obj
