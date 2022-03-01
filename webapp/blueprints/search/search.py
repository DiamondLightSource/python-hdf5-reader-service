from flask import current_app as app
import h5py
import os
import sys
from flask.json import JSONEncoder

from . import blueprint

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

# Setup blueprint route
@blueprint.route("/search/", defaults={"subpath": None}, methods=["GET"])
@blueprint.route("/search/<path:subpath>", methods=["GET"])
def get_nodes(subpath):
    """Function that tells flask to output the subnodes of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """

    app.logger.info("-> search")

    file = app.config["file"]

    if not isinstance(file, h5py.File):
        try:

            with h5py.File(
                app.config["file"], "r", swmr=SWMR_DEFAULT, libver="latest"
            ) as file:
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
