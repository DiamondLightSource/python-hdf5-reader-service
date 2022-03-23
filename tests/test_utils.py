from typing import Any, Mapping

import h5py as h5
import pytest

from hdf5_reader_service.utils import h5_tree_map

_TEST_FILE = "./tests/test-data.nxs"


# Test trees

NO_RECURSION = "/entry/sample/name", {"name": {"contents": "META"}}

ONE_LEVEL_RECURSION = "/entry/sample", {
    "sample": {
        "children": {
            "description": {"contents": "META"},
            "name": {"contents": "META"},
        },
        "contents": "META",
    }
}


TWO_LEVEL_RECURSION = "/entry/instrument", {
    "instrument": {
        "children": {
            "DIFFRACTION": {
                "children": {"count_time": {"contents": "META"}},
                "contents": "META",
            },
            "IZERO": {
                "children": {"count_time": {"contents": "META"}},
                "contents": "META",
            },
            "beamline": {"contents": "META"},
            "name": {"contents": "META"},
            "simx": {"children": {}, "contents": "META"},
            "simy": {"children": {}, "contents": "META"},
        },
        "contents": "META",
    }
}


@pytest.mark.parametrize(
    "path,expected_tree", [NO_RECURSION, ONE_LEVEL_RECURSION, TWO_LEVEL_RECURSION]
)
def test_h5_visit_map(path: str, expected_tree: Mapping[str, Any]) -> None:
    with h5.File("./tests/test-data.nxs") as f:
        tree = h5_tree_map(lambda name, obj: "META", f[path])

    assert expected_tree == tree
