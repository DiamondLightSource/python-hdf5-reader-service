import multiprocessing as mp
import os
from typing import Any, Mapping

import h5py
from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.blueprints.info import metadata
from hdf5_reader_service.utils import NumpySafeJSONResponse, h5_tree_map

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

router = APIRouter()


# Setup blueprint route
@router.get("/tree/")
def show_tree(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to render the tree of the HDF5 file."""
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_nodes, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_nodes(path: str, subpath: str, queue: mp.Queue) -> None:
    path = "/" + path

    def get_metadata(name: str, obj: h5py.HLObject) -> Mapping[str, Any]:
        return metadata(obj)

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as f:
        tree = h5_tree_map(get_metadata, f, map_name="metadata")

    queue.put(tree)
