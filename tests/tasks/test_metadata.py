from pathlib import Path

from hdf5_reader_service.model import MetadataNode
from hdf5_reader_service.tasks import fetch_metadata


def test_metadata(test_data_path: Path) -> None:
    expected = MetadataNode(
        name="/",
        attributes={
            "file_name": b"/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs"
        },
    )
    metadata = fetch_metadata(str(test_data_path), "/", True)

    assert expected == metadata
