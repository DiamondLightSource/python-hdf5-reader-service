from flask import current_app as app
import h5py
import os
import sys
from flask.json import JSONEncoder

from . import blueprint

SWMR_DEFAULT = bool(int(os.getenv("HDF5_SWMR_DEFAULT", "1")))

# Setup blueprint route
@blueprint.route("/metadata/", defaults={"subpath": None}, methods=["GET"])
@blueprint.route("/metadata/<path:subpath>", methods=["GET"])
def get_meta(subpath):
    """Function that tells flask to output the metadata of the HDF5 file node.

    Returns:
        template: A rendered Jinja2 HTML template
    """

    app.logger.info("-> meta")

    file = app.config["file"]

    if not isinstance(file, h5py.File):
        try:

            with h5py.File(
                app.config["file"], "r", swmr=SWMR_DEFAULT, libver="latest"
            ) as file:
                if subpath:
                    meta = metadata(file[subpath])
                else:
                    meta = metadata(file["/"])
                return meta

        except:
            print(f"File {file} can not be opened yet.")


def metadata(node):
    d = safe_json_dump(dict(node.attrs))
    # for k, v in list(d.items()):
    #     # Convert any bytes to str.
    #     d[k] = safe_json_dump(v)
    return d


class JSON_Improved(JSONEncoder):

    pass


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
