import sys
from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Union

import h5py as h5
from starlette.responses import JSONResponse


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
                # If we make it here, OPT_NUMPY_SERIALIZE failed because we have
                # hit some edge case. Give up on the numpy fast-path and convert
                # to Python list. If the items in this list aren't serializable
                # (e.g. bytes) we'll recurse on each item.
                return content.tolist()
            elif isinstance(content, (bytes, numpy.bytes_)):
                return content.decode("utf-8")
        raise TypeError

    # Not all numpy dtypes are supported by orjson.
    # Fall back to converting to a (possibly nested) Python list.
    return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY, default=default)


class NumpySafeJSONResponse(JSONResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, content: Any) -> bytes:
        return safe_json_dump(content)


_VisitCallback = Callable[[str, h5.HLObject], Mapping[str, Any]]


def h5_tree_map(
    callback: _VisitCallback, root: h5.HLObject, map_name: str = "contents"
):
    name = root.name.split("/")[-1]
    block = {name: {"contents": callback(name, root)}}

    if hasattr(root, "values"):
        subtree = {}
        for v in root.values():
            subtree = {**subtree, **h5_tree_map(callback, v)}
        block[name]["children"] = subtree

    return block


# def fetch_nodes(path: str, subpath: str, queue: mp.Queue) -> None:
#     path = "/" + path

#     tr = {}

#     def visit_node(addr: str, node: h5.HLObject) -> None:
#         if isinstance(addr, str):
#             return visit_node(addr.split("/"), node)
#         elif len(addr) > 1:
#             return visit_node(addr[1:], node, tree[addr[0]]["subnodes"])
#         else:
#             tree[addr[0]] = {
#                 "subnodes": defaultdict(dict),
#                 "metadata": metadata(node),
#             }
