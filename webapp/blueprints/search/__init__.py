from flask import Blueprint

blueprint = Blueprint('search', __name__)

from . import search