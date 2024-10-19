import logging
from flask_cors import CORS
from flask_session import Session
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from app.Blueprints.user import user_blueprint
from app.Blueprints.admin import admin_blueprint
from logging.handlers import RotatingFileHandler
from app.Blueprints.public import public_blueprint
from app.middleware.auth import Before_Request_middleware,After_Request_middleware

def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)
    jwt = JWTManager(app) # Initialize extensions
    Session(app);CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register Blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(public_blueprint)
    app.before_request(Before_Request_middleware)
    
    @app.after_request
    def apply_access_token(response):
        return After_Request_middleware(response)
    
    setup_logging(app)
    
    @app.errorhandler(Exception) # Log errors and critical issues only
    def handle_exception(e):
        app.logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return jsonify({"msg": "An error occurred contact admin..."}), 500
    
    @app.errorhandler(404) # 404 Error handler for not found URLs
    def page_not_found(e):
        return jsonify({"msg": "URL End Point Not Found"}), 404

    return app

def setup_logging(app):
    file_handler = RotatingFileHandler('app.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO) # Set the logging level to INFO (captures info, warning, error, and critical messages)
    app.logger.addHandler(file_handler) # Add the handler to the app's logger

