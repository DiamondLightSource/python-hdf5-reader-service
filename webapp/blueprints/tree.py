from fastapi import APIRouter

from .h5tree import TreeRenderer

router = APIRouter()

# Setup blueprint route
@router.get('/tree/{path:path}')
def show_tree(path: str, subpath: str = "/"):
    """Function that tells flask to render the tree of the HDF5 file.

    Returns:
        template: A rendered Jinja2 HTML template
    """

    path = "/" + path

    tr = TreeRenderer()

    try:
        return tr.render_tree(path + subpath)
    except Exception as e:
        return e
        #return f"Please provide a valid file path first. Received: {path + datapath}"
