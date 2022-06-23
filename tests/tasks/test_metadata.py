from pathlib import Path

import pytest

from hdf5_reader_service.model import (
    ByteOrder,
    DatasetMacroStructure,
    DatasetMicroStructure,
    DatasetStructure,
    MetadataNode,
)
from hdf5_reader_service.tasks import fetch_metadata

TEST_CASES = {
    "/": MetadataNode(
        name="/",
        attributes={
            "file_name": "/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs"  # noqa: E501
        },
    ),
    "/entry": MetadataNode(
        name="/entry", attributes={"NX_class": "NXentry", "default": "DIFFRACTION"}
    ),
    "/entry/DIFFRACTION/data": MetadataNode(
        name="/entry/data",
        attributes={},
        structure=DatasetStructure(
            macro=DatasetMacroStructure(
                shape=(20, 20, 120, 160), chunks=(1, 1, 60, 160)
            ),
            micro=DatasetMicroStructure(
                itemsize=1, kind="u", byte_order=ByteOrder.NOT_APPLICABLE
            ),
        ),
    ),
}


@pytest.mark.parametrize("subpath,expected", TEST_CASES.items())
def test_metadata(test_data_path: Path, subpath: str, expected: MetadataNode) -> None:
    metadata = fetch_metadata(str(test_data_path), subpath, True)
    assert expected == metadata
