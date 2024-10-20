import logging
from http import HTTPStatus
from datetime import datetime
from . import admin_blueprint
from app.logic.backend import backend
from flask import jsonify, request, session
from flask_jwt_extended import (
jwt_required, create_access_token, create_refresh_token,
set_access_cookies, set_refresh_cookies, get_csrf_token,unset_jwt_cookies)

class AdminRoutes:
    @staticmethod
    @admin_blueprint.route('/profile', methods=['GET'])
    @jwt_required()
    def admin_dashboard():
      return jsonify({"msg": "Welcome to the admin dashboard!"}), 200

    @staticmethod
    @admin_blueprint.route('/login', methods=['GET', 'POST'])
    def admin_login():
      if request.method == 'GET':
        if request.args.get('phone_number'):
          msg, code = backend.fetch_admin(request.args.get('phone_number'))
          return jsonify(msg), code
        else:return jsonify({"Message": "Phone number not found"}), 404

      elif request.method == 'POST':
        if request.json.get('username') and request.json.get('password'):
          msg, code = backend.authenticate(request.json.get('username'), request.json.get('password'), "admin")
          if code == HTTPStatus.OK:  # Clear the session if the same admin is already logged in
            if session.get('admin_info') and session['admin_info'].get('username') == request.json.get('username'):
              session.pop('admin_info', None)
            session['admin_info'] = { 'login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'username': request.json.get('username'), 'logged_in': True,'role': 'admin'}
            access_token = create_access_token(identity=request.json.get('username'), additional_claims={"role": "admin"})
            refresh_token = create_refresh_token(identity=request.json.get('username'));response = jsonify(msg)
            set_access_cookies(response, access_token);set_refresh_cookies(response, refresh_token)
            response.set_cookie('csrf_access_token', get_csrf_token(access_token), httponly=True, secure=True)
            response.set_cookie('csrf_refresh_token', get_csrf_token(refresh_token), httponly=True, secure=True)
            return response, code
          else:return jsonify(msg), code  
        else:return jsonify({"ErrorMessage": "Username or password not provided"}), HTTPStatus.BAD_REQUEST

    @admin_blueprint.route('/logout', methods=['GET'])
    @jwt_required()
    def logout():
      try:
        response = jsonify({"msg": "Logout successful"})
        session.pop('admin_info', None);unset_jwt_cookies(response)
        return response, HTTPStatus.OK
      except Exception as e:
        return jsonify({"msg": "Logout failed", "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
