import multiprocessing as mp
import os
from typing import Optional

from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.utils import NumpySafeJSONResponse

from .fork import fork_and_do
from .tasks import fetch_children, fetch_metadata, fetch_shapes, fetch_slice, fetch_tree

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

router = APIRouter()


@router.get("/info/")
def get_info(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to output the info of the HDF5 file node."""
    info = fork_and_do(fetch_metadata, args=(path, subpath, SWMR_DEFAULT))
    return NumpySafeJSONResponse(info)


@router.get("/search/")
def get_children(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to output the subnodes of the HDF5 file node."""
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_children, args=(path, subpath, SWMR_DEFAULT, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


@router.get("/shapes/")
def get_shapes(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to get the shapes of the HDF5 datasets."""
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_shapes, args=(path, subpath, SWMR_DEFAULT, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


@router.get("/slice/")
def get_slice(
    path: str, subpath: str = "/", slice_info: Optional[str] = None
) -> JSONResponse:
    """Function that tells flask to output the metadata of the HDF5 file node.
    The slice_info parameter should take the form
    start:stop:steps,start:stop:steps,...
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(
        target=fetch_slice, args=(path, subpath, slice_info, SWMR_DEFAULT, queue)
    )
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


@router.get("/tree/")
def get_tree(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to render the tree of the HDF5 file."""
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_tree, args=(path, subpath, SWMR_DEFAULT, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())
