import os
from pathlib import Path

from fastapi.testclient import TestClient

from hdf5_reader_service.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."
    }


def test_read_shapes(test_data_path: Path):
    response = client.get(f"/shapes/?path={test_data_path}")
    assert response.status_code == 200


def test_read_tree(test_data_path: Path):
    response = client.get(f"/tree/?path={test_data_path}")
    assert response.status_code == 200


def test_read_info(test_data_path: Path):
    response = client.get(f"/info/?path={test_data_path}")
    assert response.status_code == 200


def test_read_search(test_data_path: Path):
    response = client.get(f"/search/?path={test_data_path}")
    assert response.status_code == 200
