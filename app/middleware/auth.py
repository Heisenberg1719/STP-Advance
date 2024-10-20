import logging
from http import HTTPStatus  
from datetime import timedelta
from app.utils.appconfig.config import PathConfig
from flask import request, jsonify, g  
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt, create_access_token,set_access_cookies,get_csrf_token

def Before_Request_middleware():
    if request.path not in PathConfig.before_paths:
        try:
            verify_jwt_in_request()
            current_user, claims = get_jwt_identity(), get_jwt()
            if "user" in request.path and claims.get('role') == "user":pass  
            elif "admin" in request.path and claims.get('role') == "admin":pass 
            else:# Log unauthorized access attempt
                logging.warning(f"Unauthorized role access attempt by '{current_user}'. Path: {request.path}")
                return jsonify({"msg": "Unauthorized to Access"}), HTTPStatus.FORBIDDEN
        except KeyError as e:
            logging.error(f"KeyError: Missing key during role verification - {str(e)}", exc_info=True)
            return jsonify({"msg": "Token verification failed: Missing required information.", "error": str(e)}), HTTPStatus.BAD_REQUEST
        except Exception as e:
            logging.error(f"Error during token verification: {str(e)}", exc_info=True)
            return jsonify({"msg": "Token verification error.", "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    return None

def After_Request_middleware(response):
    try:
        if hasattr(g, 'new_access_token') and request.path not in PathConfig.after_paths:
            set_access_cookies(response, g.new_access_token)
            response.set_cookie('csrf_access_token', get_csrf_token(g.new_access_token), httponly=True, secure=False)
    except Exception as e:
        logging.error(f"Error setting new JWT token in cookie: {str(e)}", exc_info=True)
    return response
