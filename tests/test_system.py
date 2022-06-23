import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from hdf5_reader_service.main import app
from hdf5_reader_service.model import DataTree, ShapeMetadata
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


def test_read_info(test_data_path: Path):
    response = client.get(f"/info/?path={test_data_path}")
    assert response.status_code == 200


def test_read_search(test_data_path: Path):
    response = client.get(f"/search/?path={test_data_path}")
    assert response.status_code == 200
