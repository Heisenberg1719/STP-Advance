import random,json,bcrypt
from http import HTTPStatus
from app.utils.Database.queries import *
from app.utils.Database.connection import MySQLDatabase
# from app.services.neobiz import neobiz_payments

class backend:
  def fetch_admin(data):
    results = MySQLDatabase.fetch_results(fetch_admin_query, (data,))
    if results.get('data'):
      return results.get('data', [{}])[0], (results.get('status') if isinstance(results.get('status'), list) else [results.get('status', HTTPStatus.INTERNAL_SERVER_ERROR)])[0]
    else:return {"Message": "User Not Found"},  HTTPStatus.NOT_FOUND

  def fetch_user(data):
    results = MySQLDatabase.fetch_results(fetch_user_query, (data,))
    if results.get('data'):
      return results.get('data', [{}])[0], (results.get('status') if isinstance(results.get('status'), list) else [results.get('status', HTTPStatus.INTERNAL_SERVER_ERROR)])[0]
    else:return {"Message": "User Not Found"},  HTTPStatus.NOT_FOUND

  def authenticate(username, password, role):
      query = authenticate_admin_query if role == "admin" else authenticate_user_query
      results = MySQLDatabase.fetch_results(query, (username,))
      if results.get('data') and bcrypt.checkpw(password.encode('utf-8'), results['data'][0]['password'].encode('utf-8')):
          return {"successMsg": "User authenticated successfully"}, HTTPStatus.OK
      return {"errorMsg": "Invalid password"}, HTTPStatus.UNAUTHORIZED
