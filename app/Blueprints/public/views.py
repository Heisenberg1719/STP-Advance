from flask import jsonify,session
from . import public_blueprint 
from http import HTTPStatus
from app.utils.services.get_info import get_system_details
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies,unset_jwt_cookies

@public_blueprint.route('/', methods=['GET'])
def public_info():
    return jsonify(message="Public Information version 1.2", data = get_system_details()), 200

@public_blueprint.route('/tokenRefresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = jsonify({"msg": "Token refreshed"})
    set_access_cookies(response, new_access_token)
    return response , 200
 