import uuid
from datetime import timedelta

class Config:
    SECRET_KEY = str(uuid.uuid4())
    SESSION_TYPE = 'filesystem'  
    SESSION_PERMANENT = True
    JWT_SECRET_KEY =  str(uuid.uuid4())                 # JWT Configuration
    JWT_TOKEN_LOCATION = ['cookies']                    # Store JWT in cookies for increased security
    JWT_COOKIE_CSRF_PROTECT = True                      # Enable CSRF protection for JWT cookies
    JWT_ACCESS_COOKIE_HTTPONLY = True                   # HttpOnly flag to prevent XSS attacks
    JWT_REFRESH_COOKIE_HTTPONLY = True                  # HttpOnly flag for refresh tokens
    JWT_ACCESS_CSRF_COOKIE_HTTPONLY = True              # HttpOnly flag for CSRF access token
    JWT_REFRESH_CSRF_COOKIE_HTTPONLY = True             # HttpOnly flag for CSRF refresh token
    JWT_COOKIE_SECURE = True                            # Set to True to ensure cookies are only sent over HTTPS
    JWT_COOKIE_SAMESITE = 'Strict'                      # Strict cookie policy for improved security
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)     # Short-lived access token for increased security
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=15)   # Short-lived refresh token for increased security
    JWT_ACCESS_CSRF_TOKEN_EXPIRES = timedelta(minutes=5)    # Expiration for CSRF tokens matching access token lifetime
    JWT_REFRESH_CSRF_TOKEN_EXPIRES = timedelta(minutes=15)  # Expiration for CSRF tokens matching refresh token lifetime


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False                       # Disable secure cookies for local development
    JWT_COOKIE_SECURE = False                           # Disable secure cookies for HTTP testing in development
    JWT_ACCESS_CSRF_COOKIE_HTTPONLY = False             # Allow JS access to CSRF cookie for easier testing
    JWT_REFRESH_CSRF_COOKIE_HTTPONLY = False            # Allow JS access to CSRF cookie for easier testing

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True                        # Ensure session cookies are only sent over HTTPS
    JWT_COOKIE_SECURE = True                            # Ensure JWT cookies are only sent over HTTPS
    JWT_ACCESS_CSRF_COOKIE_HTTPONLY = True              # Prevent JS access to CSRF cookies in production
    JWT_REFRESH_CSRF_COOKIE_HTTPONLY = True             # Prevent JS access to CSRF cookies in production
    JWT_ACCESS_CSRF_COOKIE_HTTPONLY = True              # Prevent JS access to CSRF cookies in production
    JWT_REFRESH_CSRF_COOKIE_HTTPONLY = True             # Prevent JS access to CSRF cookies in production