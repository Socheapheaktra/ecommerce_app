import os

UPLOADED_IMAGES_DEST = os.path.join('static', 'images')

PROPAGATE_EXCEPTIONS = True
JSON_SORT_KEYS = False

API_TITLE = 'E-Commerce REST API'
API_VERSION = 'v1'
API_PREFIX = '/api'
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
HOST = "0.0.0.0"
PORT = 5010