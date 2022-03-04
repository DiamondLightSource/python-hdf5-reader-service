from fastapi import APIRouter
import h5py
import os
from ..utils import safe_json_dump

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

# Setup blueprint route
@router.get("/search/{path:path}")
def get_nodes(path: str, subpath: str = "/"):
    """Function that tells flask to output the subnodes of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    path = "/" + path

    try:

        with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
            if subpath:
                nodes = search(file[subpath])
            else:
                nodes = search(file["/"])
            return nodes

    except:
        print(f"File {file} can not be opened yet.")


def search(node):
    subnodes = safe_json_dump({"nodes": list(node.keys())})
    return subnodes
