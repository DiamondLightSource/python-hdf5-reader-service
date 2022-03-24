import multiprocessing as mp
import os
from typing import Optional

import h5py
from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.utils import NumpySafeJSONResponse

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))


# Setup blueprint route
@router.get("/slice/")
def get_slice(
    path: str, subpath: str = "/", slice_info: Optional[str] = None
) -> JSONResponse:
    """Function that tells flask to output the metadata of the HDF5 file node.
    The slice_info parameter should take the form
    start:stop:steps,start:stop:steps,...
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_slice, args=(path, subpath, queue, slice_info))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_slice(
    path: str, subpath: str, slice_info: Optional[str], queue: mp.Queue
) -> None:
    path = "/" + path

    if slice_info is not None:
        # Create slice objects from strings, e.g.
        # convert "1:2:1,3:4:1" to tuple(slice(1, 2, 1), slice(3, 4, 1))
        slices = tuple(
            map(lambda t: slice(*map(int, t.split(":"))), slice_info.split(","))
        )
    else:
        # Default to getting the whole dataset
        # slices = ...
        pass

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as f:
        if subpath in f:
            dataset = f[subpath]
            if isinstance(dataset, h5py.Dataset):
                queue.put(dataset[slices])
            else:
                raise Exception(
                    f"Expected {subpath} to be a dataset, \
                        it is acually a {type(dataset)}"
                )
        else:
            raise Exception(f"{path} does not contain {subpath}")
