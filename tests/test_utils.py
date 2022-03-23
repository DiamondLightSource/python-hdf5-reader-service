from typing import Any, Mapping

import h5py as h5
import pytest

from hdf5_reader_service.utils import h5_tree_map

_TEST_FILE = "./tests/test-data/p45-104.nxs"


# Test trees

NO_RECURSION = "/entry/sample/name", {"name": {"contents": "META"}}

ONE_LEVEL_RECURSION = "/entry/sample", {
    "sample": {
        "contents": "META",
        "subnodes": {"description": {"contents": "META"}, "name": {"contents": "META"}},
    }
}


TWO_LEVEL_RECURSION = "/entry/diamond_scan", {
    "diamond_scan": {
        "contents": "META",
        "subnodes": {
            "duration": {"contents": "META"},
            "end_time": {"contents": "META"},
            "keys": {
                "contents": "META",
                "subnodes": {
                    "izero": {"status": "MISSING_LINK"},
                    "uid": {"contents": "META"},
                },
            },
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
    }
}

LINKED_DATA = "/entry/DIFFRACTION", {
    "DIFFRACTION": {
        "contents": "META",
        "subnodes": {
            "data": {"contents": "META"},
            "simx": {"status": "MISSING_LINK"},
            "simy": {"status": "MISSING_LINK"},
        },
    }
}


@pytest.mark.parametrize(
    "path,expected_tree",
    [NO_RECURSION, ONE_LEVEL_RECURSION, TWO_LEVEL_RECURSION, LINKED_DATA],
)
def test_h5_visit_map(path: str, expected_tree: Mapping[str, Any]) -> None:
    with h5.File(_TEST_FILE) as f:
        tree = h5_tree_map(lambda name, obj: "META", f[path])

    from pprint import pprint

    pprint(tree)
    assert expected_tree == tree


def test_rename_contents() -> None:
    with h5.File(_TEST_FILE) as f:
        tree = h5_tree_map(
            lambda name, obj: "META", f["/entry/diamond_scan"], map_name="metadata"
        )

    assert {
        "diamond_scan": {
            "metadata": "META",
            "subnodes": {
                "duration": {"metadata": "META"},
                "end_time": {"metadata": "META"},
                "keys": {
                    "metadata": "META",
                    "subnodes": {
                        "izero": {"status": "MISSING_LINK"},
                        "uid": {"metadata": "META"},
                    },
                },
                "scan_dead_time": {"metadata": "META"},
                "scan_dead_time_percent": {"metadata": "META"},
                "scan_estimated_duration": {"metadata": "META"},
                "scan_finished": {"metadata": "META"},
                "scan_models": {"metadata": "META"},
                "scan_rank": {"metadata": "META"},
                "scan_request": {"metadata": "META"},
                "scan_shape": {"metadata": "META"},
                "start_time": {"metadata": "META"},
            },
        }
    } == tree


def test_rename_subnodes() -> None:
    with h5.File(_TEST_FILE) as f:
        tree = h5_tree_map(
            lambda name, obj: "META", f["/entry/diamond_scan"], subtree_name="children"
        )

    assert {
        "diamond_scan": {
            "contents": "META",
            "children": {
                "duration": {"contents": "META"},
                "end_time": {"contents": "META"},
                "keys": {
                    "contents": "META",
                    "children": {
                        "izero": {"status": "MISSING_LINK"},
                        "uid": {"contents": "META"},
                    },
                },
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
        }
    } == tree
