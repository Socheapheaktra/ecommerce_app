import os
from flask import Flask, jsonify, redirect
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from db import db

import models

from resources.user import blp as UserBlueprint
from resources.role import blp as RoleBlueprint
# from resources.tag import blp as TagBlueprint
# from resources.user import blp as UserBlueprint


def create_app():
    # Initialize Flask Application
    app = Flask(__name__)
    CORS(app)

    app.config['PROPAGATE_EXCEPTIONS'] = True # I have no IDEA WTF this is
    app.config['API_TITLE'] = "E-Commerce REST API" # Name of your API
    app.config['API_VERSION'] = 'v1' # Version of your API
    app.config['OPENAPI_VERSION'] = "3.0.3" # Also Version of your API Documents
    app.config['OPENAPI_URL_PREFIX'] = '/' # URL Prefix
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui" # API Document's Path
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/" # Swagger API cdn
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db" # Connection String to your database
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@localhost/db_name" # Connection String to your database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Also no idea wtf this is
    db.init_app(app) # Initialize Database
    # migrate = Migrate(app, db) # Migrate Database

    api = Api(app) # Link API
    
    # Randomly Generated SECRET KEY
    # app.config['JWT_SECRET_KEY'] = "273400726116270771902746508700512837087"
    # jwt = JWTManager(app)

    """
    These methods use to modify the Error response about the Authorization
    """

    # Check if the access token is in BLOCKLIST
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(jwt_header, jwt_payload):
    #     return models.TokenModel.query.filter_by(token=jwt_payload['jti']).first()

    # Return the response if the token has been revoked
    # @jwt.revoked_token_loader
    # def revoked_token_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({
    #             "description": "The access token has been revoked.",
    #             "error": "token_revoked"
    #         }),
    #         401
    #     )

    # @jwt.needs_fresh_token_loader
    # def token_not_fresh_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify({
    #             "description": "The token is not fresh.",
    #             "error": "fresh_token_required"
    #         }),
    #         401
    #     )

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     # Do sth in database to verify whether the user is admin or not
    #     if identity == 1:
    #         return {"is_admin": True}

    #     return {"is_admin": False}
    
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return (jsonify({"message": "The token has expired.", "erro": "token expired."}), 401)

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (jsonify({"message": "Signature verification failed.", "error": "invalid token."}), 401)

    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return (jsonify({
    #         "description": "Request does not contain access token.",
    #         "error": "authorization required."
    #     }), 401)

    @app.before_first_request
    def create_table():
        db.create_all()

    api.register_blueprint(UserBlueprint) 
    api.register_blueprint(RoleBlueprint)
    # api.register_blueprint(TagBlueprint)
    # api.register_blueprint(UserBlueprint)

    @app.route('/')
    def home():
        return redirect('/swagger-ui')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5010)