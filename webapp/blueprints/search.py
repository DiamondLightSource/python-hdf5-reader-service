from fastapi import APIRouter
import h5py
import os
import sys

router = APIRouter()

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

# Setup blueprint route
@router.get("/search/{path:path}")
def get_nodes(path: str, subpath: str = "/"):
    """Function that tells flask to output the subnodes of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """
    path = "/" + path

    try:

        with h5py.File(path, "r", swmr=SWMR_DEFAULT, libver="latest") as file:
            if subpath:
                nodes = search(file[subpath])
            else:
                nodes = search(file["/"])
            return nodes

    except:
        print(f"File {file} can not be opened yet.")


def search(node):
    subnodes = safe_json_dump({"nodes": list(node.keys())})
    return subnodes


def safe_json_dump(content):
    """
    Try to use native orjson path; fall back to going through Python list.
    """
    import orjson

    def default(content):
        # No need to import numpy if it hasn't been used already.
        numpy = sys.modules.get("numpy", None)
        if numpy is not None:
            if isinstance(content, numpy.ndarray):
                # If we make it here, OPT_NUMPY_SERIALIZE failed because we have hit some edge case.
                # Give up on the numpy fast-path and convert to Python list.
                # If the items in this list aren't serializable (e.g. bytes) we'll recurse on each item.
                return content.tolist()
            elif isinstance(content, (bytes, numpy.bytes_)):
                return content.decode("utf-8")
        raise TypeError

    # Not all numpy dtypes are supported by orjson.
    # Fall back to converting to a (possibly nested) Python list.
    return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY, default=default)
