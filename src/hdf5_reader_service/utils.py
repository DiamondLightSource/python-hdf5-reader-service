import sys
from typing import Any, Callable, Dict, List, Mapping, Union

import h5py as h5
from pydantic import BaseModel
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
            elif isinstance(content, BaseModel):
                # Handle the pydantic model case
                return content.dict()
        raise TypeError

    # Not all numpy dtypes are supported by orjson.
    # Fall back to converting to a (possibly nested) Python list.
    return orjson.dumps(content, option=orjson.OPT_SERIALIZE_NUMPY, default=default)


class NumpySafeJSONResponse(JSONResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, content: Any) -> bytes:
        return safe_json_dump(content)


#: Something that can be passed to json.dump
_Jsonable = Union[Mapping[str, Any], List[Any], bool, int, float, str]

#: A callback to pass to a tree map, do "this" to every node and leaf
_VisitCallback = Callable[[str, h5.HLObject], _Jsonable]


def h5_tree_map(
    callback: _VisitCallback,
    root: h5.HLObject,
    map_name: str = "contents",
    subtree_name: str = "subnodes",
) -> Mapping[str, Any]:
    name = root.name.split("/")[-1]
    block = {name: {map_name: callback(name, root)}}

    if hasattr(root, "items"):
        subtree: Dict[str, Any] = {}
        for k, v in root.items():
            if v is not None:
                subtree = {
                    **subtree,
                    **h5_tree_map(callback, v, map_name, subtree_name),
                }
            else:
                subtree = {**subtree, **{k: {"status": "MISSING_LINK"}}}
        block[name][subtree_name] = subtree

    return block
