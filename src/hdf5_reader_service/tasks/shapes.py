import multiprocessing as mp
from typing import Any, Mapping

import h5py

from hdf5_reader_service.utils import h5_tree_map


def fetch_shapes(path: str, subpath: str, swmr: bool, queue: mp.Queue) -> None:

    path = "/" + path

    def get_shape(name: str, obj: h5py.HLObject) -> Mapping[str, Any]:
        if hasattr(obj, "shape"):
            return {"shape": obj.shape}
        else:
            return {"shape": None}

    with h5py.File(path, "r", swmr=swmr, libver="latest") as f:
        tree = h5_tree_map(get_shape, f, map_name="metadata")

    queue.put(tree)
