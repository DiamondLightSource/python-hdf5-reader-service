import h5py as h5

from hdf5_reader_service.utils import h5_tree_map


def test_h5_visit_map() -> None:
    with h5.File("./tests/test-data.nxs") as f:
        tree = h5_tree_map(lambda name, obj: "META", f["/entry/sample"])

    exptected = {
        "sample": {
            "children": {
                "description": {"contents": "META"},
                "name": {"contents": "META"},
            },
            "contents": "META",
        }
    }
    assert exptected == tree
