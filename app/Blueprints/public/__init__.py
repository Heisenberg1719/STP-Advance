from flask import Blueprint

public_blueprint = Blueprint('public', __name__)

from . import views  # Import views after defining the public_blueprint
