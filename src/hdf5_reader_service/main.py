import os

import click
from fastapi import FastAPI  # , Response, status

from ._version_git import __version__
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


@click.group(invoke_without_command=True)
@click.option(
    "-h",
    "--host",
    type=str,
    help="host IP",
    default="0.0.0.0",
)
@click.option(
    "-p",
    "--port",
    type=int,
    help="host port",
    default="8000",
)
@click.version_option(version=__version__)
def main(host: str, port: int) -> None:
    import uvicorn

    uvicorn.run(app, host=host, port=port)
