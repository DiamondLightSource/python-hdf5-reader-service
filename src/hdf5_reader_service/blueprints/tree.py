import multiprocessing as mp
import os
import time
from collections import defaultdict
from typing import Any, Dict, List, Union

import h5py
from fastapi import APIRouter
from starlette.responses import JSONResponse

from hdf5_reader_service.blueprints.info import metadata
from hdf5_reader_service.utils import NumpySafeJSONResponse

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

router = APIRouter()


# Setup blueprint route
@router.get("/tree/")
def show_tree(path: str, subpath: str = "/") -> JSONResponse:
    """Function that tells flask to render the tree of the HDF5 file.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    queue: mp.Queue = mp.Queue()
    p = mp.Process(target=fetch_nodes, args=(path, subpath, queue))
    p.start()
    p.join()
    return NumpySafeJSONResponse(queue.get())


def fetch_nodes(path: str, subpath: str, queue: mp.Queue) -> None:
    path = "/" + path

    tr: Dict[str, Any] = defaultdict(dict)

    def visit_node(
        addr: Union[str, List[str]], node: h5py.HLObject, tree: Dict[str, Any] = tr
    ) -> None:
        if isinstance(addr, str):
            return visit_node(addr.split("/"), node)
        elif len(addr) > 1:
            return visit_node(addr[1:], node, tree[addr[0]]["subnodes"])
        else:
            tree[addr[0]] = {
                "subnodes": defaultdict(dict),
                "metadata": metadata(node),
            }

    with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as f:
        f.visititems(visit_node)

    queue.put(tr)
