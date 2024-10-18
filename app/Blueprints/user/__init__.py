from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

from . import views  # Import views after defining the user_blueprint
