import os
from urllib import response

from fastapi.testclient import TestClient

from hdf5_reader_service.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."
    }


_PATH = os.path.abspath("tests/test-data.nxs")


def test_read_tree():
    response = client.get(f"/tree/?path={_PATH}")
    assert response.status_code == 200


def test_read_info():
    response = client.get(f"/info/?path={_PATH}")
    assert response.status_code == 200


def test_read_search():
    response = client.get(f"/search/?path={_PATH}")
    assert response.status_code == 200
