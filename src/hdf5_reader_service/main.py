import os

from fastapi import FastAPI  # , Response, status

from .blueprints import info, search, shapes, slice, tree

# Setup the app
app = FastAPI(root_path=os.path.abspath(os.path.dirname(__file__)))

app.include_router(tree.router)
app.include_router(info.router)
app.include_router(search.router)
app.include_router(slice.router)
app.include_router(shapes.router)


@app.get("/")
def index():
    return {"INFO": "Please provide a path to the HDF5 file, e.g. '/file/<path>'."}


# @app.get("/busy")
# def busy(response: Response):
#     if LOCK.locked():
#         response.status_code = status.HTTP_423_LOCKED
#     return {"busy": LOCK.locked()}
