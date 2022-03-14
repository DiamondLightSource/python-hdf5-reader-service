from collections import defaultdict
import os
import time
from typing import Any, Dict, List, Union
import h5py
from fastapi import APIRouter

from webapp.blueprints.meta import metadata
from webapp.utils import NumpySafeJSONResponse, LOCK

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

router = APIRouter()

# Setup blueprint route
@router.get('/tree/{path:path}')
def show_tree(path: str, subpath: str = "/"):
    """Function that tells flask to render the tree of the HDF5 file.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    with LOCK:

        time.sleep(10)

        path = "/" + path

        tr = defaultdict(dict)

        def visit_node(addr: Union[str, List[str]], node: h5py.HLObject, tree: Dict[str, Any] = tr) -> None:
            if isinstance(addr, str):
                return visit_node(addr.split("/"), node)
            elif len(addr) > 1:
                return visit_node(addr[1:], node, tree[addr[0]]["subnodes"])
            else:
                tree[addr[0]] = {
                    "subnodes": defaultdict(dict),
                    "metadata": metadata(node)
                }

        try:
            with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
                file.visititems(visit_node)
            return NumpySafeJSONResponse(tr)
        except Exception as e:
            return e
