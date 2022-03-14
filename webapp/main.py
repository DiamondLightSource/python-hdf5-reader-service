import os
from .utils import LOCK

from fastapi import FastAPI, Response, status

# Setup the app
app = FastAPI(root_path=os.path.abspath(os.path.dirname(__file__)))


# import other parts of the app
# (Must be done after creating app due to circular imports)
from .blueprints import tree, meta, search, slice

app.include_router(tree.router)
app.include_router(meta.router)
app.include_router(search.router)
app.include_router(slice.router)


@app.get("/")
def index():
    return {"INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."}


@app.get("/busy")
def busy(response: Response):
    if LOCK.locked():
        response.status_code = status.HTTP_423_LOCKED
    return {"busy": LOCK.locked()}