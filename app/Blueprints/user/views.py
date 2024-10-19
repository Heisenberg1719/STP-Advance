from . import user_blueprint
from datetime import datetime
from app.logic.backend import backend
from http import HTTPStatus
from flask import jsonify, request, session
from flask_jwt_extended import (
jwt_required, create_access_token, create_refresh_token,
set_access_cookies, set_refresh_cookies, get_csrf_token)

class UserRoutes:
    @staticmethod
    @user_blueprint.route('/profile', methods=['GET'])
    @jwt_required()
    def user_profile():
        return jsonify("Welcome from userpanel home"), HTTPStatus.OK

    @staticmethod
    @user_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            if request.args.get('phone_number'):
                msg, code = backend.fetch_user(request.args.get('phone_number'))
                return jsonify(msg), code
            else:return jsonify({"Message": "Phone number not found"}), HTTPStatus.NOT_FOUND

        elif request.method == 'POST':
            if request.json.get('username') and request.json.get('password'):
                msg, code = backend.authenticate(request.json.get('username'), request.json.get('password'), "user")
                if code == HTTPStatus.OK:  # Clear the session if the same user is already logged in
                    if session.get('user_info') and session['user_info'].get('username') == request.json.get('username'):
                        session.clear()
                    session['user_info'] = {'username': request.json.get('username'),'logged_in': True,
                    'role': 'user','login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    access_token = create_access_token(identity=request.json.get('username'), additional_claims={"role": "user"})
                    refresh_token = create_refresh_token(identity=request.json.get('username'));response = jsonify(msg)
                    set_access_cookies(response, access_token);set_refresh_cookies(response, refresh_token)
                    response.set_cookie('csrf_access_token', get_csrf_token(access_token), httponly=True, secure=True)
                    response.set_cookie('csrf_refresh_token', get_csrf_token(refresh_token), httponly=True, secure=True)
                    return response, code
                else:return jsonify(msg), code  
            else:return jsonify({"ErrorMessage": "Username or password not provided"}), HTTPStatus.BAD_REQUEST

    @staticmethod
    @user_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        session.pop('user_info', None)
        response = jsonify({"msg": "User logged out successfully"})
        cookies_to_clear = ['access_token_cookie', 'refresh_token_cookie', 'csrf_access_token', 'csrf_refresh_token']
        for cookie in cookies_to_clear:response.set_cookie(cookie, '', expires=0, httponly=True, secure=True)
        return response, HTTPStatus.OK
