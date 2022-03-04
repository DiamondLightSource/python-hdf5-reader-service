from urllib import response
from fastapi.testclient import TestClient
from webapp.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."
    }


def test_read_tree():
    response = client.get("/tree/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs?subpath=/")
    assert response.status_code == 200
    #assert response.json() == 


def test_read_metadata():
    response = client.get("/metadata/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs?subpath=/")
    assert response.status_code == 200
    #assert response.json() == 


def test_read_search():
    response = client.get("/search/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs?subpath=/")
    assert response.status_code == 200
    #assert response.json() == 

# def test_read_slice():
#     response = client.get("/slice/scratch/ryi58813/gda-master-tiled/gda_data_non_live/2022/0-0/p45-104.nxs?subpath=/")
#     assert response.status_code == 200
#     #assert response.json() == 