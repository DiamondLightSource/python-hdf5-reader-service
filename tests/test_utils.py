from typing import Any, Mapping

import h5py as h5
import pytest

from hdf5_reader_service.utils import h5_tree_map

_TEST_FILE = "./tests/test-data/p45-104.nxs"


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


TWO_LEVEL_RECURSION = "/entry/diamond_scan", {
    "diamond_scan": {
        "children": {
            "duration": {"contents": "META"},
            "end_time": {"contents": "META"},
            "keys": {"children": {"uid": {"contents": "META"}}, "contents": "META"},
            "scan_dead_time": {"contents": "META"},
            "scan_dead_time_percent": {"contents": "META"},
            "scan_estimated_duration": {"contents": "META"},
            "scan_finished": {"contents": "META"},
            "scan_models": {"contents": "META"},
            "scan_rank": {"contents": "META"},
            "scan_request": {"contents": "META"},
            "scan_shape": {"contents": "META"},
            "start_time": {"contents": "META"},
        },
        "contents": "META",
    }
}

LINKED_DATA = "/entry/DIFFRACTION", {
    "DIFFRACTION": {"children": {"data": {"contents": "META"}}, "contents": "META"}
}


@pytest.mark.parametrize(
    "path,expected_tree",
    [NO_RECURSION, ONE_LEVEL_RECURSION, TWO_LEVEL_RECURSION, LINKED_DATA],
)
def test_h5_visit_map(path: str, expected_tree: Mapping[str, Any]) -> None:
    with h5.File(_TEST_FILE) as f:
        tree = h5_tree_map(lambda name, obj: "META", f[path])

    assert expected_tree == tree
