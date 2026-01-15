from flask import Blueprint

bp = Blueprint('models', __name__)


from .employee import *