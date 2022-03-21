import multiprocessing as mp
import os

import h5py
from fastapi import APIRouter

from hdf5_reader_service.utils import NumpySafeJSONResponse

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))


# Setup blueprint route
@router.get("/search/")
def get_nodes(path: str, subpath: str = "/"):
    """Function that tells flask to output the subnodes of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_nodes, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_nodes(path, subpath, queue):
    path = "/" + path

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
        if subpath:
            nodes = search(file[subpath])
        else:
            nodes = search(file["/"])
        queue.put(nodes)


def search(node):
    subnodes = {"nodes": list(node.keys())}
    return subnodes
