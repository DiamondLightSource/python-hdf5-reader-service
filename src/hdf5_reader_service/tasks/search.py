import h5py

from hdf5_reader_service.model import NodeChildren


def fetch_children(path: str, subpath: str, swmr: bool) -> NodeChildren:
    path = "/" + path

    with h5py.File(path, "r", swmr=swmr, libver="latest") as f:
        node = f[subpath]
        if isinstance(node, h5py.Group):
            return NodeChildren(nodes=list(node.keys()))
        else:
            raise KeyError(f"{path}/{subpath} is not a group")
