import multiprocessing as mp
import os
from typing import Any, Mapping

import h5py
from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.utils import NumpySafeJSONResponse

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))


# Setup blueprint route
@router.get("/search/")
def get_nodes(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to output the subnodes of the HDF5 file node."""
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_nodes, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_nodes(path: str, subpath: str, queue: mp.Queue) -> None:
    path = "/" + path

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as f:

        node = f[subpath]

        if not isinstance(node, h5py.Group):
            queue.put({"INFO": "Please provide a path to a dataset"})
        else:
            nodes = search(node)
            queue.put(nodes)


def search(node: h5py.Group) -> Mapping[str, Any]:
    subnodes = {"nodes": list(node.keys())}
    return subnodes
