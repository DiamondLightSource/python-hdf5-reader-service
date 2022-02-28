import logging
import os
# import argparse
from logging.handlers import RotatingFileHandler

from flask import Flask

# Setup the app
app = Flask(__name__, root_path=os.path.abspath(os.path.dirname(__file__)))
app.config.from_pyfile("config.py")

# Set up logging
handler = RotatingFileHandler("flask_log.log", maxBytes=100000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# import other parts of the app
# (Must be done after creating app due to circular imports)
from .blueprints import tree

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     "file_path", type=str, help="The path of the HDF5 file to be traversed."
# )
# args = parser.parse_args()

# app.path = args.file_path

@app.route("/")
def index():
    return "Hello world!"


app.register_blueprint(tree.blueprint)
