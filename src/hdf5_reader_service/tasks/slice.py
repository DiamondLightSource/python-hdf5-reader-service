import multiprocessing as mp
from typing import Optional

import h5py


def fetch_slice(
    path: str, subpath: str, slice_info: Optional[str], swmr: bool, queue: mp.Queue
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

    with h5py.File(path, "r", swmr=swmr, libver="latest") as f:
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
