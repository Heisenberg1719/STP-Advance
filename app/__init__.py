from flask_cors import CORS
from flask_session import Session
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from app.Blueprints.user import user_blueprint
from app.Blueprints.admin import admin_blueprint
from app.Blueprints.public import public_blueprint
from app.middleware.auth import Before_Request_middleware,After_Request_middleware

def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)
    jwt = JWTManager(app) # Initialize extensions
    Session(app);CORS(app, supports_credentials=True)
    
    # Register Blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(public_blueprint)
    app.before_request(Before_Request_middleware)
    
    @app.after_request
    def apply_access_token(response):
        return After_Request_middleware(response)

    @app.errorhandler(Exception) # Log errors and critical issues only
    def handle_exception(e):
        return jsonify({"msg": "An error occurred contact admin..."}), 500
    
    @app.errorhandler(404) # 404 Error handler for not found URLs
    def page_not_found(e):
        return jsonify({"msg": "URL End Point Not Found"}), 404

    return app

