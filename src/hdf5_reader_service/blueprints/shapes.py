import multiprocessing as mp
import os
from typing import Any, Mapping

import h5py
from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.utils import NumpySafeJSONResponse, h5_tree_map

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

router = APIRouter()


# Setup blueprint route
@router.get("/shapes/")
def show_shapes(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to get the shapes of the HDF5 datasets.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_shapes, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_shapes(path: str, subpath: str, queue: mp.Queue) -> None:

    path = "/" + path

    def get_shape(name: str, obj: h5py.HLObject) -> Mapping[str, Any]:
        if hasattr(obj, "shape"):
            return {"shape": obj.shape}
        else:
            return {"shape": None}

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as f:
        tree = h5_tree_map(get_shape, f, map_name="metadata")

    queue.put(tree)
