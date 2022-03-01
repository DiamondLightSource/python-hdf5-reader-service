import logging
import os
from markupsafe import escape
# import argparse
from logging.handlers import RotatingFileHandler

from flask import Flask

# Setup the app
app = Flask(__name__, root_path=os.path.abspath(os.path.dirname(__file__)))

# Set up logging
handler = RotatingFileHandler("flask_log.log", maxBytes=100000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# import other parts of the app
# (Must be done after creating app due to circular imports)
from .blueprints import tree, meta, search

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "file_path", type=str, help="The path of the HDF5 file to be traversed."
# )
# args = parser.parse_args()

# app.path = args.file_path


@app.route("/")
def index():
    return "Please provide a path to the HDF5 file after the '/'."

@app.route("/<path:file>")
def add_file(file):
    app.config["file"] = "/" + file
    return f"Added file path: {escape(file)}"


app.register_blueprint(tree.blueprint)
app.register_blueprint(meta.blueprint)
app.register_blueprint(search.blueprint)
