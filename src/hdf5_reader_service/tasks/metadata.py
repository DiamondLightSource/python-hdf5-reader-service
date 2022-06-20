import multiprocessing as mp
from typing import Any, Mapping

import h5py


def fetch_metadata(path: str, subpath: str, swmr: bool, queue: mp.Queue) -> None:

    path = "/" + path

    with h5py.File(path, "r", swmr=swmr, libver="latest") as f:
        if subpath:
            meta = metadata(f[subpath])
        else:
            meta = metadata(f["/"])
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
