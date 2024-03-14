from flask import Blueprint

newrnnl = Blueprint('newrnnl', __name__)
from . import routes
