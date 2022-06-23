import os
from pathlib import Path
from typing import Any, Dict, Mapping

import pytest
from fastapi.testclient import TestClient

from hdf5_reader_service.main import app
from hdf5_reader_service.model import (
    ByteOrder,
    DatasetMacroStructure,
    DatasetMicroStructure,
    DatasetStructure,
    DataTree,
    MetadataNode,
    NodeChildren,
    ShapeMetadata,
)
from tests.tasks.test_metadata import TEST_CASES as METADATA_TEST_CASES
from tests.tasks.test_search import TEST_CASES as SEARCH_TEST_CASES
from tests.tasks.test_shapes import TEST_CASES as SHAPE_TEST_CASES

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."
    }


@pytest.mark.parametrize("subpath,shape", SHAPE_TEST_CASES.items())
def test_read_shapes(
    test_data_path: Path, subpath: str, shape: DataTree[ShapeMetadata]
):
    response = client.get(
        "/shapes/", params={"path": test_data_path, "subpath": subpath}
    )
    assert response.status_code == 200
    actual_shape = DataTree[ShapeMetadata].parse_obj(response.json())
    assert actual_shape == shape


def test_read_tree(test_data_path: Path):
    response = client.get(f"/tree/?path={test_data_path}")
    assert response.status_code == 200


@pytest.mark.parametrize("subpath,metadata", METADATA_TEST_CASES.items())
def test_read_info(test_data_path: Path, subpath: str, metadata: MetadataNode):
    response = client.get("/info/", params={"path": test_data_path, "subpath": subpath})
    assert response.status_code == 200
    actual_metadata = MetadataNode.parse_obj(response.json())
    assert actual_metadata == metadata


@pytest.mark.parametrize("subpath,children", SEARCH_TEST_CASES.items())
def test_read_search(test_data_path: Path, subpath: str, children: NodeChildren):
    response = client.get(
        "/search/", params={"path": test_data_path, "subpath": subpath}
    )
    assert response.status_code == 200
    actual_children = NodeChildren.parse_obj(response.json())
    assert actual_children == children
