import os

import h5py
from fastapi import APIRouter

from ..utils import LOCK, NumpySafeJSONResponse

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))


# Setup blueprint route
@router.get("/search/{path:path}")
def get_nodes(path: str, subpath: str = "/"):
    """Function that tells flask to output the subnodes of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    with LOCK:

        path = "/" + path

        with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
            if subpath:
                nodes = NumpySafeJSONResponse(search(file[subpath]))
            else:
                nodes = NumpySafeJSONResponse(search(file["/"]))
            return nodes


def search(node):
    subnodes = {"nodes": list(node.keys())}
    return subnodes
