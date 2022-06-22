from pathlib import Path

import pytest

from hdf5_reader_service.model import NodeChildren
from hdf5_reader_service.tasks.search import fetch_children

TEST_CASES = {
    "/": NodeChildren(nodes=["entry"]),
    "/entry": NodeChildren(
        nodes=[
            "DIFFRACTION",
            "DIFFRACTION.sum",
            "IZERO",
            "IZERO.sum",
            "diamond_scan",
            "duration",
            "end_time",
            "experiment_identifier",
            "instrument",
            "program_name",
            "sample",
            "scan_shape",
            "start_time",
        ]
    ),
    "/entry/DIFFRACTION": NodeChildren(nodes=["data", "simx", "simy"]),
}


@pytest.mark.parametrize("subpath,expected", TEST_CASES.items())
def test_fetch_children(
    test_data_path: Path, subpath: str, expected: NodeChildren
) -> None:
    children = fetch_children(str(test_data_path), subpath, True)
    assert expected == children


def test_fetch_children_of_dataset(test_data_path: Path) -> None:
    with pytest.raises(KeyError):
        fetch_children(str(test_data_path), "/entry/DIFFRACTION/data", True)


def test_fetch_children_of_broken_link(test_data_path: Path) -> None:
    with pytest.raises(KeyError):
        fetch_children(str(test_data_path), "/entry/DIFFRACTION/simx", True)
