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
@router.get("/info/")
def get_info(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to output the info of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_info, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_info(path: str, subpath: str, queue: mp.Queue) -> None:

    path = "/" + path

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
        if subpath:
            meta = metadata(file[subpath])
        else:
            meta = metadata(file["/"])
        queue.put(meta)


def metadata(node: h5py.HLObject) -> Mapping[str, Any]:

    name = node.name
    metadata = dict(node.attrs)

    data = {"name": name, "data": {"attributes": {"metadata": metadata}}}

    if isinstance(node, h5py.Dataset):
        shape = node.shape
        chunks = node.chunks
        itemsize = node.dtype.itemsize
        kind = node.dtype.kind
        # endianness = dtype.endiannness if dtype.endiannness else "not_applicable"

        macro = {"chunks": chunks, "shape": shape}
        micro = {"itemsize": itemsize, "kind": kind}
        structure = {"macro": macro, "micro": micro}

        data["data"]["attributes"]["structure"] = structure

    return data
