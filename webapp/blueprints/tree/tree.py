from flask import Blueprint
from flask import current_app as app
from flask import render_template

from . import blueprint
from .h5tree import TreeRenderer


# Setup blueprint route
@blueprint.route('/tree', methods=['GET', 'POST'])
def show_tree():
    """Function that tells flask to render the tree of the HDF5 file.

    Returns:
        template: A rendered Jinja2 HTML template
    """

    app.logger.info('-> tree')

    tr = TreeRenderer()

    return tr.render_tree(app.config["HDF5_PATH"])
    # Render the compare template, passing along the dataframe json
    #return render_template('/data/data.html.j2')
