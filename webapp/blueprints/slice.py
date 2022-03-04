import h5py
import os
import re
from fastapi import APIRouter, Query
from ..utils import safe_json_dump

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

# Setup blueprint route
@router.get("/slice/{path:path}")
def get_slice(path: str, subpath: str = "/", slice: str = None):
    """Function that tells flask to output the metadata of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """

    path = "/" + path

    if slice is not None:
        slices = re.search("(\d+):(\d+):(\d+)", slice)
        if slice:
            slice_start = int(slices[1])
            slice_stop = int(slices[2])
            slice_step = int(slices[3])
        else:
            print("Defaulting to 'all'.")
            slice_start = 0
            slice_stop = 0
            slice_step = 0
    else:
        return "Please enter a valid url, e.g. \
            '/slice/<path>?subpath=<subpath>?slice=<slice>'"

    try:
        with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
            try:
                if subpath and isinstance(file[subpath], h5py.Dataset):
                    sliced = file[subpath][slice_start:slice_stop:slice_step]
                    return safe_json_dump(sliced)
                else:
                    # meta = metadata(file["/"])
                    print("Path not valid or not a dataset.")
                # return meta
            except Exception as e:
                print(e)

    except:
        print(f"File {file} can not be opened yet.")
